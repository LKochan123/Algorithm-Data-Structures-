# skończone
import time
from math import log as ln


class TextAlgorithms:

    def __init__(self, text):
        self.text = text

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

    def SET_rabin_karp(self, set_of_strings, N):
        S, M = self.text, len(self.text)
        q, d, h = 101, 256, 1
        P, n = 0.001, 20
        b, k = self.calculate_k_and_b(P, n)
        counter, fake_info = 0, 0

        bloom_subs = [0] * b

        for i in range(N-1):
            h = (h * d) % q

        for template in set_of_strings:
            bloom_subs[self.hash(template)] = 1

        hS = self.hash(S[:N])
        for m in range(1, M-N+1):
            hS = (d * (hS - ord(S[m - 1]) * h) + ord(S[m + N - 1])) % q
            if bloom_subs[hS]:
                fake_info += 1
                if S[m:m+N] in set_of_strings:
                    counter += 1

        fake_info -= counter

        return counter, fake_info

    @staticmethod
    def calculate_k_and_b(P, n):
        b = -n * ln(P)/ln(2)**2
        k = b/n * ln(2)
        return int(b), int(k)


def main():
    with open("lotr.txt", encoding='utf-8') as f:
        text = f.readlines()

    S = ''.join(text).lower()

    test = TextAlgorithms(S)
    W = "gandalf"

    t_start = time.perf_counter()
    rabin_sol, rabin_iter, rabin_accidents = test.rabin_karp_method(W)
    t_stop = time.perf_counter()

    print(f'Wyniki dla 1 wzorca:')
    print(f"- liczba wystąpień słowa {W}: {rabin_sol}")
    print("- czas obliczeń:", "{:.7f}".format(t_stop - t_start))
    print("")

    set_of_strings = ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred',
                      'hobbits', 'however', 'popular', 'nothing', 'enjoyed', 'stuffed',  'relaxed',
                      'himself', 'present', 'deliver', 'welcome', 'baggins', 'further']

    n = 7
    t_start1 = time.perf_counter()
    solutions, fake_info = test.SET_rabin_karp(set_of_strings, n)
    t_stop1 = time.perf_counter()
    print(f'Wyniki dla {len(set_of_strings)} wzorców:')
    print(f'- liczba wystąpień wzorców: {solutions}')
    print(f"- detekcje fałszywe: {fake_info}")
    print("- czas obliczeń:", "{:.7f}".format(t_stop1 - t_start1))

    # Możemy zauważyć, że czas wyszukiwania dla wielu słów jest niemal identyczny.
    # Nie wzrósł on n-krotnie, także algorytm wydaje się działać poprawnie.


if __name__ == '__main__':
    main()