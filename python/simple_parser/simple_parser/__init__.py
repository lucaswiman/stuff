from collections import namedtuple

from toolz import interleave


class Rule(object):
    def matches_at_position(self, string, position):
        """
        Returns a generator of matches in the string which start at position.
        """
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)

    def __add__(self, other):
        return Concatenation(self, other)

    def __or__(self, other):
        return Disjunction(self, other)

    def parse(self, string):
        """
        Returns an iterator of all parse trees of the string for the given rule.
        """
        for match in self.matches_at_position(string, 0):
            if match.length == len(string):
                yield match

    def matches(self, string):
        return bool(next(self.parse(string), False))


class Match(namedtuple('Match', ('string', 'position', 'length', 'rule', 'children'))):
    def __new__(cls, string, position, length, rule=None, children=()):
        return super(Match, cls).__new__(cls, string, position, length, rule, children)

    def __str__(self):
        return self.string[self.position:self.position + self.length]


class _Epsilon(Rule):
    __slots__ = ()

    def __new__(cls):
        try:
            return Epsilon
        except NameError:
            return super(_Epsilon, cls).__new__(cls)

    def __hash__(self):
        return hash(self.__class__)

    def matches_at_position(self, string, position):
        # consumes 0 characters whatever the string
        yield Match(string, position, 0, rule=self)

    def __add__(self, other):
        return other

    def __radd__(self, other):
        return other


Epsilon = _Epsilon()


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

    def matches_at_position(self, string, position):
        if string.startswith(self.literal, position):
            yield Match(string, position, self.length, rule=self)


class Concatenation(Rule):
    __slots__ = ('head', 'tail')

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

    def matches_at_position(self, string, position):
        for match in self.head.matches_at_position(string, position):
            for tail_match in self.tail.matches_at_position(string, position + match.length):
                children = (match, ) + (tail_match.children if tail_match.children else (tail_match, ))
                yield Match(
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

    def __eq__(self, other):
        return isinstance(other, Disjunction) and tuple.__eq__(self, other)

    def matches_at_position(self, string, position):
        # Do a breadth-first search over the set of matches.
        return interleave(
            disjunct.matches_at_position(string, position)
            for disjunct in self)


class Reference(Rule):
    __slots__ = ('name', 'namespace')
    def __init__(self, name, namespace):
        self.name = name
        self.namespace = namespace

    def __repr__(self):
        return 'Reference<%r>' % self.name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (
            isinstance(other, Reference) and
            self.name == other.name and
            self.namespace is other.namespace)

    def matches_at_position(self, string, position):
        return self.namespace[self.name].matches_at_position(string, position)
