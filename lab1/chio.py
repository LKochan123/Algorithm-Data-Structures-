#skończone

class Matrix:

    def __init__(self, dimensions, value=0):
        if isinstance(dimensions, tuple):
            row, col = dimensions
            self.__matrix = [[value] * col for _ in range(row)]
        else:
            self.__matrix = dimensions

    def chio(self, matrix1) -> float:
        n = len(matrix1)
        m = len(matrix1[0])

        if n != m:
            raise Exception("Matrix isn't square")
        else:
            if n == 2:
                det = matrix1[0][0] * matrix1[1][1] - (matrix1[1][0] * matrix1[0][1])
                return det
            else:
                new_matrix = [[0]*(n-1) for _ in range(n-1)]
                for i in range(n-1):
                    for j in range(n-1):
                        det1 = matrix1[0][0] * matrix1[i + 1][j + 1] - (matrix1[i + 1][0] * matrix1[0][j + 1])
                        new_matrix[i][j] = det1

                k = pow(matrix1[0][0], n - 2)

                if k != 0:
                    return 1/k * Matrix.chio(self, new_matrix)
                else:
                    first_row = matrix1[0]
                    for i in range(n):
                        if first_row[i] != 0:
                            k = i  # szukamy pierwszego indeksu kolumny w którym nie ma 0 żeby zamienić
                            break
                    for j in range(n):
                        for w in range(n):
                            matrix1[j][0], matrix1[j][k] = matrix1[j][k], matrix1[j][0]
                    return -1/k * Matrix.chio(self, matrix1)


if __name__ == '__main__':

    m1 = [[5, 1, 1, 2, 3],
          [4, 2, 1, 7, 3],
          [2, 1, 2, 4, 7],
          [9, 1, 0, 7, 0],
          [1, 4, 7, 2, 2]]

    m2 = [[0, 1, 1, 2, 3],
          [4, 2, 1, 7, 3],
          [2, 1, 2, 4, 7],
          [9, 1, 0, 7, 0],
          [1, 4, 7, 2, 2]]

    o1 = Matrix(m1)
    o2 = Matrix(m2)

    print(o1.chio(m1))
    print(o2.chio(m2))