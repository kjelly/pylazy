from lazy_obj import LazyObj


def lazy_eval(func):
    def inner(*args, **kwargs):
        return LazyObj(func, *args, **kwargs)
    return inner
