
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import itertools
import operator
import re
from ast import literal_eval
from collections import namedtuple, OrderedDict
try:
    from functools import reduce, partial
except ImportError:
    from six.moves import reduce as reduce
    from functools import partial as partial
import attr
from pyrsistent import pset


class Grammar(OrderedDict):

    def __init__(self, grammar_text=None):
        self.default_rule = None
        super(Grammar, self).__init__()
        if grammar_text:
            GrammarVisitor(grammar=self).parse(grammar_text)

    def parse(self, string):
        '\n        Returns the first parse tree found by parsing string according to the default rule\n        '
        tree = self.default_rule.parse(string)
        if (tree is None):
            raise ParseError(string)
        return tree

    def __setitem__(self, key, value):
        if (key in self):
            raise ValueError(('Rule %r already defined: %r' %
                              (key, self[key])))
        super(Grammar, self).__setitem__(
            key, NamedRule(key, value, grammar=self))

    def define_rule(self, rule_definition, default_rule=False):
        '\n        Takes in a rule definition and a visitor method, and adds a rule to the grammar\n        of the appropriate name. This allows a grammar definition to be right next to the\n        visitor code that deserializes it.\n\n        class MyVisitor(NodeVisitor):\n            grammar = Grammar()\n\n            @grammar.define_rule(\'number+\', default_rule=True)\n            def visit_numbers(self, node, *children):\n                return int(\'\'.join(children))\n            @grammar.define_rule(\'"0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"\')\n            def visit_number(self, node, *children):\n                return node.text\n\n        After executing this code, MyVisitor.grammar will consist of two rules (numbers and\n        number), with number the default.\n        '
        if isinstance(rule_definition, Rule):
            rule = rule_definition
        else:
            parsed = GrammarVisitor.grammar['rule_definition'].parse(
                rule_definition)
            rule = GrammarVisitor(self).visit(parsed)

        def decorator(visit_method):
            if (not visit_method.__name__.startswith('visit_')):
                raise ValueError(
                    ('Cannot interpret name for %r' % visit_method))
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
            visitor_method = getattr(self, ('visit_%s' % name), visitor_method)
        visited_children = [self.visit(child) for child in node.children]
        visited_children = [
            child for child in visited_children if (child is not IGNORED)]
        result = visitor_method(*([node] + list(visited_children)))
        return result

    def generic_visit(self, node, *children):
        if (len(children) == 1):
            return children[0]
        else:
            return (children or node.text)


class Rule(object):

    def matches_at_position(self, string, position):
        '\n        Returns a generator of matches in the string which start at position.\n\n        Should be implemented by subclasses.\n        '
        raise NotImplementedError

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __add__(self, other):
        return Concatenation(self, other)

    def __or__(self, other):
        return Disjunction(self, other)

    @property
    def i(self):
        '\n        Shorthand to ignore a rule in visitors.\n        '
        return Ignored(self)

    def all_parses(self, string):
        '\n        Returns an iterator of all parse trees of the string for the given rule.\n        '
        for match in self.matches_at_position(string, 0, stack=pset()):
            if (match.length == len(string)):
                (yield match)

    def parse(self, string):
        '\n        Returns a parse tree, or None if the string is not matched by the rule.\n        '
        return next(self.all_parses(string), None)


class NamedRule(Rule):
    __slots__ = ('name', 'rule', 'ignored')

    def __init__(self, name, rule, grammar):
        self.name = name
        self.rule = rule
        self.grammar = grammar

    def __eq__(self, other):
        return (isinstance(other, NamedRule) and (self.name == other.name) and (self.rule == other.rule) and (self.grammar is other.grammar))

    def __hash__(self):
        return hash((self.name, self.rule))

    def __repr__(self):
        return ('NamedRule(%r, %r)' % (self.name, self.rule))

    def __str__(self):
        return '{self.name} = {self.rule}'.format(self=self)

    def matches_at_position(self, string, position, stack):
        for match in self.rule.matches_at_position(string, position, stack):
            (yield Node(string, position, match.length, self, children=match.children))


def should_ignore(rule):
    if isinstance(rule, Reference):
        return (rule.ignored or should_ignore(rule.referent))
    elif isinstance(rule, NamedRule):
        return should_ignore(rule.rule)
    else:
        return isinstance(rule, Ignored)


class Node(namedtuple('Node', ('string', 'position', 'length', 'rule', 'children'))):

    def __new__(cls, string, position, length, rule=None, children=()):
        return super(Node, cls).__new__(cls, string, position, length, rule, children)

    @property
    def text(self):
        return self.string[self.position:(self.position + self.length)]

    def __repr__(self):
        if self.children:
            return ('<%s s[%s:%s]=%r %r>' % (self.rule, self.position, (self.position + self.length), self.text, [child for child in self.children if (not should_ignore(child.rule))]))
        else:
            return ('<%s s[%s:%s]=%r>' % (self.rule, self.position, (self.position + self.length), self.text))

    def __str__(self):
        return self.text


@attr.s(init=False, hash=True, cmp=True, str=False)
class Literal(Rule):
    literal = attr.ib()
    length = attr.ib()

    def __init__(self, literal):
        self.literal = literal
        self.length = len(literal)

    def __str__(self):
        return repr(self.literal)

    def matches_at_position(self, string, position, stack=pset()):
        if string.startswith(self.literal, position):
            (yield Node(string, position, self.length, rule=self))


Epsilon = Literal('')


@attr.s(init=False, hash=True, cmp=True, repr=False, str=False)
class Concatenation(Rule):
    head = attr.ib()
    tail = attr.ib()

    def __new__(cls, *args):
        if (not args):
            return Epsilon
        elif (len(args) == 1):
            return args[0]
        else:
            concat = super(Concatenation, cls).__new__(cls)
            concat.head = args[0]
            concat.tail = Concatenation(*list(args[1:]))
            return concat

    def __iter__(self):
        cur = self
        while isinstance(cur, Concatenation):
            (yield cur.head)
            cur = cur.tail
        (yield cur)

    def __repr__(self):
        return ('Concatenation(%s)' % ', '.join(map(repr, self)))

    def __str__(self):
        return ('(%s)' % ' '.join((str(r) for r in self if (r is not Epsilon))))

    def __add__(self, other):
        if isinstance(other, Concatenation):
            return Concatenation(*list((tuple(self) + tuple(other))))
        else:
            return Concatenation(*list((tuple(self) + (other,))))

    def matches_at_position(self, string, position, stack=pset()):
        if ((self, position) in stack):
            return
        stack = stack.add((self, position))
        for match in self.head.matches_at_position(string, position, stack=stack):
            for tail_match in self.tail.matches_at_position(string, (position + match.length), stack=stack):
                tail_children = (tail_match.children if isinstance(
                    self.tail, Concatenation) else (tail_match,))
                children = ((match,) + tail_children)
                (yield Node(string, position, length=(match.length + tail_match.length), children=children, rule=self))


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
        return ('%s%s' % (self.__class__.__name__, super(Disjunction, self).__repr__()))

    def __str__(self):
        return ('(%s)' % ' | '.join((str(r) for r in self)))

    def __add__(self, other):
        return Rule.__add__(self, other)

    def __hash__(self):
        if (not hasattr(self, '_hash')):
            self._hash = tuple.__hash__(self)
        return self._hash

    def __eq__(self, other):
        return (isinstance(other, Disjunction) and tuple.__eq__(self, other))

    def matches_at_position(self, string, position, stack=pset()):
        if ((self, position) in stack):
            return
        stack = stack.add((self, position))
        matches = itertools.chain(
            *list((disjunct.matches_at_position(string, position, stack=stack) for disjunct in self)))
        for match in matches:
            (yield match)


@attr.s(slots=True, hash=False, cmp=False, repr=False, str=False)
class Reference(Rule):
    name = attr.ib()
    grammar = attr.ib()
    ignored = attr.ib(default=False)

    def __repr__(self):
        return ('Reference<%r, ignored=%r>' % (self.name, self.ignored))

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash((self.name, self.ignored))

    def __str__(self):
        if self.ignored:
            return ('%s.ignore' % self.name)
        return self.name

    def __eq__(self, other):
        return (isinstance(other, Reference) and (self.name == other.name) and (self.grammar is other.grammar))

    @property
    def referent(self):
        return self.grammar[self.name]

    def matches_at_position(self, string, position, stack=pset()):
        if ((self, position) in stack):
            return
        stack = stack.add((self, position))
        for match in self.referent.matches_at_position(string, position, stack=stack):
            (yield Node(string, position, match.length, rule=self, children=(match,)))


def validate_charclass(instance, attribute, regex):
    if (not re.match('^\\[([^\\]]|(?<=\\\\)\\])+\\]$', regex.pattern)):
        raise ValueError(('%r does not look like a charclass' % regex.pattern))


@attr.s(slots=True, hash=True, cmp=True, str=False)
class Charclass(Rule):
    '\n    A regular expression character class.\n\n    Note that we do not allow full regular expressions here for the following reasons:\n    1. PCRE\'s can recognize some languages which are not even context-free due to backreferences.\n    2. Using Python\'s regex engine means that we have very limited control over how many\n       characters are captured: we can select either "as many as possible" or "as few as\n       possible". This means we might miss valid parse trees because the regex rule matched\n       either too much or too little. I\'m uncertain whether the resulting language would still\n       be context free.\n\n    Including this class makes the bootstrap grammar much easier.\n\n    TODO: add a subgrammar for regular expressions, and transform it to production rules.\n    That would replace this rule once the grammar has been bootstrapped.\n    '
    re = attr.ib(convert=re.compile, validator=validate_charclass)

    def __str__(self):
        return ('/%s/' % self.re.pattern)

    def matches_at_position(self, string, position, stack=pset()):
        match = self.re.match(string, position)
        if (match is not None):
            (yield Node(string, position, 1, rule=self))


@attr.s(slots=True, hash=True, cmp=True, str=False, repr=False)
class Ignored(Rule):
    '\n    Class for marking that visitors should ignore matches from this rule. It can be\n    used in the following syntaxes:\n\n    foo.ignored = ...  # This will ignore visiting all references to foo.\n    bar = foo.ignored "asdf"  # Only this reference will be ignored.\n    baz = "foo".ignore "baz"  # The word "foo" will be ignored.\n    quux = "foo".i "baz"  # Abbreviation for ignore.\n    '
    rule = attr.ib()

    def __repr__(self):
        return ('%r.i' % (self.rule,))

    def __str__(self):
        return ('%s.ignore' % (self.rule,))

    def matches_at_position(self, string, position, stack=pset()):
        for match in self.rule.matches_at_position(string, position, stack):
            (yield Node(string, position, match.length, rule=self, children=(match,)))


class VisitationError(Exception):
    pass


class ParseError(Exception):
    pass


BOOTSTRAP_GRAMMAR = Grammar()
(ref, L) = (partial(Reference, grammar=BOOTSTRAP_GRAMMAR), Literal)


def star(rule, grammar):
    identifier_name = ('star_%s' % len(grammar))
    grammar[identifier_name] = (
        (rule + Reference(identifier_name, grammar)) | Epsilon.i)
    return grammar[identifier_name]


def plus(rule, grammar):
    identifier_name = ('plus_%s' % len(grammar))
    grammar[identifier_name] = (
        rule + (Reference(identifier_name, grammar) | Epsilon.i))
    return grammar[identifier_name]


def optional(rule, grammar):
    return (rule | Epsilon.i)


class GrammarVisitor(NodeVisitor):
    grammar = BOOTSTRAP_GRAMMAR

    @grammar.define_rule(ref('rule_assignments'), default_rule=True)
    def visit_rules(self, node, names_and_rules):
        self.constructed_grammar.update(names_and_rules)
        self.constructed_grammar.default_rule = self.constructed_grammar[names_and_rules[0][0]]
        return self.constructed_grammar

    @grammar.define_rule(((ref('_') + ref('rule_assignment')) + ((ref('whitespace').i + ref('rule_assignments')) | ref('_'))))
    def visit_rule_assignments(self, node, rule_assignment, names_and_rules=()):
        return ((rule_assignment,) + names_and_rules)
    grammar['_'] = (
        (ref('whitespace') + ((ref('comment') + ref('_')) | Epsilon)) | Epsilon).i
    grammar['whitespace'] = (Charclass('[\\s]') +
                             (ref('whitespace') | Epsilon)).i
    grammar['comment'] = (Literal('#') + ref('EOL'))
    grammar['EOL'] = (star(Charclass('[^\\n]'), grammar) + Literal('\n'))
    grammar['escaped_quote_body'] = (
        ((Charclass('[^"]') | L('\\"')) + ref('escaped_quote_body')) | Epsilon)
    grammar['unquantified_term'] = (
        ((ref('reference') | ref('charclass')) | ref('literal')) | ref('parenthesized'))
    grammar['term'] = (ref('quantified') | ref('unquantified_term'))
    grammar['rule_definition'] = ref('disjunction')
    grammar['rule_name'] = ref('identifier')
    grammar['parenthesized'] = ((L('(').i + ref('rule_definition')) + L(')').i)
    grammar['rule_assignment'] = (
        (((ref('rule_name') + ref('_')) + L('=').i) + ref('_')) + ref('rule_definition'))
    grammar['ignored_term'] = (
        ref('term') + (L('.') + (L('ignore') | L('i'))).i)

    def __init__(self, grammar=None):
        self.constructed_grammar = (
            Grammar() if (grammar is None) else grammar)

    @grammar.define_rule((ref('concatenation') + ((((ref('_') + L('|').i) + ref('_')) + ref('disjunction')) | Epsilon.i)))
    def visit_disjunction(self, node, *disjuncts):
        return reduce(operator.or_, disjuncts)

    @grammar.define_rule((Charclass('[\\w]') + (ref('identifier') | Epsilon).i))
    def visit_identifier(self, node, *_):
        return node.text

    @grammar.define_rule(ref('identifier'))
    def visit_reference(self, node, identifier):
        return Reference(identifier, grammar=self.constructed_grammar)

    @grammar.define_rule((((Literal('\\]') | Charclass('[^\\]]')) + ref('charclass_body')) | Epsilon.i))
    def visit_charclass_body(self, node, *_):
        return node.text

    @grammar.define_rule(((Literal('[') + ref('charclass_body')) + Literal(']')))
    def visit_charclass(self, node, *_):
        return Charclass(node.text)

    @grammar.define_rule(((ref('unquantified_term') + ref('_')) + Charclass('[*+?]')))
    def visit_quantified(self, node, term, quantifier):
        builders = {
            '*': star,
            '+': plus,
            '?': optional,
        }
        return builders[quantifier](term, self.grammar)

    @grammar.define_rule((ref('term') + ((ref('_') + ref('concatenation')) | Epsilon.i)))
    def visit_concatenation(self, node, *terms):
        return reduce(operator.add, terms)

    @grammar.define_rule(((L('"').i + ref('escaped_quote_body').i) + L('"').i))
    def visit_literal(self, node):
        return Literal(literal_eval(node.text))


foo = 'asdf'
x = '{}'.format(foo)
