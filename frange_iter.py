class frange(object): # noqa
    def __init__(self, start, stop=None, step=None):
        if stop is None:
            self.i = 0.0
            self.stop = start
            self.step = 1.0
        elif step is None:
            self.i = start
            self.stop = stop
            self.step = 1.0
        else:
            self.i = start
            self.stop = stop
            self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.stop and self.step > 0 or self.i > self.stop and self.step < 0:
            self.i += self.step
            return self.i - self.step
        else:
            raise StopIteration


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
