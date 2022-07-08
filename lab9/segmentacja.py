#skończone

from abc import ABC, abstractmethod
from math import inf
import cv2
import numpy as np
from matplotlib import pyplot as plt


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

    def dfs(self, vertex):
        start_idx = self.get_vertex_idx(vertex)
        visited, stack = [], [start_idx]

        while len(stack):
            v = stack.pop()
            if v not in visited:
                visited.append(v)
                for neighbour, _ in self.lst_nei[v]:
                    stack.append(neighbour)

        return visited

    def print_neighbour_list(self):
        print(self.lst_nei)


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

    @staticmethod
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


# W mainie realizuje cały proces segmentacji
def main():
    I = cv2.imread('sample.png', cv2.IMREAD_GRAYSCALE)
    m = MinimumSpanningTree()
    rslt = ListNeighbors()

    XX, YY = I.shape
    # Moja implementacja wymaga aby najpierw dodać wierzchołki
    for i in range(XX):
        for j in range(YY):
            m.insert_vertex(YY * j + i)
            rslt.insert_vertex(YY * j + i)

    # pomijam piksele leżące na brzegach
    for i in range(1, XX - 1):
        for j in range(1, YY - 1):
            # Aktualny wierzchołek i jego jasność
            act_key = YY * j + i
            act_color = int(I[i][j])

            # Wierzchołki sąsiednie i ich jasność
            left_nei, right_nei = YY * (j - 1) + i, YY * (j + 1) + i
            w_left_nei, w_right_nei = I[i][j - 1], I[i][j + 1]

            up_nei, down_nei = YY * j + i - 1, YY * j + i + 1
            w_up_nei, w_down_nei = I[i - 1][j], I[i + 1][j]

            low_diag_l, low_diag_r = YY * (j - 1) + i - 1, YY * (j + 1) + i - 1
            w_low_diag_l, w_low_diag_r = I[i - 1][j - 1], I[i - 1][j + 1]

            upp_diag_l, upp_diag_r = YY * (j - 1) + i + 1, YY * (j + 1) + i + 1
            w_upp_diag_l, w_upp_diag_r = I[i + 1][j - 1], I[i + 1][j + 1]

            # Dodanie krawędzi wraz z wagą
            m.insert_edge(act_key, left_nei, abs(act_color - w_left_nei))
            m.insert_edge(act_key, right_nei, abs(act_color - w_right_nei))
            m.insert_edge(act_key, up_nei, abs(act_color - w_up_nei))
            m.insert_edge(act_key, down_nei, abs(act_color - w_down_nei))
            m.insert_edge(act_key, low_diag_l, abs(act_color - w_low_diag_l))
            m.insert_edge(act_key, low_diag_r, abs(act_color - w_low_diag_r))
            m.insert_edge(act_key, upp_diag_l, abs(act_color - w_upp_diag_l))
            m.insert_edge(act_key, upp_diag_r, abs(act_color - w_upp_diag_r))

    edges, total_cost = m.prime_algorithm(33)
    edges.sort(key=lambda x: x[2])  # sortowanie po wadze
    v1, v2, _ = edges.pop()  # usunięcie krawędzi o najwyższej wadze

    for v_start, v_end, weight in edges:
        rslt.insert_edge(v_start, v_end, weight)

    IS = np.zeros((YY, XX), dtype='uint8')

    # Przeszukiwanie grafu dfs
    dfs_part_1 = rslt.dfs(v1)
    dfs_part_2 = rslt.dfs(v2)

    for element in dfs_part_1:
        col = element // 32
        row = element - 32 * col
        IS[row][col] = 50  # jasność

    for element in dfs_part_2:
        col = element // 32
        row = element - 32 * col
        IS[row][col] = 150  # inna jasność

    plt.imshow(IS, 'gray')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    main()
