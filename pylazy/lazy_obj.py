class LazyObjMeta(type):
    _special_names = [
        '__abs__', '__add__', '__and__', '__cmp__', '__coerce__',
        '__contains__', '__delitem__', '__delslice__', '__div__', '__divmod__',
        '__eq__', '__float__', '__floordiv__', '__ge__', '__getitem__',
        '__getslice__', '__gt__', '__hash__', '__hex__', '__iadd__', '__iand__',
        '__idiv__', '__idivmod__', '__ifloordiv__', '__ilshift__', '__imod__',
        '__imul__', '__int__', '__invert__', '__ior__', '__ipow__', '__irshift__',
        '__isub__', '__iter__', '__itruediv__', '__ixor__', '__le__', '__len__',
        '__long__', '__lshift__', '__lt__', '__mod__', '__mul__', '__ne__',
        '__neg__', '__oct__', '__or__', '__pos__', '__pow__', '__radd__',
        '__rand__', '__rdiv__', '__rdivmod__', '__reduce__', '__reduce_ex__',
        '__repr__', '__reversed__', '__rfloorfiv__', '__rlshift__', '__rmod__',
        '__rmul__', '__ror__', '__rpow__', '__rrshift__', '__rshift__', '__rsub__',
        '__rtruediv__', '__rxor__', '__setitem__', '__setslice__', '__sub__',
        '__truediv__', '__xor__', 'next', '__getitem__', '__setitem__', '__rcmp__',
        '__unicode__', '__get__', '__set__', '__delete__',
        '__instancecheck__', '__subclasscheck__', '__call__', '__index__', '__enter__', '__exit__'
    ]

    def __new__(cls, cls_name, bases, attrs):
        def make_method(name):
            def method(self, *args, **kw):
                self._exe()
                obj = super(LazyObj, self).__getattribute__('_obj')
                if hasattr(obj, name):
                    return getattr(obj, name)(*args, **kw)
                else:
                    raise AttributeError('"%s"(%s) object has no attribute "%s"' % (str(obj), str(type(obj)), name))
            return method
        for i in cls._special_names:
            attrs[i] = make_method(i)
        self = super(LazyObjMeta, cls).__new__(cls, cls_name, bases, attrs)
        return self


class LazyObj(object):
    __metaclass__ = LazyObjMeta
    _lazy_obj_attr = ['__new__', "_obj", "__weakref__", "_func", "_args", "_kwargs", "_executed", "_exe", '_make_method', '_special_names']

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._obj = None
        self._executed = False
        self._args = args
        self._kwargs = kwargs

    def __delattr__(self, name):
        self._exe()
        delattr(self._obj, name)

    def __setattr__(self, name, value):
        if name in super(LazyObj, self).__getattribute__('_lazy_obj_attr'):
            super(LazyObj, self).__setattr__(name, value)
            return
        self._exe()
        setattr(self._obj, name, value)

    def __nonzero__(self):
        return bool(self._obj)

    def __str__(self):
        self._exe()
        return str(self._obj)

    def _exe(self):
        if self._executed:
            return
        result = self._func(*self._args, **self._kwargs)
        self._obj = result
        self._executed = True

    def __getattribute__(self, name):
        if name in super(LazyObj, self).__getattribute__('_lazy_obj_attr'):
            return super(LazyObj, self).__getattribute__(name)
        self._exe()
        return getattr(self._obj, name)

    def __getattr__(self, name):
        if name in super(LazyObj, self).__getattr__('_lazy_obj_attr'):
            return super(LazyObj, self).__getattr__(name)
        self._exe()
        return getattr(self._obj, name)
