#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include "fract_seed.h.ham"

/* fract_seed.h defines:
 * K		log(N)
 * N		number of points per sequence
 * XS		Hammersley's permutation of N elements
 * YS		pre-computed fractal permutations matching with Hammersley(K)
 * YSEEDS	number of permutations that YS contains
 */

/* The quality of the sequences generated doesn't depend much on the RNG used,
 * so feel free to plug your favourite here.
 * Also note that those two funcitons are the only source of nondeterminism.
 * rand_bit	returns 0 or 1 (may also be defined as rand_range(2))
 * rand_range	returns random number in [0,max)
 */
static inline int rand_bit() { return rand() > RAND_MAX / 2; }
static inline int rand_range(int max) { return (int) ((double) max * rand() / (RAND_MAX + 1.0)); }

/* Makes random swaps over the permutation xs which keep it's fractality. It
 * only affects the lower K/2 bits of xs elements, so it doesn't degrade the
 * discrepancy.
 * The complexity of the algorithm is O(N log(N)).
 */
static void jumble(uint16_t *xs)
{
	uint16_t inv[N/2];
	for (int i = 0; i < K/2; i++) {
		int length = 1 << (K - i), q = 1 << (i + 1);
		for (int offset = 0; offset < N; offset += length) {
			for (int j = offset; j < offset + length/2; j++)
				inv[xs[j] / q] = j;

			for (int j = offset + length/2; j < offset + length; j++)
				if (rand_bit()) {
					int j2 = inv[xs[j] / q];
					uint16_t tmp = xs[j];
					xs[j] = xs[j2];
					xs[j2] = tmp;
				}
		}
	}
}

static void reverse(uint16_t *arr, int length)
{
	uint16_t *a = arr, *b = a + length - 1;
	while (a < b) {
		uint16_t tmp = *a;
		*a++ = *b;
		*b-- = tmp;
	}
}

/* Makes random reverses over xs and ys. It keeps the points untouched and
 * chages only their order while keeping xs and ys fractal.
 * The complexity is O(N log(N)).
 *
 * NOTE: faster algorithm may be applied exploiting that reverse(reverse(x)) = x
 */
static void reorder(uint16_t *xs, uint16_t *ys)
{
	for (int length = N; length > 1; length /= 2)
		for (int offset = 0; offset < N; offset += length)
			if (rand_bit()) {
				reverse(xs + offset, length);
				reverse(ys + offset, length);
			}
}

struct fract {
	int nseq;
	uint16_t *xs, *ys;
};

struct fract *fract_init(int nseq)
{
	struct fract *fract = malloc(sizeof(*fract));
	fract->nseq = nseq;
	fract->xs = malloc(2 * nseq * N * sizeof(uint16_t));
	fract->ys = fract->xs + nseq * N;

	for (int i = 0; i < nseq; i++) {
		int yseed = rand_range(YSEEDS);
		uint16_t *xx = fract->xs + i * N;
		uint16_t *yy = fract->ys + i * N;
		memcpy(xx, XS, N * sizeof(uint16_t));
		memcpy(yy, YS[yseed], N * sizeof(uint16_t));
		jumble(xx); jumble(yy);
		reorder(xx, yy);
	}

	return fract;
}

void fract_free(struct fract *fract)
{
	free(fract->xs);
	free(fract);
}

void fract_get(struct fract *fract, int seq, int idx, float *x, float *y)
{
	uint16_t *xx = fract->xs + seq * N;
	uint16_t *yy = fract->ys + seq * N;
	*x = (float) xx[idx] / N;
	*y = (float) yy[idx] / N;
}
