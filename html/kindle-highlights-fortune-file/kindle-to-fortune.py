import os
from io import BytesIO
from getpass import getpass

##### Encrypt / decrypt the file so we're not storing the copyrighted highlights in github.
##### Based on http://stackoverflow.com/questions/16761458/how-to-aes-encrypt-decrypt-files-using-python-pycrypto-in-an-openssl-compatible
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random
import lxml.html
from lxml.cssselect import CSSSelector

def derive_key_and_iv(password, salt, key_length, iv_length):
    d = d_i = ''
    while len(d) < key_length + iv_length:
        d_i = md5(d_i + password + salt).digest()
        d += d_i
    return d[:key_length], d[key_length:key_length+iv_length]


def encrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = Random.new().read(bs - len('Salted__'))
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    out_file.write('Salted__' + salt)
    finished = False
    while not finished:
        chunk = in_file.read(1024 * bs)
        if len(chunk) == 0 or len(chunk) % bs != 0:
            padding_length = bs - (len(chunk) % bs)
            chunk += padding_length * chr(padding_length)
            finished = True
        out_file.write(cipher.encrypt(chunk))


def decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]
    key, iv = derive_key_and_iv(password, salt, key_length, bs)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    next_chunk = ''
    finished = False
    while not finished:
        chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
        if len(next_chunk) == 0:
            padding_length = ord(chunk[-1])
            if padding_length < 1 or padding_length > bs:
               raise ValueError("bad decrypt pad (%d)" % padding_length)
            # all the pad-bytes must be the same
            if chunk[-padding_length:] != (padding_length * chr(padding_length)):
               # this is similar to the bad decrypt:evp_enc.c from openssl program
               raise ValueError("bad decrypt")
            chunk = chunk[:-padding_length]
            finished = True
        out_file.write(chunk)


def ensure_encrypted_file_exists(password):
    if os.path.isfile('./highlights.html.encrypted'):
        return None
    assert os.path.isfile('./highlights.html')
    with open('./highlights.html', 'rb') as f:
        orig = f.read()
        f.seek(0)
        with open('./highlights.html.encrypted', 'wb') as out:
            encrypted = encrypt(f, out, password)
    return orig


def get_decrypted_text(password):
    assert os.path.isfile('./highlights.html.encrypted')
    if os.path.isfile('./highlights.html'):
        with open('./highlights.html', 'rb') as f:
            return f.read()
    with open('./highlights.html.encrypted', 'rb') as f:
        out = BytesIO()
        decrypt(f, out, password)
    return out.getvalue()


def parse_highlights_html(html):
    node = lxml.html.fromstring(html)
    useless_nodes = (
        list(CSSSelector('.addEditNote')(node)) +
        list(CSSSelector('.editNote')(node)) +
        list(CSSSelector('script')(node)) + 
        list(CSSSelector('#header')(node)) + 
        list(CSSSelector('form')(node))
    )
    for useless in useless_nodes:
        useless.getparent().remove(useless)
    return parse_element_into_books(CSSSelector('#allHighlightedBooks')(node)[0])


from refo import finditer, Predicate, Literal, Any, Group, Star, Plus
from collections import *
import re
from blessings import Terminal
TERM = Terminal()


class Highlight(namedtuple('Highlight', ['text', 'location'])):
    def __new__(cls, element):
        text = element[0].text.replace('ââ', '"').replace('â', "'")
        [location] = re.findall('Read\xa0more\xa0at\xa0location\xa0(\d+)', element[1].text)
        return super(Highlight, cls).__new__(cls, text=text, location=int(location))
    

class Book(namedtuple('Book', ['title', 'author', 'highlights'])):
    def __new__(cls, elements):
        book_elem, *highlight_elems = elements
        highlights = [Highlight(elem) for elem in highlight_elems]
        title = book_elem[0][0].text
        [author] = re.findall(r'\s+by (.*\S)\s+$', book_elem[1].text)
        return super(Book, cls).__new__(cls, title=title, author=author, highlights=highlights)


def parse_element_into_books(html_elements):
    # Based on https://github.com/machinalis/refo/blob/master/examples/xml_reader.py
    is_header = lambda elem: elem.get('class').startswith('bookMain')
    is_highlight = lambda elem: elem.get('class').startswith('highlightRow')
    regex = Group(Predicate(is_header) + Plus(Predicate(is_highlight)), 'book')
    groups = [html_elements[g['book'][0]:g['book'][1]] for g in finditer(regex, html_elements)]
    return [Book(group) for group in groups]


def justify(text, number_of_chars=70, bold_words=0):
    words = text.split()
    lines = []

    # Sum of word lengths plus number of spaces between them.
    line_length = lambda words: sum(map(len, words)) + len(words)

    cur_line = []
    for word in words:
        if line_length(cur_line + [word]) > number_of_chars:
            lines.append(cur_line)
            cur_line = [word]
        else:
            cur_line.append(word)
    if cur_line:
        lines.append(cur_line)
    if bold_words:
        formatted_lines = [
            ' '.join([TERM.bold(' '.join(lines[0][:bold_words])), *lines[0][bold_words:]]),
            *(' '.join(l) for l in lines[1:])
        ]
    else:
        formatted_lines = [' '.join(line) for line in lines]
    return '\n'.join(formatted_lines)


def indent(text, indent='    '):
    return '\n'.join(indent + line for line in text.split('\n'))
            

def construct_highlight_string(author, title, text, location):
        
    title, *subs = title.split(':')
    subtitle = ':'.join(subs).strip()
    title = TERM.bold(title)
    if subtitle:
        title += ':'
        subtitle = indent(justify(subtitle, number_of_chars=70-4))
        title = '\n'.join([title, subtitle])
    author_location = 'By {author} (Location: {location})'.format(
        author=TERM.bold(author),
        location=location,
    )
    ret = '{text}\n\n{title}\n{author_location}'.format(
        text=justify(text.strip(), bold_words=5),
        title=indent(title),
        author_location=indent(author_location)
    )
    return indent(ret)

def write_fortune_file(books):
    """
    Construct a datfile suitable for use with the `fortune` command.
    
    Based on:
    https://ubuntuforums.org/showthread.php?t=1343692&s=3adc5275d51d97464edba1dad8fa3092&p=8456253#post8456253
    """
    highlight_strings = [
        construct_highlight_string(
            author=book.author,
            title=book.title,
            text=highlight.text,
            location=highlight.location,
        ) for book in books for highlight in book.highlights
    ]
    formatted_highlights = '\n%\n'.join(highlight_strings)
    with open('./fortunes', 'wb') as f:
        f.write(formatted_highlights.encode('utf-8'))
        f.flush()
        outfile = './fortunes.dat'
        cmd = 'strfile -c % {f.name} {outfile}'.format(**locals())
        ret = os.system(cmd)
        assert ret == 0, ret
    return ret


if __name__ == '__main__':
    if os.path.isfile('./highlights.html.encrypted'):
        with open('./highlights.html', 'rb') as f:
            html = f.read()
        assert md5(html).hexdigest() == 'b3cf5c9761bb5c68bcc0cd6747902262'
    else:
        password = getpass()
        orig = ensure_encrypted_file_exists(password)
        html = get_decrypted_text(password)
        if orig and html:
            assert orig == html
        else:
            assert md5(html).hexdigest() == 'b3cf5c9761bb5c68bcc0cd6747902262'
    
    books = parse_highlights_html(html)
    write_fortune_file(books)
    
