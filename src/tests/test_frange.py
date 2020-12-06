from testify.tests.test_base import TestCaseBase


def frange_gen(start, stop=None, step=None):
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


class frange_iter(object): # noqa
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


class TestFrange(TestCaseBase):

    def tests_frange_gen(self):

        assert list(frange_gen(1, 20, 3.5)) == [1, 4.5, 8.0, 11.5, 15.0, 18.5]
        assert list(frange_gen(20, 1, -3.5)) == [20, 16.5, 13.0, 9.5, 6.0, 2.5]
        assert list(frange_gen(10)) == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        assert list(frange_gen(-5, 5)) == [-5, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0]
        assert list(frange_gen(20, 10)) == []
        assert list(frange_gen(-20, -10)) == [-20, -19.0, -18.0, -17.0, -16.0, -15.0, -14.0, -13.0, -12.0, -11.0]
        assert list(frange_gen(10, 20, -2.5)) == []
        assert list(frange_gen(0.5, 0.5, 0.5)) == []

    def tests_frange_iter(self):

        assert list(frange_iter(1, 20, 3.5)) == [1, 4.5, 8.0, 11.5, 15.0, 18.5]
        assert list(frange_iter(20, 1, -3.5)) == [20, 16.5, 13.0, 9.5, 6.0, 2.5]
        assert list(frange_iter(10)) == [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
        assert list(frange_iter(-5, 5)) == [-5, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0]
        assert list(frange_iter(20, 10)) == []
        assert list(frange_iter(-20, -10)) == [-20, -19.0, -18.0, -17.0, -16.0, -15.0, -14.0, -13.0, -12.0, -11.0]
        assert list(frange_iter(10, 20, -2.5)) == []
        assert list(frange_iter(0.5, 0.5, 0.5)) == []
