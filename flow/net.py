from numbers import Number
from typing import Any, Dict

class Network:
    gamma_fw: Dict[Any, Dict[Any, Number]]
    gamma_bw: Dict[Any, Dict[Any, Number]]

    def __init__(self, source, sink):
        self.v = set()

        # self.gamma[x] = {y: cap}
        self.gamma_fw = {source: {}, sink: {}}
        self.gamma_bw = {source: {}, sink: {}}

        self.s = source
        self.t = sink

    def add_edge(self, x, y, cap):
        self.v.add(x)
        self.v.add(y)

        if x not in self.gamma_fw:
            self.gamma_fw[x] = {}
        self.gamma_fw[x][y] = cap

        if y not in self.gamma_bw:
            self.gamma_bw[y] = {}
        self.gamma_bw[y][x] = cap

        if x not in self.gamma_bw: self.gamma_bw[x] = {}
        if y not in self.gamma_fw: self.gamma_fw[y] = {}

    def aux_net(self, f: Dict) -> "Network":
        na = Network(self.s, self.t)
        last_level = [(None, self.s, 0)]
        t_in_level = False

        while True:
            level = []
            for _, v, _ in last_level:
                for u, c in self.gamma_fw[v].items():
                    if u not in na.v and f[v, u] < c:
                        level.append((v, u, c - f[v, u]))
                        if u == self.t:
                            t_in_level = True

                for u, c in self.gamma_bw[v].items():
                    if u not in na.v and f[u, v] > 0:
                        level.append((v, u, f[u, v]))
                        if u == self.t:
                            t_in_level = True

            if t_in_level:
                for v, u, c in level:
                    if u == na.t:
                        na.add_edge(v, u, c)
            else:
                for v, u, c in level:
                    na.add_edge(v, u, c)

            if not level or t_in_level:
                return na

            last_level = level

