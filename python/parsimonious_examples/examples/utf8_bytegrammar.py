from parsimonious import Grammar, NodeVisitor

UTF8_GRAMMAR = Grammar(r"""
    # Grammar that parses bytes as UTF-8.  See https://en.wikipedia.org/wiki/UTF-8#Encoding
    text = encoded_character*
    encoded_character = ascii / two_bytes / three_bytes / four_bytes

    # Standard ascii range; single-byte unicode character.
    ascii = ~b"[\x00-\x7f]"

    # Two bytes. The first bite consists of all characters whose codepoints
    # have 10 as their most significant bits, 0b11000000-0b11011111.
    two_bytes = ~b"[\xc0-\xdf]" subsequent_byte
    
    # Three bytes. First byte is 0b11100000-0b11101111
    three_bytes = ~b"[\xe0-\xef]" subsequent_byte subsequent_byte

    # Four bytes. First byte is 0b11110000-0b11110111
    four_bytes = ~b"[\xf0-\xf7]" subsequent_byte subsequent_byte subsequent_byte

    # 0b10000000-0b10111111
    subsequent_byte = ~b"[\x80-\xbf]"
""")

class Utf8Decoder(NodeVisitor):
    def generic_visit(self, node, children) -> int:
        assert len(node.text) == 1
        return node.text[0]

    def visit_subsequent_byte(self, node, _) -> int:
        return node.text[0] & 0b00_111111

    def visit_ascii(self, node, children):
        return node.text[0]

    def visit_two_bytes(self, node, children):
        return self.concat(children[0] & 0b000_11111, *children[1:])

    def visit_three_bytes(self, node, children):
        return self.concat(children[0] & 0b0000_1111, *children[1:])

    def visit_four_bytes(self, node, children):
        return self.concat(children[0] & 0b00000_111, *children[1:])

    def concat(self, *ints) -> int:
        acc = 0
        for i in ints:
            acc <<= i.bit_length()
            acc |= i
        breakpoint()
        return acc

    def visit_encoded_character(self, node, codepoints):
        try:
            [codepoint] = codepoints
            return chr(codepoint)
        except Exception as e:
            breakpoint()

    def visit_text(self, node, characters) -> str:
        try:
            return ''.join(characters)
        except Exception as e:
            breakpoint()


def assert_parses_correctly(s: str):
    for c in s:
        encoded = c.encode('utf-8')
        assert isinstance(encoded, bytes)
        tree = UTF8_GRAMMAR.parse(encoded)
        result = Utf8Decoder().visit(tree)
        assert result == c, f"{result=} != {c=}"


assert_parses_correctly("✅ªº7djjd•••")