from __future__ import unicode_literals

import os
from collections import namedtuple
from decimal import Decimal
from datetime import date, datetime

namedtuple('T', [])

print(date(2017, 1, 26).strftime('%Y-%m-%d'))
print(datetime.strptime('2017-01-26', '%Y-%m-%d'))

Decimal('1.0')
Decimal(str('1.0'))