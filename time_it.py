from time import perf_counter


def time_it(f, *args, **kwargs):
    t0 = perf_counter()
    res = f(*args, **kwargs)
    dt = perf_counter() - t0
    return res, dt
