#ifndef FRACT_H
#define FRACT_H

struct fract *fract_init(int nseq);
void fract_get(struct fract *fract, int seq, int idx, float *x, float *y);
void fract_free(struct fract *fract);

#endif
