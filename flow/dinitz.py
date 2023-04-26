from typing import Callable, Dict, List, Set, Tuple
from math import inf
from net import Network 


def block_original(an: Network, f: Dict) -> int:
    def aug_path():
        eps, p, path = inf, an.s, [an.s]
        while p != an.t:
            q, c = next(iter(an.gamma_fw[p].items()))
            path.append(q)
            p = q
            eps = min(eps, c)
        return eps, path

    def prune(dead_ends: List):
        idx = 0
        while idx < len(dead_ends):
            x = dead_ends[idx]
            for y in an.gamma_bw[x]:
                an.gamma_fw[y].pop(x)
                if not an.gamma_fw[y] and an.gamma_bw:
                    dead_ends.append(y)
            an.gamma_bw[x] = {}
            idx += 1

    aux_net_eps = 0
    dead_ends = [v for v, g in an.gamma_fw.items() if not g and v != an.t]

    while True:
        prune(dead_ends)
        dead_ends = []
        if not an.gamma_fw[an.s]: return aux_net_eps

        eps, path = aug_path()
        print(f"\t{path}")
        aux_net_eps += eps
        for x, y in zip(path, path[1:]):
            an.gamma_fw[x][y] -= eps
            if an.gamma_fw[x][y] == 0:
                an.gamma_fw[x].pop(y)
                an.gamma_bw[y].pop(x)
            if not an.gamma_fw[x]: dead_ends.append(x)

            if (x, y) in f: f[x, y] += eps
            else: f[y, x] -= eps


def block_even(an: Network, f: Dict) -> int:
    def fwd(p):
        x, eps = p[-1]
        y, xy_cap = next(iter(an.gamma_fw[x].items()))
        p.append((y, min(eps, xy_cap)))
    def bwd(p):
        (z, _), (x, _) = p[-2:]
        an.gamma_fw[z].pop(x)
        p.pop()
    def inc(p):
        eps = p[-1][1]
        for (v, _), (u, _) in zip(p, p[1:]):
            if (v, u) in f: f[v, u] += eps
            else: f[u, v] -= eps
            an.gamma_fw[v][u] -= eps
            if an.gamma_fw[v][u] == 0: an.gamma_fw[v].pop(u)
        return eps

    aux_net_eps = 0
    stop = False
    while not stop:
        path = [(an.s, inf)]
        while path[-1][0] != an.t and not stop:
            x, _ = path[-1]
            if an.gamma_fw[x]: fwd(path)
            elif x != an.s: bwd(path) 
            else: stop = True
        if path[-1][0] == an.t:
            print(f"\t{[v for v, _ in path]}")
            aux_net_eps += inc(path)

    return aux_net_eps


def print_layered(i: int, n: Network):
    print(f"NA {i}", end="")
    layer = {n.s}
    i = 0
    while layer and layer != {n.t}:
        print(f"\t>>> V{i}")
        next_layer = set()
        for v in layer:
            if n.gamma_fw[v]:
                print(f"\t{v} -> {list(n.gamma_fw[v].keys())}")
                for u in n.gamma_fw[v]: next_layer.add(u)
        layer = next_layer
        i += 1


def dinitz_type(n: Network, block: Callable[[Network, Dict], int]) -> Tuple[int, Dict, Set]:
    v_f, f = 0, {(x, y): 0 for x in n.v for y in n.gamma_fw[x]}
    an = n.aux_net(f)
    i = 1
    while n.t in an.v:
        print_layered(i, an)
        v_f += block(an, f)
        print()
        an = n.aux_net(f)
        i += 1
    return v_f, f, an.v


def dinitz(n: Network): return dinitz_type(n, block_original)
def dinic_even(n: Network): return dinitz_type(n, block_even)


if __name__ == "__main__":
    algo = int(input("Choose an algorithm (1 for Dinitz, 2 for Dinic-Even): "))
    algo = [dinitz, dinic_even][algo-1]

    def proc(edges):
        n = Network('s', 't')
        for e, c in edges:
            n.add_edge(e[0], e[1], int(c))

        v, _, s = algo(n)

        print("Flow value:", v)
        print("Min cut:", sorted(s))
        print()

    networks = ["""
    sA:144 sB:96 sN:150 AC:100 AD:70 AF:85 AL:17 BC:10  BD:17 BG:102 BL:35
    Ct:80  CJ:5  Dt:80  EC:100 ED:15 EG:10 FH:15 FK:100 Gt:80 Ht:20  HM:40
    ID:22  IG:10 JA:5   Kt:120 LH:30 LK:60 Mt:30 NE:110 NI:40
    """, """
    sa:15 sd:20 sj:7 ab:17 ah:5 bc:15 ct:20 dc:26 de:5 dg:10 di:6 ef:5 ek:2
    ft:5  gk:10 gm:3 go:1  hn:4 if:4  jl:7  kt:10 lb:5 ln:4  mt:1 nc:6 ot:10
    """, """
    sA:20 sB:69  sC:145 AD:14 AE:19  AF:18 BD:9  BE:4  BF:14
    BH:1  CE:190 CF:4   CH:20 CI:20  Dt:9  DH:8  DI:1  DJ:7
    Et:16 EH:2   EI:16  EJ:7  Ft:146 GI:5  Ht:25 It:15 Jt:7
    """, """
    su:160 sv:50  sw:100 ah:20 an:10 bh:10 bi:20 ci:10  cj:20 dj:15 dk:20 ek:15
    el:20  fl:15  fm:20  gm:15 gn:10 ht:20 it:20 jt:20  kt:20 lt:20 mt:20 nt:20
    pa:20  pb:20  pc:20  pd:20 pe:20 pf:20 pg:25 qx:50  qz:50 rx:50 rz:50 ux:60
    uy:200 uz:100 vq:70  vr:20 wq:70 wr:30 xt:60 yp:200 zt:100
    """]

    for i, n in enumerate(networks):
        net = [x.split(":") for x in n.split()]
        print(">>> ", i+1)
        proc(net)

