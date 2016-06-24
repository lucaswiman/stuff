from peak.util.proxies import ObjectWrapper
class StringWrapper(ObjectWrapper):
    wrapped = None
    def __init__(self, obj):
        super(StringWrapper, self).__init__(obj)
        self.wrapped = obj
    def __unicode__(self):
        return u'Wrapped: %s' % self.wrapped
    def __str__(self):
        return 'Wrapped: %s' % self.wrapped


if __name__ == '__main__':
    print '(%s)' % StringWrapper('foo')


class NameWrapper(ObjectWrapper):
    name = None
    def __init__(self, ob, name):
        ObjectWrapper.__init__(self, ob)
        self.name = name
    def __str__(self):
        return self.name

print NameWrapper('foo', 'bar')
print '' + NameWrapper('foo', 'bar')