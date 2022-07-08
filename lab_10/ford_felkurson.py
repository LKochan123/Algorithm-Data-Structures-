# skończone
from abc import ABC, abstractmethod
from math import inf


class Node:

    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        if self.key == other:
            return True
        return False


class Edge:

    def __init__(self, capacity, flow, residual, isresidual):
        self.capacity = capacity
        self.flow = flow
        self.residual = residual
        self.isresidual = isresidual

    def __repr__(self):
        return f'{self.capacity} {self.flow} {self.residual} {self.isresidual}'

    def return_tuple(self):
        return self.capacity, self.flow, self.residual, self.isresidual


class Graph(ABC):

    @abstractmethod
    def __init__(self):
        self.lst = []
        self.dct = {}

    def insert_vertex(self, vertex):
        v = Node(vertex)
        if v not in self.lst:
            self.lst.append(v.key)

        n = len(self.lst)
        self.dct = {self.lst[i]: i for i in range(n)}

    @abstractmethod
    def insert_edge(self, vertex1, vertex2, edge):
        pass

    @abstractmethod
    def delete_vertex(self, vertex):
        pass

    @abstractmethod
    def delete_edge(self, vertex1, vertex2):
        pass

    def get_vertex_idx(self, vertex):
        if vertex in self.lst:
            return self.dct[vertex]
        else:
            return "Nie ma takiego węzła"

    def get_vertex(self, vertex_idx):
        n = len(self.lst) - 1
        if vertex_idx > n:
            return 'Nie ma węzła o takim indeksie'
        else:
            for key, value in self.dct.items():
                if vertex_idx == value:
                    return key

    @abstractmethod
    def neighbours(self, vertex_idx):
        pass

    def order(self):
        return len(self.lst)

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def edges(self):
        pass


class ListNeighbors(Graph):

    def __init__(self):
        super().__init__()
        self.lst_nei = {}

    def insert_vertex(self, vertex):
        super().insert_vertex(vertex)
        n = len(self.lst)

        if len(self.lst_nei) == 0:
            self.lst_nei = {0: []}
        else:
            self.lst_nei[n - 1] = []

    def insert_edge(self, vertex1, vertex2, edge):
        if vertex1 and vertex2 in self.lst:
            idx_v1 = self.get_vertex_idx(vertex1)
            idx_v2 = self.get_vertex_idx(vertex2)
            if idx_v2 not in self.lst_nei[idx_v1]:
                self.lst_nei[idx_v1] += [(idx_v2, edge)]
            # if idx_v1 not in self.lst_nei[idx_v2]:
            #     self.lst_nei[idx_v2] += [(idx_v1, edge)]

    def delete_vertex(self, vertex):
        del_idx = self.get_vertex_idx(vertex)  # zapamiętujemy usuwany indeks
        self.lst.pop(del_idx)
        self.dct = {self.lst[i]: i for i in range(len(self.lst))}  # nowy słownik

        for key in self.lst_nei.keys():
            for i, el in enumerate(self.lst_nei[key]):
                neighbour_key, _ = el
                if neighbour_key == del_idx:
                    self.lst_nei[key].pop(i)
                elif neighbour_key > del_idx:
                    self.lst_nei[key][i] = neighbour_key - 1

        n = self.order()

        for key, val in self.lst_nei.items():  # przesuwamy klucze elementów wyższe niż usunięty
            if key > del_idx:
                self.lst_nei[key - 1] = val

        self.lst_nei.pop(n)  # ostatni wywalamy bo się zmieniejsza o 1

    def delete_edge(self, vertex1, vertex2):
        if vertex1 and vertex2 in self.lst:
            idx_v1 = self.get_vertex_idx(vertex1)
            idx_v2 = self.get_vertex_idx(vertex2)
            for j, el in enumerate(self.lst_nei[idx_v1]):
                key, weight = el  
                if key == idx_v2:
                    self.lst_nei[idx_v1].pop(j)

            for w, el in enumerate(self.lst_nei[idx_v2]):
                key, weight = el
                if key == idx_v1:
                    self.lst_nei[idx_v2].pop(w)

    def neighbours(self, vertex_idx):
        return self.lst_nei[vertex_idx]

    def size(self):
        how_many_edges = 0
        for idx in self.lst_nei.keys():
            how_many_edges += len(self.lst_nei[idx])

        return int(how_many_edges / 2)  # dla grafów nieskierowanych

    def edges(self):
        result_lst = []
        for idx in self.lst_nei.keys():
            for w, weight in self.lst_nei[idx]:
                key_v1 = self.get_vertex(idx)
                key_v2 = self.get_vertex(w)
                result_lst.append((key_v1, key_v2))

        return result_lst

    def bfs(self, v_start):
        idx_start, n = self.get_vertex_idx(v_start), self.order()

        parent = {i: -1 for i in range(n)}
        visited = {i: False for i in range(n)}

        queue = [idx_start]
        visited[idx_start] = True

        while queue:
            actual_vertex = queue.pop(0)
            for neighbour, edge in self.neighbours(actual_vertex):
                if (not visited[neighbour]) and edge.residual > 0:
                    queue.append(neighbour)
                    visited[neighbour] = True
                    parent[neighbour] = actual_vertex

        return parent

    def path_analysis(self, v_start, v_end, parent):
        idx_start = self.get_vertex_idx(v_start)
        idx_end = self.get_vertex_idx(v_end)

        min_flow = inf
        act_idx = idx_end

        if parent[idx_end] == -1:
            return 0
        else:
            while act_idx != idx_start:
                previous = parent[act_idx]
                for v, edge in self.lst_nei[previous]:
                    if v == act_idx and not edge.isresidual:
                        if edge.residual < min_flow:
                            min_flow = edge.residual
                act_idx = previous

        return min_flow

    def path_augmentation(self, v_start, v_end, parent, min_flow):
        idx_start = self.get_vertex_idx(v_start)
        idx_end = self.get_vertex_idx(v_end)

        act_idx = idx_end

        while act_idx != idx_start:
            previous = parent[act_idx]
            # krawędź rzeczywista
            for v, edge in self.lst_nei[previous]:
                if v == act_idx and not edge.isresidual:
                    edge.flow += min_flow
                    edge.residual -= min_flow

            # krawędź resztowa
            for v1, edge1 in self.lst_nei[act_idx]:
                if v1 == previous and edge1.isresidual:
                    edge1.residual += min_flow

            act_idx = previous

    def ford_fulkerson(self):
        parents = self.bfs('s')
        min_flow = self.path_analysis('s', 't', parents)

        while min_flow > 0:
            self.path_augmentation('s', 't', parents, min_flow)
            parents = self.bfs('s')
            min_flow = self.path_analysis('s', 't', parents)

    def calculate_total_flow(self):
        t_idx = self.get_vertex_idx('t')
        total_flow = 0

        for v, edge in self.neighbours(t_idx):
            total_flow += edge.residual

        return total_flow

    def print_neighbour_list(self):
        print(self.lst_nei)

    @ staticmethod
    def print_graph(g):
        n = g.order()
        print("------GRAPH------", n)
        for i in range(n):
            v = g.get_vertex(i)
            print(v, end=" -> ")
            nbrs = g.neighbours(i)
            for (j, w) in nbrs:
                print(g.get_vertex(j), w, end=";")
            print()
        print("-------------------")


def test_graf_0():
    graf_0 = [('s', 'u', 2), ('u', 't', 1), ('u', 'v', 3), ('s', 'v', 1), ('v', 't', 2)]
    graf_0_vertexes = ['s', 'u', 'v', 't']
    g = ListNeighbors()

    for v1 in graf_0_vertexes:
        g.insert_vertex(v1)

    for v_start, v_end, weight in graf_0:
        # rzeczywista
        e1 = Edge(weight, 0, weight, False)
        g.insert_edge(v_start, v_end, e1)

        # rezydualna
        e2 = Edge(weight, 0, 0, True)
        g.insert_edge(v_end, v_start, e2)

    g.ford_fulkerson()
    print(g.calculate_total_flow())
    g.print_graph(g)


def test_graf_1():
    graf_1 = [('s', 'a', 16), ('s', 'c', 13), ('a', 'c', 10), ('c', 'a', 4), ('a', 'b', 12), ('b', 'c', 9),
              ('b', 't', 20), ('c', 'd', 14), ('d', 'b', 7), ('d', 't', 4)]
    graf_1_vertexes = ['s', 'a', 'b', 'c', 'd', 't']
    g1 = ListNeighbors()

    for v in graf_1_vertexes:
        g1.insert_vertex(v)

    for v_start, v_end, weight in graf_1:
        # rzeczywista
        e1 = Edge(weight, 0, weight, False)
        g1.insert_edge(v_start, v_end, e1)

        # rezydualna
        e2 = Edge(weight, 0, 0, True)
        g1.insert_edge(v_end, v_start, e2)

    g1.ford_fulkerson()
    print(g1.calculate_total_flow())
    g1.print_graph(g1)


def test_graf_2():
    graf_2 = [('s', 'a', 3), ('s', 'c', 3), ('a', 'b', 4), ('b', 's', 3), ('b', 'c', 1),
               ('b', 'd', 2), ('c', 'e', 6), ('c', 'd', 2), ('d', 't', 1), ('e', 't', 9)]
    graf_2_vertexes = ['s', 'a', 'b', 'c', 'd', 'e', 't']
    g2 = ListNeighbors()

    for v in graf_2_vertexes:
        g2.insert_vertex(v)

    for v_start, v_end, weight in graf_2:
        # rzeczywista
        e1 = Edge(weight, 0, weight, False)
        g2.insert_edge(v_start, v_end, e1)

        # rezydualna
        e2 = Edge(weight, 0, 0, True)
        g2.insert_edge(v_end, v_start, e2)

    g2.ford_fulkerson()
    print(g2.calculate_total_flow())
    g2.print_graph(g2)


def test_graf_3():
    graf_3 = [('s', 'a', 8), ('s', 'd', 3), ('a', 'b', 9), ('b', 'd', 7), ('b', 't', 2),
              ('c', 't', 5), ('d', 'b', 7), ('d', 'c', 4)]
    graf_3_vertexes = ['s', 'a', 'b', 'c', 'd', 't']
    g = ListNeighbors()

    for v in graf_3_vertexes:
        g.insert_vertex(v)

    for v_start, v_end, weight in graf_3:
        # rzeczywista
        e1 = Edge(weight, 0, weight, False)
        g.insert_edge(v_start, v_end, e1)

        # rezydualna
        e2 = Edge(weight, 0, 0, True)
        g.insert_edge(v_end, v_start, e2)

    g.ford_fulkerson()
    print(g.calculate_total_flow())
    g.print_graph(g)


def main():
    test_graf_0()
    test_graf_1()
    test_graf_2()
    test_graf_3()


if __name__ == '__main__':
    main()