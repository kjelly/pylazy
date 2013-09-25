from pylazy import lazy_eval


class MyCls(object):
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return str(self.data)

    @lazy_eval
    def __add__(self, another):
        print 'add'
        return self.__class__(self.data + another.data)


a = MyCls(5)
b = MyCls(3)
c = a + b
print "lazy"
print c
c.data = 5
print c
