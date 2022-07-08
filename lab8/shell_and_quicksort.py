# skończone

from random import randint
import time


class SortingMethods:

    def __init__(self, lst):
        self.lst = lst

    def shell_sort_normal(self):
        n = len(self.lst)

        h = n // 2

        while h > 0:
            for i in range(h, n):
                j = i-h
                shift_el = self.lst[i]

                while j >= 0 and self.lst[j] > shift_el:
                    self.lst[j+h] = self.lst[j]
                    j -= h

                self.lst[j+h] = shift_el
            h //= 2

    def find_best_h(self):
        n, h = len(self.lst), 1
        for k in range(2, n):
            h = (3**k - 1) / 2
            if h > n/3:  # koryguje, bo robiła się o 1 iteracja za dużo
                h = (3**(k-1) - 1) // 2
                break

        return h

    def shell_sort_better_h(self):
        n = len(self.lst)
        h = self.find_best_h()

        while h > 0:
            for i in range(h, n):
                j = i-h
                shift_el = self.lst[i]

                while j >= 0 and self.lst[j] > shift_el:
                    self.lst[j+h] = self.lst[j]
                    j -= h

                self.lst[j+h] = shift_el
            h //= 3

    def quicksort(self, arr):
        smaller, equal, higher = [], [], []

        if len(arr) > 1:
            pivot = arr[0]  # pierwszy element jest zawsze pivotem
            for element in arr:
                if element < pivot:
                    smaller.append(element)
                elif element == pivot:
                    equal.append(element)
                else:
                    higher.append(element)

            return self.quicksort(smaller) + equal + self.quicksort(higher)
        else:
            return arr

    def find_best_pivot(self, arr):
        n = len(arr)
        i = n // 5  # ile jest podlist 5 elementowych
        k = n % 5  # ilość elementów w ostatniej podliście
        new_lst = []

        if len(arr) > 1:
            if i >= 1:
                for i in range(0, 5*i-4, 5):
                    el = self.median_5(arr[i], arr[i+1], arr[i+2], arr[i+3], arr[i+4])
                    new_lst.append(el)

                if k == 1:
                    new_lst.append(arr[-1])
                elif k == 2:
                    el = self.median_2(arr[-1], arr[-2])
                    new_lst.append(el)
                elif k == 3:
                    el = self.median_3(arr[-1], arr[-2], arr[-3])
                    new_lst.append(el)
                elif k == 4:
                    el = self.median_4(arr[-1], arr[-2], arr[-3], arr[-4])
                    new_lst.append(el)

            else:
                if k == 2:
                    return self.median_2(arr[0], arr[1])
                elif k == 3:
                    return self.median_3(arr[0], arr[1], arr[2])
                elif k == 4:
                    return self.median_4(arr[0], arr[1], arr[2], arr[3])

            return self.find_best_pivot(new_lst)

        else:
            return arr[0]

    @staticmethod
    def median_2(a, b):  # mediana to nie może być średnia
        return min(a, b)

    @staticmethod
    def median_3(a, b, c):
        return max(min(a, b), min(c, max(a, b)))

    @staticmethod
    def median_4(a, b, c, d):
        return max(min(a, b), min(c, max(a, b)), min(d, max(b, c)))

    def median_5(self, a, b, c, d, e):
        f = max(min(a, b), min(c, d))
        g = min(max(a, b), max(c, d))
        return self.median_3(e, f, g)

    def quicksort_by_magic_five(self, arr):
        smaller, equal, higher = [], [], []
        used_time_to_find_pivot = 0

        if len(arr) > 1:
            t_start = time.perf_counter()
            pivot = self.find_best_pivot(arr)
            t_stop = time.perf_counter()

            used_time_to_find_pivot += (t_stop - t_start)

            for element in arr:
                if element < pivot:
                    smaller.append(element)
                elif element == pivot:
                    equal.append(element)
                else:
                    higher.append(element)

            return self.quicksort_by_magic_five(smaller) + equal + self.quicksort_by_magic_five(higher)
        else:
            return arr

    def check_is_it_sorted(self):
        print(self.lst)


def test1(method):
    N = 10000
    lst = [randint(0, 99) for _ in range(N)]

    if method == 1:  # Shell sort -> h = N/2, i h //= 2
        s = SortingMethods(lst)
        t_start = time.perf_counter()
        s.shell_sort_normal()
        t_stop = time.perf_counter()
        print("Czas obliczeń zwykłym sortowaniem Shella:   ", "{:.7f}".format(t_stop - t_start))

    elif method == 2:  # Shell sort -> h = (3**k - 1)/ 2 < N/3, i h//=3
        s = SortingMethods(lst)
        t_start = time.perf_counter()
        s.shell_sort_better_h()
        t_stop = time.perf_counter()
        print("Czas obliczeń ulepszonym sortowaniem Shella:", "{:.7f}".format(t_stop - t_start))

    elif method == 3:  # Zwykły quicksort
        s = SortingMethods(lst)
        t_start = time.perf_counter()
        s.quicksort(lst)
        t_stop = time.perf_counter()
        print("Czas obliczeń quicksortem:              ", "{:.7f}".format(t_stop - t_start))

    elif method == 4:  # Quicksort median median
        s = SortingMethods(lst)
        t_start = time.perf_counter()
        s.quicksort_by_magic_five(lst)
        t_stop = time.perf_counter()
        print("Czas obliczeń quicksortem median median:", "{:.7f}".format(t_stop - t_start))


def main():
    test1(1)  # sortowanie shella dla zwykłego h
    test1(2)  # sortowanie shella dla lepszego h
    print('')
    test1(3)
    test1(4)


if __name__ == '__main__':
    main()

# Czas quciksorta, który wyszukuje najlepszy pivot jest nieco dłuższy.
# Wydaje mi się jednak, że może to być spowodowane tym, iż w każdej iteracji jest szukany nowy najlepszy pivot i
# na jego znalezienia schodzi większa ilość czasu. Metoda ta wydaje się działać poprawnie i jest zaimplementowana
# identycznie jak zwykły quicksort, więc ten powód wydaje się być jedynym sensownym.