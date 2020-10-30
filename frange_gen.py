def frange(end, *args): # noqa
    step = 1.0
    start = 0.0
    if len(args) == 0:
        i = start
        while i < end:
            yield i
            i += step
    elif len(args) == 1:
        i = end
        end = args[0]
        while i < end:
            yield i
            i += step
    elif len(args) == 2:
        if args[1] == 0:
            raise ValueError('frange() arg 3 must not be zero') # noqa
        elif args[1] > 0:
            i = end
            end = args[0]
            while i < end:
                yield i
                i += args[1]
        elif args[1] < 0:
            i = end
            end = args[0]
            while i > end:
                yield i
                i += args[1]
    elif len(args) > 2:
        raise AttributeError('there should be 3 parameters maximum')


for i in frange(1, 100, 3.5):
    print(i)
