#!/usr/bin/env python
from __future__ import division, print_function
import argparse
import traceback
import permutations
import z3


def fract(x, y, k, n, o, z):
    if k == 0:
        return []
    n2 = n // 2
    k2 = k // 2
    return (
        fract(x, y, k - 1, n2, o, z + 1) +
        fract(x, y, k - 1, n2, o + n2, z + 1) +
        [z3.Distinct(*[x[i] >> z for i in range(o, o + n)]),
         z3.Distinct(*[y[i] >> z for i in range(o, o + n)])] +
        ([z3.Distinct(*[((x[i] >> (z + k - k2)) << k2) + (y[i] >> (z + k - k2)) for i in range(o, o + n)])]
         if k % 2 == 0 else []))


def fractz3(k, use_hammersley=False, seed=-1):
    if k == 0:
        return
    n = 2 ** k
    x = [z3.BitVec('x__{}'.format(i), k) for i in range(n)]
    y = [z3.BitVec('y__{}'.format(i), k) for i in range(n)]
    cond = fract(x, y, k, n, 0, 0)

    # Fix x to be hammersley or have z3 figure an x for us
    if use_hammersley:
        hamm = permutations.hammersley(k)
        cond.extend([x[i] == hamm[i] for i in range(n)])

    if seed >= 0:
        z3.set_param('auto_config', False)
        z3.set_param('smt.phase_selection', 5)
        z3.set_param('smt.random_seed', seed)

    # Solve
    print('Solving fractz3({}): {} conditions, hold tight..'.format(k, len(cond)))
    s = z3.Solver()
    s.push()  # The above `z3.set_param`s don't work without this push
    s.add(*cond)
    print(s.check())
    try:
        m = s.model()
        xx = [m.evaluate(m[i]).as_long() for i in x]
        yy = [m.evaluate(m[i]).as_long() for i in y]
        print('x: {}'.format(xx))
        print('y: {}'.format(yy))
        print('is_fractal(x): {}'.format(permutations.is_fractal(xx)))
        print('is_fractal(y): {}'.format(permutations.is_fractal(yy)))
        print('is_perfect(x, y): {}'.format(permutations.is_perfect(k, xx, yy)))
    except:
        traceback.print_exc()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('k', type=int, nargs='?', default=6)
    parser.add_argument('--seed', type=int, default=-1)
    parser.add_argument('--hammersley', action='store_const', const=True, default=False)
    args = parser.parse_args()
    fractz3(args.k, use_hammersley=args.hammersley, seed=args.seed)
