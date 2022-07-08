#skończone

class Matrix:

    def __init__(self, dimensions, value=0):
        if isinstance(dimensions, tuple):
            row, col = dimensions
            self.__matrix = [[value] * col for _ in range(row)]
        else:
            self.__matrix = dimensions

    def __add__(self, other):
        n = other.__len__()[0]
        m = other.__len__()[1]
        result = [[0] * m for _ in range(n)]

        if len(self.__matrix) != other.__len__()[0] or len(self.__matrix[0]) != other.__len__()[1]:
            raise ValueError('Niezgodne rozmiary macierzy')
        else:
            for i in range(n):
                for j in range(m):
                    result[i][j] = self.__matrix[i][j] + other[i][j]

        return Matrix(result)

    def __mul__(self, other):
        row1, col1 = len(self.__matrix), len(self.__matrix[0])
        row2, col2 = other.__len__()[0], other.__len__()[1]
        result = [[0] * col2 for _ in range(row1)]

        if col1 != row2:
            raise ValueError('Nie można pomnożyć macierzowo')
        else:
            for i in range(row1):
                for j in range(col2):
                    for k in range(row2):
                        result[i][j] += self.__matrix[i][k] * other[k][j]

        return Matrix(result)

    def __getitem__(self, item):
        return self.__matrix[item]

    def __str__(self):
        row = len(self.__matrix)
        column = len(self.__matrix[0])

        for i in range(row):
            for j in range(column):
                print(self.__matrix[i][j], end=" ")
            print("")

    def __len__(self):  # zwraca rozmiar macierzy
        return len(self.__matrix), len(self.__matrix[0])


def transpose_matrix(matrix):
    n = len(matrix)
    m = len(matrix[0])
    result = [[0]*n for _ in range(m)]

    for row in range(m):
        for col in range(n):
            result[row][col] = matrix[col][row]

    return result


if __name__ == '__main__':

    m1 = [[1, 0, 2],
          [-1, 3, 1]]

    m3 = [[3, 1],
          [2, 1],
          [1, 0]]

    o1 = Matrix(m1)
    o2 = Matrix((2, 3), 1)
    o3 = Matrix(m3)

    k = transpose_matrix(m1)
    o4 = Matrix(k)

    o4.__str__(), print("")
    (o1 + o2).__str__(), print("")
    (o1 * o3).__str__()