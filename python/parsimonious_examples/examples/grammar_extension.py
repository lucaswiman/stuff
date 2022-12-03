# from parsimonious.grammar import TokenGrammar, RULES_SYNTAX as ORIG_RULES_SYNTAX, RuleVisitor, Grammar
#
# class ExtendedTokenRuleVisitor(RuleVisitor):
#     pass
#
#
# class TokenGrammar(Grammar):
#     """A Grammar which takes a list of pre-lexed tokens instead of text
#     This is useful if you want to do the lexing yourself, as a separate pass:
#     for example, to implement indentation-based languages.
#     """
#     def _expressions_from_rules(self, rules, custom_rules):
#         tree = rule_grammar.parse(rules)
#         return TokenRuleVisitor(custom_rules).visit(tree)
#
# rule_syntax = (r'''
#     # Ignored things (represented by _) are typically hung off the end of the
#     # leafmost kinds of nodes. Literals like "/" count as leaves.
#     rules = _ rule*
#     rule = label equals expression
#     equals = "=" _
#     literal = spaceless_literal _
#     # So you can't spell a regex like `~"..." ilm`:
#     spaceless_literal = ~"u?r?\"[^\"\\\\]*(?:\\\\.[^\"\\\\]*)*\""is /
#                         ~"u?r?'[^'\\\\]*(?:\\\\.[^'\\\\]*)*'"is
#     expression = ored / sequence / term
#     or_term = "/" _ term
#     ored = term or_term+
#     sequence = term term+
#     not_term = "!" term _
#     lookahead_term = "&" term _
#     quantified = atom quantifier
#     atom = reference / literal / regex / parenthesized
#     regex = "~" spaceless_literal ~"[ilmsuxa]*"i _
#     parenthesized = "(" _ expression ")" _
#     quantifier = ~"[*+?]" _
#     reference = label !equals
#     # A subsequent equal sign is the only thing that distinguishes a label
#     # (which begins a new rule) from a reference (which is just a pointer to a
#     # rule defined somewhere else):
#     label = ~"[a-zA-Z_][a-zA-Z_0-9]*" _
#     # _ = ~r"\s*(?:#[^\r\n]*)?\s*"
#     _ = meaninglessness*
#     meaninglessness = ~r"\s+" / comment
#     comment = ~r"#[^\r\n]*"
#
#     # New stuff
#     term = not_term / lookahead_term / qualified / quantified / atom
#     qualified = label "[" _ qualification _ "]" _
#     qualification = ("@" label _ "->" _ (spaceless_literal / regex))+
#     ''')
# FOO = Grammar(rule_syntax)
# FOO.parse(r"""
#     x = (y[@foo -> ~"(foo)*"] y[@bar -> "bar"])
#
# """)
#
#
#
# from dataclasses import dataclass
# @dataclass
# class Tok:
#     type: str
#
#
# TOK_EXAMPLE = TokenGrammar(r"""
#     foo = "bar" "baz"
# """)
# TOK_EXAMPLE.parse([Tok("bar"), Tok("baz")])
#
#
#
#

from enum import Enum
import regex as re
from parsimonious.expressions import Literal, Regex, Node, RegexNode
from parsimonious.utils import evaluate_string
from parsimonious.grammar import Grammar, RuleVisitor, rule_grammar

class CustomTokenMatcher(Literal):
    """An expression matching a single token of a given type
    This is for use only with TokenGrammars.
    """
    def _get_str(self, token) -> str:
        if isinstance(token, str):
            return token
        elif isinstance(token, Enum):
            return token.name
        else:
            # Assume .type is the relevant value (current behavior)
            return token.type

    def _uncached_match(self, token_list, pos, cache, error):
        token = token_list[pos]
        if self._get_str(token_list[pos]) == self.literal:
            return Node(self, token_list, pos, pos + 1)


class CustomTokenRegex(Regex):
    def _uncached_match(self, token_list, pos, cache, error):
        token = token_list[pos]
        if isinstance(token, type(self.re.pattern)) and (m:= self.re.fullmatch(token)):
            node = RegexNode(self, token_list, pos, pos + 1)
            node.match = m  # TODO: A terrible idea for cache size?
            return node


class CustomTokenGrammar(Grammar):
    def _expressions_from_rules(self, rules, custom_rules):
        tree = rule_grammar.parse(rules)
        return CustomTokenRuleVisitor(custom_rules).visit(tree)


class CustomTokenRuleVisitor(RuleVisitor):
    def visit_spaceless_literal(self, spaceless_literal, visited_children):
        return CustomTokenMatcher(evaluate_string(spaceless_literal.text))

    def visit_regex(self, node, regex):
        tilde, literal, flags, _ = regex
        flags = flags.text.upper()
        pattern = literal.literal  # Pull the string back out of the Literal
                                   # object.
        return CustomTokenRegex(pattern, ignore_case='I' in flags,
                              locale='L' in flags,
                              multiline='M' in flags,
                              dot_all='S' in flags,
                              unicode='U' in flags,
                              verbose='X' in flags,
                              ascii='A' in flags)

from enum import Enum
class Delimiters(Enum):
    DATA_SEP = 0
    REPEAT_SEP = 1
    SEG_TERM = 2
    COMPONENT_SEP = 3

def lex(data) -> list:
    data_elem_sep, repetition_sep, component_sep = (
        data[3], data[82], data[104]
    )
    # Allow multi-character segment terminators so the more
    # readable ~\n is valid. "GS" is always the second segment
    # of all x12 documents.
    seg_terminator = data[105: data.index(f'GS{data_elem_sep}', 105)]
    match_to_token_name = {
        data_elem_sep: Delimiters.DATA_SEP,
        repetition_sep: Delimiters.REPEAT_SEP,
        seg_terminator: Delimiters.SEG_TERM,
        component_sep: Delimiters.COMPONENT_SEP,
    }
    separator_re = re.compile(
        r"(\L<separators>)",
        separators=list(match_to_token_name),
    )
    prev_endpoint = 0
    tokens = []
    for match in separator_re.finditer(data):
        start, endpoint = match.span()
        # Everything between this endpoint and the last is a
        # value that contains data. Even zero-length elements
        # are meaningful.
        tokens.append(data[prev_endpoint:start])
        s = match.group()
        tokens.append(match_to_token_name[s])
        prev_endpoint = start + len(s)
    return tokens


x12 = """ISA*00*          *00*          *ZZ*EMEDNYBAT      *ZZ*ETIN           *100101*1000*^*00501*006000600*0*T*:~
GS*HP*EMEDNYBAT*ETIN*20100101*1050*6000600*X*005010X221A1~
ST*835*1740~
BPR*I*45.75*C*ACH*CCP*01*111*DA*33*1234567890**01*111*DA*22*20100101~
TRN*1*10100000000*1000000000~
REF*EV*ETIN~
DTM*405*20100101~
N1*PR*NYSDOH~
N3*OFFICE OF HEALTH INSURANCE PROGRAMS*CORNING TOWER, EMPIRE STATE PLAZA~
N4*ALBANY*NY*122370080~
PER*BL*PROVIDER SERVICES*TE*8003439000*UR*www.emedny.org~
N1*PE*MAJOR MEDICAL PROVIDER*XX*9999999995~
REF*TJ*000000000~
LX*1~
CLP*PATIENT ACCOUNT NUMBER*1*34.25*34.25**MC*1000210000000030*11~
NM1*QC*1*SUBMITTED LAST*SUBMITTED FIRST****MI*LL99999L~
NM1*74*1*CORRECTED LAST*CORRECTED FIRST~
REF*EA*PATIENT ACCOUNT NUMBER~
DTM*232*20100101~
DTM*233*20100101~
AMT*AU*34.25~
SVC*HC:V2020:RB*6*6**1~
DTM*472*20100101~
AMT*B6*6~
SVC*HC:V2700:RB*2.75*2.75**1~
DTM*472*20100101~
AMT*B6*2.75~
SVC*HC:V2103:RB*5.5*5.5**1~
DTM*472*20100101~
AMT*B6*5.5~
SVC*HC:S0580*20*20**2~
DTM*472*20100101~
AMT*B6*20~
CLP*PATIENT ACCOUNT NUMBER*2*34*0**MC*1000220000000020*11~
NM1*QC*1*SUBMITTED LAST*SUBMITTED FIRST****MI*LL88888L~
NM1*74*1*CORRECTED LAST*CORRECTED FIRST~
REF*EA*PATIENT ACCOUNT NUMBER~
DTM*232*20100101~
DTM*233*20100101~
SVC*HC:V2020*12*0**0~
DTM*472*20100101~
CAS*CO*29*12~
SVC*HC:V2103*22*0**0~
DTM*472*20100101~
CAS*CO*29*22~
CLP*PATIENT ACCOUNT NUMBER*2*34.25*11.5**MC*1000230000000020*11~
NM1*QC*1*SUBMITTED LAST*SUBMITTED FIRST****MI*LL77777L~
NM1*74*1*CORRECTED LAST*CORRECTED FIRST~
REF*EA*PATIENT ACCOUNT NUMBER~
DTM*232*20100101~
DTM*233*20100101~
AMT*AU*11.5~
SVC*HC:V2020:RB*6*6**1~
DTM*472*20100101~
AMT*B6*6~
SVC*HC:V2103:RB*5.5*5.5**1~
DTM*472*20130917~
AMT*B6*5.5~
SVC*HC:V2700:RB*2.75*0**0~
DTM*472*20100101~
CAS*CO*251*2.75~
LQ*HE*N206~
SVC*HC:S0580*20*0**0~
DTM*472*20100101~
CAS*CO*251*20~
LQ*HE*N206~
SE*65*1740~
GE*1*6000600~
IEA*1*006000600~"""

tokens = lex(x12)
# Page 65 of 835 spec
x12_835_grammar = CustomTokenGrammar(r"""
    x12_doc = header transaction_set footer
    header = ISA GS
    footer = GE IEA
    transaction_set = transaction_header loop_1000* transaction_summary
    transaction_header = ST BPR NTE* TRN? CUR? REF* DTM*  # TODO: REF/DTM should be more specific
    loop_1000 = N1 N2* N3* N4? REF* PER* RDM? DTM? loop_2000*
    loop_2000 = LX TS3? TS2? loop_2100*
    loop_2100 = CLP CAS* NM1+ MIA? MOA? REF* DTM* PER* AMT* QTY* loop_2110*
    loop_2110 = SVC DTM* CAS* REF* AMT* QTY* LQ*
    transaction_summary = PLB* SE
    seg_data = ("DATA_SEP" / "REPEAT_SEP" / "COMPONENT_SEP" / ~".*")* "SEG_TERM"
    ISA = "ISA" seg_data
    GS = "GS" seg_data
    GE = "GE" seg_data
    IEA = "IEA" seg_data
    ST = "ST" seg_data
    BPR = "BPR" seg_data
    NTE = "NTE" seg_data
    TRN = "TRN" seg_data
    CUR = "CUR" seg_data
    REF = "REF" seg_data
    DTM = "DTM" seg_data
    N1 = "N1" seg_data
    N2 = "N2" seg_data
    N3 = "N3" seg_data
    N4 = "N4" seg_data
    REF = "REF" seg_data
    PER = "PER" seg_data
    RDM = "RDM" seg_data
    DTM = "DTM" seg_data
    LX = "LX" seg_data
    TS3 = "TS3" seg_data
    TS2 = "TS2" seg_data
    CLP = "CLP" seg_data
    CAS = "CAS" seg_data
    NM1 = "NM1" seg_data
    MIA = "MIA" seg_data
    MOA = "MOA" seg_data
    REF = "REF" seg_data
    DTM = "DTM" seg_data
    PER = "PER" seg_data
    AMT = "AMT" seg_data
    QTY = "QTY" seg_data
    SVC = "SVC" seg_data
    DTM = "DTM" seg_data
    CAS = "CAS" seg_data
    REF = "REF" seg_data
    AMT = "AMT" seg_data
    QTY = "QTY" seg_data
    LQ = "LQ" seg_data
    PLB = "PLB" seg_data
    SE = "SE" seg_data
""")
x12_835_grammar.parse(tokens)