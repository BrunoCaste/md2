from net import Network
from math import inf
from typing import Dict, List, Tuple


def shortest_aug_path(n: Network, f: Dict) -> Tuple:
    # takes the generated queue, returns (eps, augpath[::-1])
    def mk_augpath(q: List) -> List:
        p = []
        idx = -1
        while True:
            p.append(q[idx][0])
            if idx == 0:
                return p
            idx = q[idx][1]

    # q: [(v, parent_idx, eps)]
    q = [(n.s, int(0), inf)]
    visited = {n.s}
    idx = 0

    while idx < len(q):
        v, _, eps = q[idx]
        for u, c in n.gamma_fw[v].items():
            if u not in visited and f[v, u] < c:
                visited.add(u)
                q.append((u, idx, min(eps, c - f[v, u])))

                if u == n.t:
                    return q[-1][2], mk_augpath(q)

        for u, c in n.gamma_bw[v].items():
            if u not in visited and f[u, v] > 0:
                visited.add(u)
                q.append((u, idx, min(eps, f[u, v])))

                if u == n.t:
                    return q[-1][2], mk_augpath(q)

        idx += 1

    return 0, [v for v, _, _ in q]


def edmonds_karp(n: Network) -> Tuple[int, Dict, List]:
    v_f, f = 0, {(x, y): 0 for x in n.v for y in n.gamma_fw[x]}
    while True:
        eps, aug_path = shortest_aug_path(n, f)
        if eps != 0: print(f"eps: {eps}\tpath: {aug_path[::-1]}")
        if aug_path[0] != n.t:
            break
        v_f += eps
        for v, u in zip(reversed(aug_path), reversed(aug_path[:-1])):
            if (v, u) in f:
                f[v, u] += eps
            else:
                f[u, v] -= eps

    return v_f, f, aug_path


if __name__ == "__main__":

    def proc(edges):
        n = Network('s', 't')
        for e, c in edges:
            n.add_edge(e[0], e[1], int(c))

        v, _, s = edmonds_karp(n)

        print("Flow value:", v)
        print("Min cut:", s)
        print()

    networks = ["""
    sa:20 se:10 sg:10 sj:10 ab:20 ah:10 bt:20 cd:30
    di:10 ef:10 ek:5  ft:10 gk:10 gm:5  hj:5  hn:8
    if:5  im:5  jq:10 kt:10 qb:10 mp:10 nc:10 pt:10
    """, """
    sA:10  sC:10 sG:100 AB:10 AE:15 AR:100 Bt:10 CD:10
    CL:100 DB:20 EF:10  EL:7  Ft:20 GH:64  HI:63 IJ:62 JK:61
    KE:60  LM:59 MN:58  NO:57 OP:56 PQ:55  Qt:54 RD:53
    """, """
    sa:5  sc:9  sf:5  sj:10 ab:5 ai:4
    bt:5  ci:10 ck:4  de:10 dn:5 eℓ:10
    fb:4  fh:5  gt:10 ht:5  hk:5 id:10
    jh:10 km:4  ℓg:10 mn:7  mg:4 nt:10
    """, """
    sa:20 sj:10 ab:20 ah:10 bc:20 cd:30 de:10
    dg:10 di:10 ef:10 ek:5  ft:10 gk:10 gm:5  hj:5
    hn:4  if:5  im:5  jℓ:10 kt:10 ℓb:5  mt:10 nc:10
    """, """
    sa:10 sg:10 si:10 ab:10 ak:5  bc:10 cd:30 de:20
    dj:10 ef:20 eh:10 ft:20 gk:10 gm:5  hj:5  hn:4
    ib:5  im:5  jℓ:10 kc:10 ℓf:5  mc:10 nt:10
    """, """
    sa:11 sc:9  sf:5  sj:11 ab:11 ac:3  an:7  bt:11
    ci:10 ck:3  de:10 eg:10 fb:5  fh:10 gt:17 ht:5
    id:10 jh:10 jk:3  kb:3  nm:3  mt:3
    """, """
    sB:20 sC:10 sE:10 sI:10 At:10 BF:20 CD:10 DG:10
    DN:10 EL:10 EN:10 FM:20 Gt:10 Ht:20 IJ:15
    JH:15 KB:10 KG:10 LI:10 LK:10 Mt:10 MK:10 NA:10
    """]

    for i, n in enumerate(networks):
        net = [x.split(":") for x in n.split()]
        print(">>> ", i+1)
        proc(net)

