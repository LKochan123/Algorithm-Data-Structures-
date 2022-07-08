# skończone
import polska
from abc import ABC, abstractmethod


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

    def __init__(self):
        pass


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
            self.lst_nei[n-1] = []

    def insert_edge(self, vertex1, vertex2, edge):
        if vertex1 and vertex2 in self.lst:
            idx_v1 = self.get_vertex_idx(vertex1)
            idx_v2 = self.get_vertex_idx(vertex2)
            if idx_v2 not in self.lst_nei[idx_v1]:
                self.lst_nei[idx_v1] += [idx_v2]
            if idx_v1 not in self.lst_nei[idx_v2]:
                self.lst_nei[idx_v2] += [idx_v1]

    def delete_vertex(self, vertex):
        del_idx = self.get_vertex_idx(vertex)  # zapamiętujemy usuwany indeks
        self.lst.pop(del_idx)
        self.dct = {self.lst[i]: i for i in range(len(self.lst))}  # nowy słownik

        for key in self.lst_nei.keys():
            for i, el in enumerate(self.lst_nei[key]):
                if el == del_idx:
                    self.lst_nei[key].pop(i)
                elif el > del_idx:
                    self.lst_nei[key][i] = el - 1

        n = self.order()

        for key, val in self.lst_nei.items():  # przesuwamy klucze elementów wyższe niż usunięty
            if key > del_idx:
                self.lst_nei[key-1] = val

        self.lst_nei.pop(n)  # ostatni wywalamy bo się zmieniejsza o 1

    def delete_edge(self, vertex1, vertex2):
        if vertex1 and vertex2 in self.lst:
            idx_v1 = self.get_vertex_idx(vertex1)
            idx_v2 = self.get_vertex_idx(vertex2)
            for j, el in enumerate(self.lst_nei[idx_v1]):
                if el == idx_v2:
                    self.lst_nei[idx_v1].pop(j)

            for w, el in enumerate(self.lst_nei[idx_v2]):
                if el == idx_v1:
                    self.lst_nei[idx_v2].pop(w)

    def neighbours(self, vertex_idx):
        return self.lst_nei[vertex_idx]

    def size(self):
        how_many_edges = 0
        for idx in self.lst_nei.keys():
            how_many_edges += len(self.lst_nei[idx])

        return int(how_many_edges/2)  # dla grafów nieskierowanych

    def edges(self):
        result_lst = []
        for idx in self.lst_nei.keys():
            for w in self.lst_nei[idx]:
                key_v1 = self.get_vertex(idx)
                key_v2 = self.get_vertex(w)
                result_lst.append((key_v1, key_v2))

        return result_lst


class MatrixNeighbors(Graph):

    def __init__(self):
        super().__init__()
        self.matrix = [[]]

    def insert_vertex(self, vertex):
        super().insert_vertex(vertex)
        n = len(self.lst)

        if len(self.matrix[0]) == 0:  # mamy 0 wierzchołków
            self.matrix = [[0]]
        else:  # 1 lub więcej wierzchołków
            for row in self.matrix:
                row.append(0)
            self.matrix.append([0]*n)

    def insert_edge(self, vertex1, vertex2, edge):
        if vertex1 and vertex2 in self.lst:
            idx1 = int(self.dct[vertex1])
            idx2 = int(self.dct[vertex2])
            self.matrix[idx1][idx2] = 1
            self.matrix[idx2][idx1] = 1
        else:
            return "Podanych wierzchołków nie ma w grafie!"

    def delete_vertex(self, vertex):
        del_idx = self.get_vertex_idx(vertex)
        self.lst.pop(del_idx)
        self.dct = {self.lst[i]: i for i in range(len(self.lst))}  # nowy słownik

        for row in self.matrix:
            row.pop(del_idx)

        self.matrix.pop(del_idx)

    def delete_edge(self, vertex1, vertex2):
        n = self.order() - 1
        v1, v2 = int(self.dct[vertex1]), int(self.dct[vertex2])
        if (v1 and v2) <= n:
            self.matrix[v1][v2] = 0
            self.matrix[v2][v1] = 0

    def neighbours(self, vertex_idx):
        n, lst = self.order() - 1, []
        if vertex_idx > n:
            return "Nie ma węzła o takim indeksie"
        else:
            for i, el in enumerate(self.matrix[vertex_idx]):
                if el == 1:
                    lst.append(i)
            return lst

    def size(self):
        how_many_edges = 0
        n = self.order()
        for i in range(n):
            for j in range(n):
                if self.matrix[i][j] == 1:
                    how_many_edges += 1

        return int(how_many_edges/2)  # dla grafów nieskierowanych dzielimy na 2
        # return how_many_edges  # dla grafów skierowanych

    def edges(self):
        n, edges = self.order(), []
        for i in range(n):
            for j in range(n):
                if self.matrix[i][j] == 1:
                    key1, key2 = self.get_vertex(i), self.get_vertex(j)
                    edges.append((key1, key2))

        return edges


if __name__ == '__main__':
    m = MatrixNeighbors()
    ln = ListNeighbors()

    for _, _, i in polska.polska:
        m.insert_vertex(i)
        ln.insert_vertex(i)

    for v1, v2 in polska.graf:
        m.insert_edge(v1, v2, 1)
        ln.insert_edge(v1, v2, 1)

    m.delete_vertex('K')  # małopolskie
    m.delete_edge('W', 'E')  # mazowieckie - łódzkie

    ln.delete_vertex('K')
    ln.delete_edge('W', 'E')

    all_edges_mn = m.edges()
    all_edges_ln = ln.edges()
    
    # w razie potrzeby można zakomentować 1 funkcję
    polska.draw_map(all_edges_mn) # rysowanie według macierzy sąsiedztwa
    polska.draw_map(all_edges_ln) # rysowanie według listy sąsiedztwa 