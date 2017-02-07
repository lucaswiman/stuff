from __future__ import absolute_import

from parsimonious import Grammar, NodeVisitor

JSON_GRAMMAR = r"""
    json = _ (object / empty_object / list / empty_list / string / number / boolean / null) _

    object = "{" (key_value ",")* key_value "}"
        key_value = _ string _ ":" json
    empty_object = _ "{" _ "}" _

    list = "[" (json ",")* json "]"
    empty_list = _ "[" _ "]" _

    string = '"' ~'[^"]*' '"'  # does not handle escaping or 'quotes'
    number = ~"nan|inf|[-+]?[0-9]*\.?[0-9]+(e[-+]?[0-9]+)?"i
    boolean = "true" / "false"
    null = "null"
    _ = ~'\s*'
"""

JSON = Grammar(JSON_GRAMMAR)


class JSONVisitor(NodeVisitor):
    grammar = JSON

    def visit_json(self, node, children):
        _, [obj], _ = children
        return obj

    def visit_object(self, node, children):
        lbrac, separated_children, last_child, rbrac = children
        key_values = [kv for [kv, comma] in separated_children] + [last_child]
        return dict(key_values)

    def visit_empty_object(self, node, children):
        return {}

    def visit_key_value(self, node, children):
        _, key, _, colon, value = children
        return (key, value)

    def visit_list(self, node, children):
        lbrac, separated_children, last_child, rbrac = children
        return [elem for elem, comma in separated_children] + [last_child]

    def visit_empty_list(self, node, children):
        return []

    def visit_string(self, node, children):
        quote, text, quote = children
        return text

    def visit_number(self, node, children):
        return float(node.text)

    def visit_boolean(self, node, children):
        return {'true': True, 'false': False}[node.text]

    def visit__(self, node, children):
        return None

    def visit_null(self, node, children):
        return None

    def generic_visit(self, node, children):
        return children or node.text

examples = [
    '[1, "asdf", {"true": true, "false": false, "null": null}, {"a": "b"}, null, "inf", {}, []]'
]
if __name__ == '__main__':
    from json import loads
    for example in examples:
        print('Example: %r' % example)
        expected = loads(example)
        actual = JSONVisitor().parse(example)
        assert expected == actual
