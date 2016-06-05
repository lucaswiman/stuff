"""
Parsimonious grammar for the ISO 8601 timestamp format based on the ABNF
grammar from section 5.6 of RFC 3339: https://www.ietf.org/rfc/rfc3339.txt
The original ABNF grammar is here:

    date-fullyear   = 4DIGIT
    date-month      = 2DIGIT  ; 01-12
    date-mday       = 2DIGIT  ; 01-28, 01-29, 01-30, 01-31 based on
                              ; month/year
    time-hour       = 2DIGIT  ; 00-23
    time-minute     = 2DIGIT  ; 00-59
    time-second     = 2DIGIT  ; 00-58, 00-59, 00-60 based on leap second
                              ; rules
    time-secfrac    = "." 1*DIGIT
    time-numoffset  = ("+" / "-") time-hour ":" time-minute
    time-offset     = "Z" / time-numoffset

    partial-time    = time-hour ":" time-minute ":" time-second
                      [time-secfrac]
    full-date       = date-fullyear "-" date-month "-" date-mday
    full-time       = partial-time time-offset

    date-time       = full-date "T" full-time
"""
from __future__ import print_function

from parsimonious.grammar import Grammar

from . import run_examples

ISO8601_RAW_GRAMMAR = r"""
    date_time       = full_date "T" full_time

    full_time       = partial_time time_offset
    year_month      = date_fullyear "-" date_month
    full_date       = year_month "-" date_mday
    partial_time    = time_hour ":" time_minute ":" time_second time_secfrac?

    time_offset     = "Z" / time_numoffset
    time_numoffset  = ("+" / "-") time_hour ":" time_minute
    time_secfrac    = "." ~"[0-9]*"
    time_second     = ~"[0-5][0-9]|60"  # 60 included to allow for leap seconds
    time_minute     = ~"[0-5][0-9]"
    time_hour       = ~"[01][0-9]|2[0-3]"
    date_mday       = ~"0[1-9]|[12][0-9]|3[0-1]"
    date_month      = ~"0[1-9]|1[0-2]"
    date_fullyear   = ~"\d{4}"
"""

ISO8601 = Grammar(ISO8601_RAW_GRAMMAR)

ISO8601_EXAMPLES = (
    '1997-07-16T19:20:30.45+01:00',
    '1997-07-16T19:20:30+01:00',
    '2015-09-05T14:28:23.412175Z',
)

ISO8601_NON_EXAMPLES = (
    '1997-07-16T19:20:61.45+01:00',
    '1997-07-16',
)


if __name__ == "__main__":
    run_examples(ISO8601, ISO8601_EXAMPLES, ISO8601_NON_EXAMPLES)
