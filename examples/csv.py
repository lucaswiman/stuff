"""
Parsimonious grammar for the the CSV file format (RFC 4180), with the grammar
adapted from https://gist.github.com/mnzk/5426024
The original BNF grammar is here:

    file = [header CRLF] record (CRLF record)* [CRLF]
    header = name (COMMA name)*
    record = field (COMMA field)*
    name = field
    field = (escaped | non-escaped)
    escaped = DQUOTE (TEXTDATA | COMMA | CR | LF | 2DQUOTE)* DQUOTE
    2DQUOTE = DQUOTE DQUOTE
    non-escaped = TEXTDATA*
    COMMA = '\u002C'
    CR = '\u000D'
    DQUOTE = '\u0022'
    LF = '\u000A'
    CRLF = CR LF
    TEXTDATA = #'[\u0020-\u0021\u0023-\u002B\u002D-\u007E]'
"""
from __future__ import print_function

from parsimonious.grammar import Grammar

from . import run_examples

CSV_RAW_GRAMMAR = ur"""
    file = (header CRLF)? record (CRLF record)* CRLF?
    header = name (COMMA name)*
    record = field (COMMA field)*
    name = field
    field = escaped / non_escaped
    escaped = DQUOTE (TEXTDATA / COMMA / CR / LF / TWODQUOTE)* DQUOTE
    
    TWODQUOTE = DQUOTE DQUOTE
    non_escaped = TEXTDATA*
    COMMA = "\u002C"
    CR = "\r"
    DQUOTE = "\""
    LF = "\n"
    CRLF = CR LF
    TEXTDATA = ~"[\u0020-\u0021\u0023-\u002B\u002D-\u007E]"
"""

CSV = Grammar(CSV_RAW_GRAMMAR)

CSV_EXAMPLES = (
    '',
    ',',
    ',\r\n',
    ',\r\n,,',
    '\r\n',
    '"\r\n"""'
    '","""'
)

CSV_NON_EXAMPLES = (
    ',",',
    '\x00',
)
