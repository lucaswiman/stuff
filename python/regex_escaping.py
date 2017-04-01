import re, string

def char_is_escapable_in_ranges(char):
    try:
        regex = re.compile(r'[\{char}-\{char}]'.format(char=char))
    except Exception:
        return False
    return {c for c in string.printable if regex.match(c)} == {char}


RANGE_ESCAPABLE_CHARS = ''.join(filter(char_is_escapable_in_ranges, string.printable))

print('Escapable chars: %r' % RANGE_ESCAPABLE_CHARS)
print('Non-escapable chars: %r' % ''.join(c for c in string.printable if not char_is_escapable_in_ranges(c)))
print('u is escapable: %s' % char_is_escapable_in_ranges('u'))
print('U is escapable: %s' % char_is_escapable_in_ranges('U'))
