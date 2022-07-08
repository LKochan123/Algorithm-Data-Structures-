# skończone
from abc import ABC, abstractmethod
from math import inf
import graf_mst

class Node:

    def __init__(self, key):
        self.key = key

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        if self.key == other:
            return True
        return False


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

    def insert_edge(self, vertex1, vertex2, edge_weight):
        if vertex1 and vertex2 in self.lst:
            idx_v1 = self.get_vertex_idx(vertex1)
            idx_v2 = self.get_vertex_idx(vertex2)
            if idx_v2 not in self.lst_nei[idx_v1]:
                self.lst_nei[idx_v1] += [(idx_v2, edge_weight)]
            if idx_v1 not in self.lst_nei[idx_v2]:
                self.lst_nei[idx_v2] += [(idx_v1, edge_weight)]

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
                key, weight = el  # tuple unpacking klucz i waga wierzchołka
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
            for w, weight in self.lst_nei[idx]:  # w - klucz, weight - waga krawedzi
                key_v1 = self.get_vertex(idx)
                key_v2 = self.get_vertex(w)
                result_lst.append((key_v1, key_v2))

        return result_lst

    def print_neighbour_list(self):
        print(self.lst_nei)


# class MatrixNeighbors(Graph):

#     def __init__(self):
#         super().__init__()
#         self.matrix = [[]]

#     def insert_vertex(self, vertex):
#         super().insert_vertex(vertex)
#         n = len(self.lst)

#         if len(self.matrix[0]) == 0:  # mamy 0 wierzchołków
#             self.matrix = [[0]]
#         else:  # 1 lub więcej wierzchołków
#             for row in self.matrix:
#                 row.append(0)
#             self.matrix.append([0] * n)

#     def insert_edge(self, vertex1, vertex2, edge):
#         if vertex1 and vertex2 in self.lst:
#             idx1 = int(self.dct[vertex1])
#             idx2 = int(self.dct[vertex2])
#             self.matrix[idx1][idx2] = 1
#             self.matrix[idx2][idx1] = 1
#         else:
#             return "Podanych wierzchołków nie ma w grafie!"

#     def delete_vertex(self, vertex):
#         del_idx = self.get_vertex_idx(vertex)
#         self.lst.pop(del_idx)
#         self.dct = {self.lst[i]: i for i in range(len(self.lst))}  # nowy słownik

#         for row in self.matrix:
#             row.pop(del_idx)

#         self.matrix.pop(del_idx)

#     def delete_edge(self, vertex1, vertex2):
#         n = self.order() - 1
#         v1, v2 = int(self.dct[vertex1]), int(self.dct[vertex2])
#         if (v1 and v2) <= n:
#             self.matrix[v1][v2] = 0
#             self.matrix[v2][v1] = 0

#     def neighbours(self, vertex_idx):
#         n, lst = self.order() - 1, []
#         if vertex_idx > n:
#             return "Nie ma węzła o takim indeksie"
#         else:
#             for i, el in enumerate(self.matrix[vertex_idx]):
#                 if el == 1:
#                     lst.append(i)
#             return lst

#     def size(self):
#         how_many_edges = 0
#         n = self.order()
#         for i in range(n):
#             for j in range(n):
#                 if self.matrix[i][j] == 1:
#                     how_many_edges += 1

#         return int(how_many_edges / 2)  # dla grafów nieskierowanych dzielimy na 2
#         # return how_many_edges  # dla grafów skierowanych

#     def edges(self):
#         n, edges = self.order(), []
#         for i in range(n):
#             for j in range(n):
#                 if self.matrix[i][j] == 1:
#                     key1, key2 = self.get_vertex(i), self.get_vertex(j)
#                     edges.append((key1, key2))

#         return edges


class MinimumSpanningTree(ListNeighbors):

    def __init__(self):
        super().__init__()

    def prime_algorithm(self, start_vertex):
        start_idx = self.get_vertex_idx(start_vertex)

        n = self.order()  # ilość wierzchołków w grafie
        visited = {idx: False for idx in range(n)}
        added_edges, total_cost = 0, 0
        edges_lst_result = []

        visited[start_idx] = True

        while added_edges < n - 1:
            min_cost = inf
            act_vertex, neighbour_of_act_vertex = -1, -1
            for idx_vertex in range(n):
                if visited[idx_vertex]:
                    for neighbour, weight in self.lst_nei[idx_vertex]:
                        if not visited[neighbour]:
                            if min_cost > weight:
                                min_cost = weight
                                act_vertex, neighbour_of_act_vertex = idx_vertex, neighbour

            visited[neighbour_of_act_vertex] = True
            added_edges += 1
            total_cost += min_cost

            v1 = self.get_vertex(act_vertex)
            v2 = self.get_vertex(neighbour_of_act_vertex)
            edges_lst_result.append((v1, v2, min_cost))

        return edges_lst_result, total_cost

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


def main():
    m = MinimumSpanningTree()
    result = ListNeighbors()
    vertexes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

    for key in vertexes:
        m.insert_vertex(key)
        result.insert_vertex(key)

    # Metoda insert_edge sama dodaje krawędź w obie strony
    for element in range(len(graf_mst.graf)):
        v1, v2, weight = graf_mst.graf[element]
        m.insert_edge(v1, v2, weight)

    edges, total_cost = m.prime_algorithm('A')

    # Wczytywanie grafu wynikowego (MST)
    for v1, v2, weight in edges:
        result.insert_edge(v1, v2, weight)

    m.print_graph(result)


if __name__ == '__main__':
    main()