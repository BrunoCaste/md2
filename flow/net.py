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

