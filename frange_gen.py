# def frange(end, *args): # noqa
#     step = 1.0
#     start = 0.0
#     if len(args) == 0:
#         i = start
#         while i < end:
#             yield i
#             i += step
#     elif len(args) == 1:
#         i = end
#         end = args[0]
#         while i < end:
#             yield i
#             i += step
#     elif len(args) == 2:
#         if args[1] == 0:
#             raise ValueError('frange() arg 3 must not be zero') # noqa
#         elif args[1] > 0:
#             i = end
#             end = args[0]
#             step = args[1]
#             while i < end:
#                 yield i
#                 i += step
#         elif args[1] < 0:
#             i = end
#             end = args[0]
#             step = args[1]
#             while i > end:
#                 yield i
#                 i += step
#     elif len(args) > 2:
#         raise AttributeError('there should be 3 parameters maximum')
#
#
# for i in frange(1, 100, 3.5):
#     print(i)


def frange(start, stop=None, step=None):
    if stop is None:
        i = 0.0
        stop = start
        step = 1.0
    elif step is None:
        i = start
        stop = stop
        step = 1.0
    else:
        i = start
        stop = stop
        step = step
    while i < stop and step > 0 or i > stop and step < 0:
        yield i
        i += step


# for i in frange(1, 100, 3.5):
#     print(i)
#
# for i in frange(100, 1, -3.5):
#     print(i)
#
# for i in frange(10):
#     print(i)
#
# for i in frange(-10, 10):
#     print(i)
#
# for i in frange(100, 10):
#     print(i)
#
# for i in frange(-20, -10):
#     print(i)
#
# for i in frange(10, 20, -2.5):
#     print(i)
#
# for i in frange(0.5, 0.5, 0.5):
#     print(i)
