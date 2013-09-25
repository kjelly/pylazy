from pylazy import lazy_eval

@lazy_eval
def retrun_dict():
    print 'run'
    return {'a': 1, 'b': 2,}


a = retrun_dict()
print 'lazy'
print a['a']