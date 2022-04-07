from lark import Lark

l = Lark('''
  start: bar+
  bar: /a|b|c*/ "foo"
''')

l.parse('afoobfooccfoo')

l2 = Lark('''
  start: "bar"+
''')
l2.parse('barbarbar')
