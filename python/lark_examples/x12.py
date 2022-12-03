from typing import *
from lark import Lark
from lark.lexer import Lexer, LexerState, Token
import regex as re

flags = re.MULTILINE | re.DOTALL | re.VERBOSE, re.V1

class X12Lexer(Lexer):
    def __init__(self, lexer_conf):
        pass
    def lex(self, data) -> Iterator[Token]:
        data_elem_sep, repetition_sep, component_sep = (
            data[3], data[82], data[104]
        )
        # Allow multi-character segment terminators so the more
        # readable ~\n is valid. "GS" is always the second segment
        # of all x12 documents.
        seg_terminator = data[105: data.index(f'GS{data_elem_sep}', 105)]
        match_to_token_name = {
            data_elem_sep: "DATA_SEP",
            repetition_sep: "REPEAT_SEP",
            seg_terminator: "SEG_TERM",
            component_sep: "COMPONENT_SEP",
        }
        separator_re = re.compile(
            r"(\L<separators>)",
            separators=list(match_to_token_name),
        )
        prev_endpoint = 0
        for match in separator_re.finditer(data):
            start, endpoint = match.span()
            # Everything between this endpoint and the last is a
            # value that contains data. Even zero-length elements
            # are meaningful.
            yield Token(
                "VALUE", data[prev_endpoint:start], start_pos=prev_endpoint, end_pos=start,
            )
            s = match.group()
            yield Token(
                match_to_token_name[s], s, start_pos=start, end_pos=endpoint,
            )
            prev_endpoint = start + len(s)

l_custom = Lark("""
    start: isa segment+
    isa: "ISA" (DATA_SEP seg_data)* SEG_TERM
    segment: segment_id (DATA_SEP seg_data)* SEG_TERM
    segment_id: VALUE
    seg_data: data_elem (REPEAT_SEP data_elem)*
    data_elem: VALUE (COMPONENT_SEP VALUE)*
    %declare SEGMENT_ID DATA_SEP SEG_TERM REPEAT_SEP COMPONENT_SEP VALUE
    %ignore COMPONENT_SEP
""", lexer=X12Lexer)
x12_example = """ISA*00*          *00*          *ZZ*EMEDNYBAT      *ZZ*ETIN           *100101*1000*^*00501*006000600*0*T*:~GS*HP*EMEDNYBAT*ETIN*20100101*1050*6000600*X*005010X221A1~ST*835*1740~BPR*I*45.75*C*ACH*CCP*01*111*DA*33*1234567890**01*111*DA*22*20100101~TRN*1*10100000000*1000000000~REF*EV*ETIN~DTM*405*20100101~N1*PR*NYSDOH~N3*OFFICE OF HEALTH INSURANCE PROGRAMS*CORNING TOWER, EMPIRE STATE PLAZA~N4*ALBANY*NY*122370080~PER*BL*PROVIDER SERVICES*TE*8003439000*UR*www.emedny.org~N1*PE*MAJOR MEDICAL PROVIDER*XX*9999999995~REF*TJ*000000000~LX*1~CLP*PATIENT ACCOUNT NUMBER*1*34.25*34.25**MC*1000210000000030*11~NM1*QC*1*SUBMITTED LAST*SUBMITTED FIRST****MI*LL99999L~NM1*74*1*CORRECTED LAST*CORRECTED FIRST~REF*EA*PATIENT ACCOUNT NUMBER~DTM*232*20100101~DTM*233*20100101~AMT*AU*34.25~SVC*HC:V2020:RB*6*6**1~DTM*472*20100101~AMT*B6*6~SVC*HC:V2700:RB*2.75*2.75**1~DTM*472*20100101~AMT*B6*2.75~SVC*HC:V2103:RB*5.5*5.5**1~DTM*472*20100101~AMT*B6*5.5~SVC*HC:S0580*20*20**2~DTM*472*20100101~AMT*B6*20~CLP*PATIENT ACCOUNT NUMBER*2*34*0**MC*1000220000000020*11~NM1*QC*1*SUBMITTED LAST*SUBMITTED FIRST****MI*LL88888L~NM1*74*1*CORRECTED LAST*CORRECTED FIRST~REF*EA*PATIENT ACCOUNT NUMBER~DTM*232*20100101~DTM*233*20100101~SVC*HC:V2020*12*0**0~DTM*472*20100101~CAS*CO*29*12~SVC*HC:V2103*22*0**0~DTM*472*20100101~CAS*CO*29*22~CLP*PATIENT ACCOUNT NUMBER*2*34.25*11.5**MC*1000230000000020*11~NM1*QC*1*SUBMITTED LAST*SUBMITTED FIRST****MI*LL77777L~NM1*74*1*CORRECTED LAST*CORRECTED FIRST~REF*EA*PATIENT ACCOUNT NUMBER~DTM*232*20100101~DTM*233*20100101~AMT*AU*11.5~SVC*HC:V2020:RB*6*6**1~DTM*472*20100101~AMT*B6*6~SVC*HC:V2103:RB*5.5*5.5**1~DTM*472*20130917~AMT*B6*5.5~SVC*HC:V2700:RB*2.75*0**0~DTM*472*20100101~CAS*CO*251*2.75~LQ*HE*N206~SVC*HC:S0580*20*0**0~DTM*472*20100101~CAS*CO*251*20~LQ*HE*N206~SE*65*1740~GE*1*6000600~IEA*1*006000600~"""
tree = l_custom.parse(x12_example)

