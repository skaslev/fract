def igcd(m, n):
    bs = []
    while m != n:
        if m < n:
            n = n - m
            bs.insert(0, 0)
        else:
            m = m - n
            bs.insert(0, 1)
    return m, bs

def ungcd(d, bs):
    m, n = d, d
    for b in bs:
        if b == 0:
            n = m + n
        else:
            m = m + n
    return m, n


def seq(dig):
    ds = []
    while True:
        for i in product(*ds):
            yield i
        ds.append(dig)


def farey_sum(ab, cd, w0=1, w1=1):
    return (w0*ab[0] + w1*cd[0], w0*ab[1] + w1*cd[1])


def split2(ab, cd):
    m = farey_sum(ab, cd)
    return ((ab, m), (m, cd))


def split3(ab, cd):
    m0 = farey_sum(ab, cd, 1, 2)
    m1 = farey_sum(ab, cd, 2, 1)
    return ((ab, m0), (m0, m1), (m1, cd))


def sbt_node(path, ab=(0,1), cd=(1,0), split=split2):
    q = (ab, cd)
    for b in path:
        q = split(*q)[b]
    #return farey_sum(*q)
    rs = split(*q)
    if len(rs) == 2:
        return rs[0][1]
    elif len(rs) == 3:
        return rs[1][0]
        return farey_sum(rs[1][0], rs[1][1])


def sbt(ab=(0,1), cd=(1,0), dig=(0,1), split=split2):
    for s in seq(dig):
        yield sbt_node(s, ab, cd, split)


def cwt(ab=(0,1), cd=(1,0), dig=(0,1), split=split2):
    for s in seq(dig):
        yield sbt_node(reversed(s), ab, cd, split)


cwx=np.linspace(0, 1, N, endpoint=False)
cwy=np.array(take(N, (i[0]/i[1] for i in cwt(dig=(0,1), split=split2) if i[0] < i[1])))
plt.figure(figsize=(5, 5))
plt.grid(True)
plt.plot(cwx, cwy, 'o')
plt.title('Calkin-Wilf')
plt.axes().set_aspect('equal', 'datalim')
plt.show()
