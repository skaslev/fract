from random import random


# Basic test whether p is fractal permutation. It may also be used as a
# definition for fractal permutation.
def is_fractal(p):
    n = len(p)
    if n == 1:
        return p == [0]
    return (
        set(p) == set(range(n)) and
        is_fractal([x//2 for x in p[:n//2]]) and
        is_fractal([x//2 for x in p[n//2:]]))


# Fractal permutations

# fp_rec and fp give the number of fractal permutations of 2**k elements. The
# difference between the them is that fp_rec is recursive, while fp uses closed
# formula.
def fp_rec(k):
    if k == 0:
        return 1
    return 2 ** (2 ** (k - 1)) * fp_rec(k - 1) ** 2


def fp(k):
    return 2 ** (k * (2 ** (k - 1)))


# Same as fp and fp_rec, but return only the exponent, that is log(fp(k)).
def log_fp_rec(k):
    if k == 0:
        return 0
    return 2 ** (k - 1) + 2 * log_fp_rec(k-1)


def log_fp(k):
    return k * (2 ** (k - 1))


def random_bit():
    return 0 if random() < 0.5 else 1


# Generates a random fractal permutation with 2**k elements
def random_fractal(k):
    if k == 0:
        return [0]
    bits = [random_bit() for i in range(1 << (k - 1))]
    return (
        [(i << 1) | bits[i]        for i in random_fractal(k-1)] +
        [(i << 1) | (~bits[i] & 1) for i in random_fractal(k-1)])


# Also, hammersley(k) == xfractal(k).next(). In other words hammersley
# is the first fractal permutation yielded by xfractal
def hammersley(k):
    if k == 0:
        return [0]
    hamm = hammersley(k - 1)
    return [(i << 1) | 0 for i in hamm] + [(i << 1) | 1 for i in hamm]


# xfractal generates all fractal permutations of 2**k elements.
# Also, len(list(xfractal(k))) == fp(k) is true for all k.
def xfractal(k):
    if k == 0:
        yield [0]
    else:
        bits, max_bits, = 0, 2 ** (2 ** (k - 1))
        while bits < max_bits:
            for left in xfractal(k - 1):
                for right in xfractal(k - 1):
                    yield (
                        [(i << 1) | ((bits >> i) & 1)  for i in left] +
                        [(i << 1) | (~(bits >> i) & 1) for i in right])
            bits += 1


# Fractal* permutations

# The same functionality as before, but for fractal* permutations.
def fp_star_rec(k):
    if k == 0:
        return 1
    return 2 * fp_star_rec(k - 1) ** 2


def fp_star(k):
    return 2 ** (2 ** k - 1)


def log_fp_star(k):
    return 2 ** k - 1


# Again, len(list(xfractal_star(k))) == fp_star(k) is true for all k.
def xfractal_star(k):
    if k == 0:
        yield [0]
    else:
        for bit in range(2):
            for left in xfractal_star(k - 1):
                for right in xfractal_star(k - 1):
                    yield (
                        [(i << 1) | (bit & 1)  for i in left] +
                        [(i << 1) | (~bit & 1) for i in right])


def get_bit(n, i):
    return (n & (1 << i)) >> i


# fp_star_oracle(k,n) returns the n-th fractal* permutation with 2**k elements.
# Also,
# [fp_star_oracle(k,n) for n in range(fp_star(k))] == list(xfractal_star(k))
# is true for all k.
def fp_star_oracle(k, n):
    if k == 0:
        return [0]
    bit = get_bit(n, log_fp_star(k) - 1)
    left_n, right_n = divmod(n, fp_star(k-1))
    left, right = fp_star_oracle(k-1, left_n), fp_star_oracle(k-1, right_n)
    return (
        [(i << 1) | (bit & 1)  for i in left] +
        [(i << 1) | (~bit & 1) for i in right])


# Given a fractal* permutation of 2**k elements fp_star_oracle_inv returns it's
# subsequent number.
# That is:
# fp_star_oracle_inv(k, fp_star_oracle(k, n)) == n
# for all k and n <- [0..fp_star(k))
def fp_star_oracle_inv(k, p):
    if k == 0:
        return 0
    bit = p[0] % 2
    left  = fp_star_oracle_inv(k-1, [p[i] >> 1 for i in range(2**(k-1))])
    right = fp_star_oracle_inv(k-1, [p[i] >> 1 for i in range(2**(k-1), 2**k)])
    return bit * (1 << (log_fp_star(k) - 1)) + fp_star(k-1) * left + right


def is_perfect(k, x, y):
    assert len(x) == (1 << k) and len(y) == (1 << k)
    if k == 0:
        return x == [0] and y == [0]
    # Fractality check
    if set(x) != set(range(1 << k)) or set(y) != set(range(1 << k)):
        return False
    if k % 2 == 0:
        bucket_bits = k // 2
        bucket_points = 1
    else:
        bucket_bits = (k - 1) // 2
        bucket_points = 2
    buckets = {}
    for i in range(1 << k):
        b = ((x[i] >> (k - bucket_bits)) << bucket_bits) | (y[i] >> (k - bucket_bits))
        buckets[b] = buckets.setdefault(b, 0) + 1
    if len(buckets) != 1 << (2 * bucket_bits):
        return False
    if not all(v == bucket_points for v in buckets.values()):
        return False
    return (
        is_perfect(k-1, [i >> 1 for i in x[:(1 << (k-1))]], [i >> 1 for i in y[:(1 << (k-1))]]) and
        is_perfect(k-1, [i >> 1 for i in x[(1 << (k-1)):]], [i >> 1 for i in y[(1 << (k-1)):]]))
