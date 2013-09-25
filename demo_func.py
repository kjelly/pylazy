from pylazy import lazy_eval


def add(a, b):
    print 'add'
    return a + b


a = 5
b = 3
c = add(a, b)
print "lazy"
print c

print '--------------------'

a = 1
b = 2
add = lazy_eval(add)
c = add(a, b)
print "lazy"
print c
