import re, string

def char_is_escapable(char):
    try:
        regex = re.compile(r'[\{char}]'.format(char=char))
    except Exception:
        return False
    return {c for c in string.printable if regex.match(c)} == {char}


print('Escapable chars: %r' % ''.join(filter(char_is_escapable, string.printable)))
print('Non-escapable chars: %r' % ''.join(c for c in string.printable if not char_is_escapable(c)))



