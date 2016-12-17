from time import clock


def time_it(f, *args, **kwargs):
    t0 = clock()
    res = f(*args, **kwargs)
    dt = clock() - t0
    return res, dt
