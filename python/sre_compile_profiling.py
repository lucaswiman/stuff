import re

regexps = [
    re.compile(r'^((?:19|20)\d\d)[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$'),  # http://www.regular-expressions.info/dates.html
    re.compile(r'^(?=[A-Z0-9][A-Z0-9@._%+-]{5,253}$)[A-Z0-9._%+-]{1,64}@(?:(?=[A-Z0-9-]{1,63}\.)[A-Z0-9]+(?:-[A-Z0-9]+)*\.){1,8}[A-Z]{2,63}$'),  # http://www.regular-expressions.info/email.html
    re.compile(r'a' * 100000),
    re.compile(r'\$' * 100000),
    re.compile((r'a' * 100000) + (r'\$' * 100000)),
]