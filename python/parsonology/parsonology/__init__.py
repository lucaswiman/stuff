import operator
import re
from ast import literal_eval
from collections import namedtuple, OrderedDict
from functools import reduce, partial

import itertools
from pyrsistent import pset


class Grammar(OrderedDict):

    def __init__(self, grammar_text=None):
        self.default_rule = None
        super(Grammar, self).__init__()
        if grammar_text:
            GrammarVisitor(grammar=self).parse(grammar_text)

    def parse(self, string):
        """
        Returns the first parse tree found by parsing string according to the default rule
        """
        tree = self.default_rule.parse(string)
        if tree is None:
            raise ParseError(string)
        return tree

    def __setitem__(self, key, value):
        if key in self:
            raise ValueError('Rule %r already defined: %r' % (key, self[key]))
        super(Grammar, self).__setitem__(key, NamedRule(key, value, grammar=self))

    def define_rule(self, rule_definition, default_rule=False):
        """
        Takes in a rule definition and a visitor method, and adds a rule to the grammar
        of the appropriate name. This allows a grammar definition to be right next to the
        visitor code that deserializes it.

        class MyVisitor(NodeVisitor):
            grammar = Grammar()

            @grammar.define_rule('number+', default_rule=True)
            def visit_numbers(self, node, *children):
                return int(''.join(children))
            @grammar.define_rule('"0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"')
            def visit_number(self, node, *children):
                return node.text

        After executing this code, MyVisitor.grammar will consist of two rules (numbers and
        number), with number the default.
        """
        if isinstance(rule_definition, Rule):
            rule = rule_definition
        else:
            parsed = GrammarVisitor.grammar['rule_definition'].parse(rule_definition)
            rule = GrammarVisitor(self).visit(parsed)

        def decorator(visit_method):
            if not visit_method.__name__.startswith('visit_'):
                raise ValueError('Cannot interpret name for %r' % visit_method)
            name = visit_method.__name__[len('visit_'):]
            self[name] = rule
            if default_rule:
                self.default_rule = self[name]

            return visit_method

        return decorator


IGNORED = object()


class NodeVisitor(object):
    def parse(self, string):
        tree = self.grammar.parse(string)
        return self.visit(tree)

    def visit(self, node):
        visitor_method = self.generic_visit
        if should_ignore(node.rule):
            return IGNORED
        if isinstance(node.rule, Reference):
            [child] = node.children
            return self.visit(child)

        name = getattr(node.rule, 'name', None)
        if name:
            visitor_method = getattr(self, 'visit_%s' % name, visitor_method)
        visited_children = [self.visit(child) for child in node.children]
        visited_children = [child for child in visited_children if child is not IGNORED]
        result = visitor_method(node, *visited_children)
        return result

    def generic_visit(self, node, *children):
        return children or node.text


class Rule(object):
    def matches_at_position(self, string, position):
        """
        Returns a generator of matches in the string which start at position.

        Should be implemented by subclasses.
        """
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return Concatenation(self, other)

    def __or__(self, other):
        return Disjunction(self, other)

    @property
    def i(self):
        """
        Shorthand to ignore a rule in visitors.
        """
        return Ignored(self)

    def all_parses(self, string):
        """
        Returns an iterator of all parse trees of the string for the given rule.
        """
        for match in self.matches_at_position(string, 0, stack=pset()):
            if match.length == len(string):
                yield match

    def parse(self, string):
        """
        Returns a parse tree, or None if the string is not matched by the rule.
        """
        return next(self.all_parses(string), None)


class NamedRule(Rule):
    __slots__ = ('name', 'rule', 'ignored')

    def __init__(self, name, rule, grammar):
        self.name = name
        self.rule = rule
        self.grammar = grammar

    def __eq__(self, other):
        return (
            isinstance(other, NamedRule) and
            self.name == other.name and
            self.rule == other.rule and
            self.grammar is other.grammar)

    def __hash__(self):
        return hash((self.name, self.rule))

    def __repr__(self):
        return 'NamedRule(%r, %r)' % (self.name, self.rule)

    def matches_at_position(self, string, position, stack):
        for match in self.rule.matches_at_position(string, position, stack):
            # Unpack the match for the wrapped rule, and set its rule attribute
            # to self.
            yield Node(string, position, match.length, self, children=match.children)


def should_ignore(rule):
    if isinstance(rule, Reference):
        return rule.ignored or should_ignore(rule.referent)
    elif isinstance(rule, NamedRule):
        return should_ignore(rule.rule)
    else:
        return isinstance(rule, Ignored)



class Node(namedtuple('Node', ('string', 'position', 'length', 'rule', 'children'))):
    def __new__(cls, string, position, length, rule=None, children=()):
        return super(Node, cls).__new__(cls, string, position, length, rule, children)

    @property
    def text(self):
        return self.string[self.position:self.position+self.length]

    def __str__(self):
        return self.text


class Literal(Rule):
    __slots__ = ('literal', 'length')

    def __init__(self, literal):
        self.literal = literal
        self.length = len(literal)

    def __hash__(self):
        return hash(self.literal)

    def __eq__(self, other):
        return isinstance(other, Literal) and other.literal == self.literal

    def __repr__(self):
        return 'Literal(%r)' % self.literal

    def matches_at_position(self, string, position, stack=pset()):
        if string.startswith(self.literal, position):
            yield Node(string, position, self.length, rule=self)


Epsilon = Literal('')


class Concatenation(Rule):
    __slots__ = ('head', 'tail', '_hash')

    def __new__(cls, *args):
        if not args:
            return Epsilon
        elif len(args) == 1:
            return args[0]
        else:
            concat = super(Concatenation, cls).__new__(cls)
            concat.head = args[0]
            concat.tail = Concatenation(*args[1:])
            return concat

    def __eq__(self, other):
        return (
            isinstance(other, Concatenation) and
            self.head == other.head and
            self.tail == other.tail)

    def __hash__(self):
        if not hasattr(self, '_hash'):
            self._hash = hash((self.__class__, self.head, self.tail))
        return self._hash

    def __iter__(self):
        cur = self
        while isinstance(cur, Concatenation):
            yield cur.head
            cur = cur.tail
        yield cur

    def __repr__(self):
        return 'Concatenation(%s)' % ', '.join(map(repr, self))

    def __add__(self, other):
        if isinstance(other, Concatenation):
            return Concatenation(*(tuple(self) + tuple(other)))
        else:
            return Concatenation(*(tuple(self) + (other, )))

    def matches_at_position(self, string, position, stack=pset()):
        if (self, position) in stack:
            # Prevent infinite recursion for zero-length terminals
            return
        stack = stack.add((self, position))
        for match in self.head.matches_at_position(string, position, stack=stack):
            for tail_match in self.tail.matches_at_position(string, position + match.length, stack=stack):
                tail_children = tail_match.children if isinstance(self.tail, Concatenation) else (tail_match, )
                children = (match, ) + tail_children
                yield Node(
                    string,
                    position,
                    length=match.length + tail_match.length,
                    children=children,
                    rule=self,
                )


class Disjunction(tuple, Rule):
    def __new__(cls, *args):
        disjuncts = []
        for arg in args:
            if isinstance(arg, Disjunction):
                disjuncts.extend(arg)
            else:
                disjuncts.append(arg)
        return super(Disjunction, cls).__new__(cls, disjuncts)

    def __repr__(self):
        return '%s%s' % (self.__class__.__name__, super(Disjunction, self).__repr__())

    def __add__(self, other):
        return Rule.__add__(self, other)

    def __hash__(self):
        if not hasattr(self, '_hash'):
            self._hash = tuple.__hash__(self)
        return self._hash

    def __eq__(self, other):
        return isinstance(other, Disjunction) and tuple.__eq__(self, other)

    def matches_at_position(self, string, position, stack=pset()):
        # Do a breadth-first search over the set of matches.
        if (self, position) in stack:
            # Prevent infinite recursion for zero-length terminals
            return
        stack = stack.add((self, position))
        matches = itertools.chain(*(
            disjunct.matches_at_position(string, position, stack=stack)
            for disjunct in self))
        for match in matches:
            yield match


class Reference(Rule):
    __slots__ = ('name', 'grammar', 'ignored')
    def __init__(self, name, grammar, ignored=False):
        self.name = name
        self.grammar = grammar
        self.ignored = ignored

    def __repr__(self):
        return 'Reference<%r, ignored=%r>' % (self.name, self.ignored)

    def __hash__(self):
        return hash((self.name, self.ignored))

    def __str__(self):
        if self.ignored:
            return '%s.ignore' % self.name
        return self.name

    def __eq__(self, other):
        return (
            isinstance(other, Reference) and
            self.name == other.name and
            self.grammar is other.grammar)

    @property
    def referent(self):
        return self.grammar[self.name]

    def matches_at_position(self, string, position, stack=pset()):
        if (self, position) in stack:
            # Prevent infinite recursion for zero-length matches.
            return
        stack = stack.add((self, position))
        for match in self.referent.matches_at_position(string, position, stack=stack):
            yield Node(string, position, match.length, rule=self, children=(match, ))


class Charclass(Rule):
    """
    A regular expression character class.

    Note that we do not allow full regular expressions here for the following reasons:
    1. PCRE's can recognize some languages which are not even context-free due to backreferences.
    2. Using Python's regex engine means that we have very limited control over how many
       characters are captured: we can select either "as many as possible" or "as few as
       possible". This means we might miss valid parse trees because the regex rule matched
       either too much or too little. I'm uncertain whether the resulting language would still
       be context free.

    Including this class makes the bootstrap grammar much easier.

    TODO: add a subgrammar for regular expressions, and transform it to production rules.
    That would replace this rule once the grammar has been bootstrapped.
    """
    __slots__ = ('re', )

    def __init__(self, charclass):
        if not re.match(r'^\[([^\]]|(?<=\\)\])+\]$', charclass):
            raise ValueError('This does not look like a charclass')
        self.re = re.compile(charclass)

    def __repr__(self):
        return 'Charclass(%r)' % self.re.pattern

    def __str__(self):
        return '/%r/' % self.re.pattern

    def __hash__(self):
        return hash(self.re)

    def __eq__(self, other):
        return isinstance(other, Charclass) and self.re.pattern == other.re.pattern

    def matches_at_position(self, string, position, stack=pset()):
        match = self.re.match(string, position)
        if match is not None:
            yield Node(string, position, 1, rule=self)


class Ignored(Rule):
    """
    Class for marking that visitors should ignore matches from this rule. It can be
    used in the following syntaxes:

    foo.ignored = ...  # This will ignore visiting all references to foo.
    bar = foo.ignored "asdf"  # Only this reference will be ignored.
    baz = "foo".ignore "baz"  # The word "foo" will be ignored.
    quux = "foo".i "baz"  # Abbreviation for ignore.
    """
    __slots__ = ('rule', )

    def __init__(self, rule):
        self.rule = rule

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.rule)

    def __str__(self):
        return '%s.ignore' % self.rule

    def __hash__(self):
        return hash((Ignored, self.rule))

    def __eq__(self, other):
        return isinstance(other, Ignored) and self.rule == other.rule

    def matches_at_position(self, string, position, stack=pset()):
        for match in self.rule.matches_at_position(string, position, stack):
            yield Node(
                string, position, match.length, rule=self, children=(match, )
            )


class VisitationError(Exception):
    pass


class ParseError(Exception):
    pass


BOOTSTRAP_GRAMMAR = Grammar()
ref, L = partial(Reference, grammar=BOOTSTRAP_GRAMMAR), Literal


class GrammarVisitor(NodeVisitor):
    grammar = BOOTSTRAP_GRAMMAR
    grammar['_'] = (Epsilon | (Charclass(r'[\s]') + ref('_'))).i
    grammar['identifier'] = Charclass(r'[\w]') + (ref('identifier') | Epsilon)
    grammar['escaped_quote_body'] = (Charclass(r'[^"]') | L('\\"')) + (ref('escaped_quote_body') | Epsilon)

    def __init__(self, grammar=None):
        self.constructed_grammar = Grammar() if grammar is None else grammar

    # We want disjunction to have lower precedence than concatenation.
    @grammar.define_rule(ref('disjunction'))
    def visit_rule_definition(self, node, rule):
        return rule

    @grammar.define_rule(ref('concatenation') + ((ref('_') + L("|").i + ref('_') + ref('disjunction')) | Epsilon.i))
    def visit_disjunction(self, node, *disjuncts):
        return reduce(operator.or_, disjuncts)

    @grammar.define_rule(ref('reference') | ref('charclass') | ref('literal') | ref('parenthesized'))
    def visit_term(self, node, item):
        return item

    @grammar.define_rule(L("(").i + ref('rule_definition') + L(")").i)
    def visit_parenthesized(self, node, rule_definition):
        return rule_definition

    @grammar.define_rule(ref('identifier'))
    def visit_reference(self, node, *_):
        return Reference(node.text, grammar=self.constructed_grammar)

    @grammar.define_rule(((Literal('\]') | Charclass(r'[^\]]')) + ref('charclass_body')) | Epsilon.i)
    def visit_charclass_body(self, node, *_):
        return node.text

    @grammar.define_rule(Literal('[') + ref('charclass_body') + Literal(']'))
    def visit_charclass(self, node, *_):
        return Charclass(node.text)

    @grammar.define_rule(ref('term') + ((ref('_') + ref('concatenation')) | Epsilon.i))
    def visit_concatenation(self, node, first_term, *term_groups):
        terms = [first_term]

        # TODO: this is really ugly. Is there some way to introspect that
        # `(ref('_').i + ref('term')` will always have a useless form that should
        # be automatically unpacked.
        terms.extend(t for (t, ) in term_groups)
        return reduce(operator.add, terms)

    @grammar.define_rule(
        ref('_') + ref('rule_assignment') + ref('_') + (ref('rule_assignment') | Epsilon.i),
        default_rule=True)
    def visit_rule_assignments(self, node, *names_and_rules):
        self.constructed_grammar.update(names_and_rules)
        self.constructed_grammar.default_rule = self.constructed_grammar[names_and_rules[0][0]]
        return self.constructed_grammar

    @grammar.define_rule(ref('rule_name') + ref('_') + L("=").i + ref('_') + ref('rule_definition'))
    def visit_rule_assignment(self, node, name, rule):
        return name, rule

    @grammar.define_rule(L('"').i + ref('escaped_quote_body').i + L('"').i)
    def visit_literal(self, node):
        return Literal(literal_eval(node.text))


def bootstrap(definition):
    def decorator(method):
        method = GrammarVisitor.grammar.define_rule(definition)(method)
        setattr(GrammarVisitor, method.__name__, method)
        return method
    return decorator


@bootstrap('identifier')
def visit_rule_name(self, node, *ignored):
    return node.text


@bootstrap('term "." ("ignore" | "i")')
def visit_ignored_term(self, term, *_):
    return Ignored(term)
