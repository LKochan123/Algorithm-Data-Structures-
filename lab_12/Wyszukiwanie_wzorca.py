# skończone


class TextAlgorithms:

    def __init__(self, text):
        self.text = text

    def naive_method(self, W):
        m, n = len(self.text), len(W)
        iterations, counter = 0, 0

        for i in range(m-n+1):
            j = 0
            while j < n and self.text[i + j] == W[j]:
                j += 1
                iterations += 1

            if j == n:
                counter += 1

            iterations += 1

        return counter, iterations

    @staticmethod
    def hash(text):
        q, d = 101, 256
        n, hw = len(text), 0
        for i in range(n):
            hw = (hw * d + ord(text[i])) % q

        return hw

    def rabin_karp_method(self, template):
        S = self.text
        M, N = len(S), len(template)
        hW = self.hash(template)
        hS = self.hash(S[:N])

        counter, iterations, colisions = 0, 0, 0
        q, d, h = 101, 256, 1

        for i in range(N-1):
            h = (h * d) % q

        for m in range(1, M-N+1):
            hS = (d * (hS - ord(S[m-1]) * h) + ord(S[m+N-1])) % q
            if hS < 0:
                hS += q

            if hS == hW:
                colisions += 1
                j = 0
                while j < N and S[m + j] == template[j]:
                    j += 1
                    iterations += 1

                if j == N:
                    counter += 1

            iterations += 1

        return counter, iterations, colisions

    @staticmethod
    def create_T_table(W):
        pos, cnd = 1, 0
        N = len(W)
        T = [0] * N

        while pos < N:
            if W[pos] == W[cnd]:
                T[pos] = cnd + 1
                cnd, pos = cnd + 1, pos + 1
            elif cnd == 0:
                T[pos] = 0
                pos += 1
            else:
                cnd = T[cnd - 1]

        return T

    def kmp_method(self, W):
        T = self.create_T_table(W)
        S = self.text
        M, N = len(S), len(W)
        m, i, counter, iterations = 0, 0, 0, 0

        while m < M:
            iterations += 1
            if S[m] == W[i]:
                m, i = m+1, i+1
            if i == N:
                counter += 1
                i = T[i-1]
            elif m < M and W[i] != S[m]:
                if i != 0:
                    i = T[i-1]
                else:
                    m += 1

        return counter, iterations


def main():
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()

    S = ''.join(text).lower()

    test = TextAlgorithms(S)
    W = "time."

    # Rozwiązania naiwną metodą
    solutions, iterations = test.naive_method(W)
    print(f"{solutions}; {iterations}")

    # Rozwiązania rabin_karp rolling hash
    rabin_sol, rabin_iter, rabin_accidents = test.rabin_karp_method(W)
    print(f"{rabin_sol}; {rabin_iter}; {rabin_accidents}")

    # Rozwiązania metodą KMP
    kmp_sol, kmp_iterations = test.kmp_method(W)
    print(f"{kmp_sol}; {kmp_iterations}")


if __name__ == '__main__':
    main()