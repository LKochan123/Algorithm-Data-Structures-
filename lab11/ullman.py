# skończone
from abc import ABC, abstractmethod
import numpy as np


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


class MatrixNeighbors(Graph):

    def __init__(self):
        super().__init__()
        self.matrix = [[]]
        self.edges_weight = [[]]

    def insert_vertex(self, vertex):
        super().insert_vertex(vertex)
        n = len(self.lst)

        if len(self.matrix[0]) == 0:  # mamy 0 wierzchołków
            self.matrix = [[0]]
            self.edges_weight = [[0]]
        else:  # 1 lub więcej wierzchołków
            for row in self.matrix:
                row.append(0)
            for row in self.edges_weight:
                row.append(0)

            self.matrix.append([0]*n)
            self.edges_weight.append([0]*n)

    def insert_edge(self, vertex1, vertex2, weight):
        if vertex1 and vertex2 in self.lst:
            idx1 = int(self.dct[vertex1])
            idx2 = int(self.dct[vertex2])
            self.matrix[idx1][idx2] = 1
            self.edges_weight[idx1][idx2] = weight
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
            self.edges_weight[v1][v2] = 0

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

        return how_many_edges

    def edges(self):
        n, edges = self.order(), []
        for i in range(n):
            for j in range(n):
                if self.matrix[i][j] == 1:
                    key1, key2 = self.get_vertex(i), self.get_vertex(j)
                    edges.append((key1, key2))

        return edges
    
    @staticmethod
    def save_to_numpy(matrix):
        n = len(matrix)
        numpy_matrix = matrix
        numpy_matrix = np.zeros((n, n))

        for i in range(n):
            for j in range(n):
                numpy_matrix[i, j] = matrix[i][j]

        return numpy_matrix
    
    # Zakładam, że:
    # i -> iteruje po pierwszy wierszu 
    # j -> --||-- 2 
    # k -> --||-- 3
    def ullman_brutheforce_version_1(self, g, p):
        n, m = len(g), len(p)
        count_good_solutions, iterations = 0, 0
        
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if i != j and i != k and j != k:
                        M = np.zeros(shape=(m, n))
                        G, P = self.save_to_numpy(g), self.save_to_numpy(p)

                        M[0, i], M[1, j], M[2, k] = 1, 1, 1

                        check_izomorfizm = M @ ((M @ G).T)

                        iterations += 1

                        if self.check_is_it_the_same_matrix(P, check_izomorfizm):
                            count_good_solutions += 1
                            
        return count_good_solutions, iterations
    
    
    def ullman_version_2(self, g, p):
        n, m = len(g), len(p)
        count_good_solutions, iterations = 0, 0
        
        for i in range(n):
            if self.v_deg(g, i) >= self.v_deg(p, 0):
                for j in range(n):
                    if self.v_deg(g, j) >= self.v_deg(p, 1) and i != j:
                        for k in range(n):
                            if self.v_deg(g, k) >= self.v_deg(p, 2):
                                if i != k and j != k:
                                    M = np.zeros(shape=(m, n))
                                    G, P = self.save_to_numpy(g), self.save_to_numpy(p)

                                    M[0, i], M[1, j], M[2, k] = 1, 1, 1

                                    check_izomorfizm = M @ ((M @ G).T)

                                    iterations += 1

                                    if self.check_is_it_the_same_matrix(P, check_izomorfizm):
                                        count_good_solutions += 1
                            
        return count_good_solutions, iterations
    

    def ullman_final_version_3(self, g, p):
        n, m = len(g), len(p)
        count_good_solutions, iterations = 0, 0
        
        for i in range(n):
            if self.v_deg(g, i) >= self.v_deg(p, 0):
                for j in range(n):
                    if self.v_deg(g, j) >= self.v_deg(p, 1) and i != j:
                        for k in range(n):
                            if self.v_deg(g, k) >= self.v_deg(p, 2):
                                if i != k and j != k:
                                    if self.prune(g, p, i, j, k):
                                        M = np.zeros(shape=(m, n))
                                        G, P = self.save_to_numpy(g), self.save_to_numpy(p)

                                        M[0, i], M[1, j], M[2, k] = 1, 1, 1

                                        check_izomorfizm = M @ ((M @ G).T)

                                        iterations += 1

                                        if self.check_is_it_the_same_matrix(P, check_izomorfizm):
                                            count_good_solutions += 1
                            
        return count_good_solutions, iterations
    
    # Zagmantwany prune
    def prune(self, g_matrix, p_matrix, i, j, k):
        nei_in_first_row = g_matrix[i]
        nei_in_sec_row = g_matrix[j]
        nei_in_third_row = g_matrix[k]
        
        p_nei_in_first_row = self.return_edges_form_vertex_idx(p_matrix, 0)
        p_nei_in_sec_row = self.return_edges_form_vertex_idx(p_matrix, 1)
        p_nei_in_third_row = self.return_edges_form_vertex_idx(p_matrix, 2)
        
        counter = 0
        
        for nei_0 in p_nei_in_first_row:
            mapped_nei = self.map_idx(nei_0, i, j, k)
            if nei_in_first_row[mapped_nei]:
                counter += 1
                
        for nei_0 in p_nei_in_sec_row:
            mapped_nei = self.map_idx(nei_0, i, j, k)
            if nei_in_sec_row[mapped_nei]:
                counter += 1
        
        for nei_0 in p_nei_in_third_row:
            mapped_nei = self.map_idx(nei_0, i, j, k)
            if nei_in_third_row[mapped_nei]:
                counter += 1
                
        if counter == self.v_deg(p_matrix, 0) + self.v_deg(p_matrix, 1) + self.v_deg(p_matrix, 2):
            return True
        return False
    
    # Sprawdzamy czy macierze są takie same (dla numpy)
    @staticmethod
    def check_is_it_the_same_matrix(m1, m2):
        X, Y = m1.shape
        X1, Y1 = m2.shape
        count_good_elements = 0
        
        if X == X1 and Y == Y1:
            for i in range(X):
                for j in range(Y):
                    if m1[i, j] == m2[i, j]:
                        count_good_elements += 1
                        
            if count_good_elements == X*Y:
                return True
            return False
        else:
            return False
        
    # zwraca liczbę sąsiadów danego wierzchołka
    @staticmethod
    def v_deg(matrix, v_idx):
        return sum(matrix[v_idx])

    # zwraca indeksy sąsiądów danego wierzchołka (czyli tam gdzie są 1)
    @staticmethod
    def return_edges_form_vertex_idx(matrix, vertex_idx):
        result = []
        for nei in range(len(matrix[vertex_idx])):
            if matrix[vertex_idx][nei]:
                result += [nei]

        return result
    
    # Funkcja pomocnicza do funkcji Prune 
    @staticmethod
    def map_idx(idx, i, j, k):
        if not idx:
            return i
        elif idx == 1:
            return j
        elif idx == 2:
            return k

    def print_adjacency_matrix(self):
        for row in self.matrix:
            print(row)

    def print_edges_weight(self):
        for row in self.edges_weight:
            print(row)

    def return_adjacency_matrix(self):
        return self.matrix


def main():
    g = MatrixNeighbors()
    p = MatrixNeighbors()

    graph_G = [('A', 'B', 1), ('B', 'F', 1), ('B', 'C', 1), ('C', 'D', 1), ('C', 'E', 1), ('D', 'E', 1)]
    G_vertexes = ['A', 'B', 'C', 'D', 'E', 'F']

    graph_P = [('A', 'B', 1), ('B', 'C', 1), ('A', 'C', 1)]
    P_vertexes = ['A', 'B', 'C']

    # Dodajemy wierzchołki
    for vertex in G_vertexes:
        g.insert_vertex(vertex)

    for vertex in P_vertexes:
        p.insert_vertex(vertex)

    # Dodajemy krawędzie w obie strony
    for v_start, v_end, cost in graph_G:
        g.insert_edge(v_start, v_end, cost)
        g.insert_edge(v_end, v_start, cost)

    for v_start, v_end, cost in graph_P:
        p.insert_edge(v_start, v_end, cost)
        p.insert_edge(v_end, v_start, cost)

    # Pobieramy macierz sąsiedztwa
    g11 = g.return_adjacency_matrix()
    p11 = p.return_adjacency_matrix()
    
    # Wywołanie wyników
    solutions_v1, iterations_v1 = g.ullman_brutheforce_version_1(g11, p11)
    solutions_v2, iterations_v2 = g.ullman_version_2(g11, p11)
    solutions_v3, iterations_v3 = g.ullman_final_version_3(g11, p11)
    
    print(solutions_v1, iterations_v1)
    print(solutions_v2, iterations_v2)
    print(solutions_v3, iterations_v3)

    
if __name__ == '__main__':
    main()