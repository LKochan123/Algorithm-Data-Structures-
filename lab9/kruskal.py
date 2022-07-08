# skończone
from abc import ABC, abstractmethod
from math import inf
from graf_mst import graf


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
                result_lst.append((key_v1, key_v2, weight))

        return result_lst

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

    def kruskal_algorithm(self):
        n = self.order()
        added_edges, total_cost = 0, 0
        result_edges = []

        # Sortowanie krawędzi
        all_edges = self.edges()
        all_edges.sort(key=lambda x: x[2])

        # Dodajemy n - wierzchołków do naszej struktury
        sets = UnionFind()
        for _ in range(n):
            sets.add_vertex()

        while added_edges < n - 1:
            for v_start, v_end, weight in all_edges:
                idx_start = self.get_vertex_idx(v_start)
                idx_end = self.get_vertex_idx(v_end)
                if not sets.same_components(idx_start, idx_end):
                    sets.union(idx_start, idx_end)

                    result_edges += [(v_start, v_end, weight)]
                    total_cost += weight
                    added_edges += 1

        return result_edges, total_cost

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


class UnionFind:

    def __init__(self):
        self.parents = []
        self.rank = []

    def find(self, v):
        if self.parents[v] == -1:  # -1 oznacza, że wierzchołek jest korzeniem
            return v
        return self.find(self.parents[v])

    def union(self, v1, v2):
        if not self.same_components(v1, v2):
            if self.parents[v1] == -1 and self.parents[v2] == -1:  # Dwa korzenie zbiorów
                if self.rank[v1] == self.rank[v2]:
                    self.parents[v1] = v2
                    self.rank[v2] += 1
                else:
                    if self.rank[v1] > self.rank[v2]:
                        self.parents[v2] = v1
                    else:  # ..v2 > ..v1
                        self.parents[v1] = v2
            else:
                new_parent1, new_parent2 = self.find(v1), self.find(v2)

                if self.parents[v1] != -1:
                    self.parents[v1] = new_parent1
                if self.parents[v2] != -1:
                    self.parents[v2] = new_parent2

                self.union(new_parent1, new_parent2)

    def same_components(self, v1, v2):
        if self.find(v1) == self.find(v2):
            return True
        return False

    def add_vertex(self):
        self.parents.append(-1)
        self.rank.append(0)


def main():
    m = MinimumSpanningTree()
    vertexes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    without_ascii = []

    # Moja funkcja wymaga aby najpierw dodać wierzchołki
    for v in vertexes:
        m.insert_vertex(ord(v))  # wczytywanie według kodu ASCII

    for v1, v2, weight in graf:
        m.insert_edge(ord(v1), ord(v2), weight)

    result, total_cost_of_MST = m.kruskal_algorithm()

    # Przekodowanie liczb z kodu ASCII na znaki
    for v1, v2, weight in result:
        without_ascii += [(chr(v1), chr(v2), weight)]

    print('Otrzymany wynik (według kodu ASCII): ')
    print(result, '\n')
    print('Otrzymany wynik zmieniając liczby z kodu ASCII na znaki: ')
    print(without_ascii)
    
if __name__ == "__main__":
    main()