# skończone

from random import randint
import time


class PriorityQueue:

    def __init__(self, lst=None):
        self.lst = lst
        if lst is not None:
            self.size = len(lst)

    def is_empty(self):
        if self.size == 0:
            return True
        return False

    def peek(self):
        if not self.is_empty():
            return self.lst[0].data  # najwiekszy element zawsze bedzie na poczatku naszej listy

    def enqueue(self, priority, data):
        if self.is_empty():
            new_el = Element(priority, data)
            self.lst.append(new_el)
        else:
            new_element = Element(priority, data)
            self.lst.append(new_element)

            n = self.size - 1  # indeks ostatnio wstawionego wierzcholka
            idx_parent = self.parent(n)

            while self.lst[n] > self.lst[idx_parent]:  # sprawdzamy po kolei wszystkich rodzicow
                self.lst[n], self.lst[idx_parent] = self.lst[idx_parent], self.lst[n]
                n = idx_parent
                idx_parent = self.parent(idx_parent)

    def left(self, idx):
        n = 2 * idx + 1
        return n

    def right(self, idx):
        n = 2 * idx + 2
        return n

    def parent(self, idx):
        n = int((idx - 1) / 2)
        return n

    def print_tab(self):
        if self.is_empty():
            print('{}')
        else:
            print('{', end='')
            for i in range(self.size - 1):
                print(self.lst[i], end=', ')
            if self.lst[self.size - 1]: print(self.lst[self.size - 1], end='')
            print('}')

    def print_tree(self, idx, lvl):
        if idx < self.size:
            self.print_tree(self.right(idx), lvl + 1)
            print(2 * lvl * '  ', self.lst[idx] if self.lst[idx] else None)
            self.print_tree(self.left(idx), lvl + 1)

    def dequeue_idx(self, idx, size):

        actual_element = idx
        left_child = self.left(actual_element)
        right_child = self.right(actual_element)

        while left_child < size:
            if right_child < size and (self.lst[right_child] > self.lst[left_child]):  # prawe dziecko większe
                if self.lst[actual_element] < self.lst[right_child]:
                    self.lst[actual_element], self.lst[right_child] = self.lst[right_child], self.lst[actual_element]
                    actual_element = right_child
                    left_child = self.left(actual_element)
                    right_child = self.right(actual_element)
                else:
                    break
            else:  # lewe dziecko wieksze
                if right_child >= size:  # rodzic ma tylko lewego syna
                    if self.lst[actual_element] < self.lst[left_child]:
                        self.lst[actual_element], self.lst[left_child] = self.lst[left_child], self.lst[actual_element]
                        actual_element = left_child
                        left_child = self.left(actual_element)
                        right_child = self.right(actual_element)
                    else:
                        break
                elif self.lst[left_child] >= self.lst[right_child]:
                    if self.lst[actual_element] < self.lst[left_child]:
                        self.lst[actual_element], self.lst[left_child] = self.lst[left_child], self.lst[actual_element]
                        actual_element = left_child
                        left_child = self.left(actual_element)
                        right_child = self.right(actual_element)
                    else:
                        break

    def print(self):  # można sprawdzić czy posortuje zwykłą listę
        print(self.lst)

    def get_all_parents_idx(self):
        last_el = self.size - 1
        oldest_parent = self.parent(last_el)

        all_parents = [i for i in range(oldest_parent+1)]

        return all_parents[::-1]  # odwracanie listy

    def heapify(self):
        parents = self.get_all_parents_idx()

        for i in parents:
            self.dequeue_idx(i, self.size)

    def sort(self):
        n = self.size

        for i in range(n):
           self.lst[0], self.lst[-(i+1)] = self.lst[-(i+1)], self.lst[0]
           self.dequeue_idx(0, n-(i+1))

        return self.lst

    def add_elements(self, tab):
        n = len(tab)
        for i in range(n):
            key, val = tab[i]
            tab[i] = Element(key, val)

        return tab

    def sorting_by_swap(self):
        n = len(self.lst)

        for i in range(n):
            min_el_idx = i
            for j in range(i+1, n):
                if self.lst[j] < self.lst[min_el_idx]:
                    min_el_idx = j

            self.lst[min_el_idx], self.lst[i] = self.lst[i], self.lst[min_el_idx]

    def sorting_by_shift(self):
        n = len(self.lst)

        for i in range(1, n):
            j = i - 1
            shift_el = self.lst[i]

            while j >= 0 and self.lst[j] > shift_el:
                self.lst[j+1] = self.lst[j]
                j -= 1

            self.lst[j+1] = shift_el


class Element:

    def __init__(self, priority, data):
        self.priority = priority
        self.data = data

    def __gt__(self, other):  # grater than >
        if self.priority > other.priority:
            return True
        return False

    def __lt__(self, other):  # lower than <
        if self.priority < other.priority:
            return True
        return False

    def __ge__(self, other):
        if self.priority >= other.priority:
            return True
        return False

    def __str__(self):
        return f"{self.priority}: {self.data}"


def test1(method=1):  # 1 - kopcowanie, 2 - swap, 3 - shift
    lst = [(5, 'A'), (5, 'B'), (7, 'C'), (2, 'D'), (5, 'E'), (1, 'F'), (7, 'G'), (5, 'H'), (1, 'I'), (2, 'J')]

    if method == 1:
        k_temp = PriorityQueue()
        tab = k_temp.add_elements(lst)
        k_test = PriorityQueue(tab)
        k_test.heapify()
        k_test.print_tab()
        k_test.print_tree(0, 0)
        k_test.sort()
        k_test.print_tab()

    elif method == 2:
        k_temp = PriorityQueue()
        tab = k_temp.add_elements(lst)
        k_test = PriorityQueue(tab)
        k_test.sorting_by_swap()
        k_test.print_tab()

    elif method == 3:
        k_temp = PriorityQueue()
        tab = k_temp.add_elements(lst)
        k_test = PriorityQueue(tab)
        k_test.sorting_by_shift()
        k_test.print_tab()

    else:
        raise ValueError('Method must be number from {1, 2, 3}')


def test2(method=1):  # 1 - kopcowanie, 2 - swap, 3 - shift
    lst1 = [randint(0, 1000) for _ in range(10000)]

    if method == 1:
        lst = [randint(0, 99) for _ in range(10000)]
        k1 = PriorityQueue(lst)
        t_start = time.perf_counter()
        k1.heapify()
        k1.sort()
        t_stop = time.perf_counter()
        print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    elif method == 2:
        k1 = PriorityQueue(lst1)
        t_start = time.perf_counter()
        k1.sorting_by_swap()
        t_stop = time.perf_counter()
        print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))

    elif method == 3:
        k1 = PriorityQueue(lst1)
        t_start = time.perf_counter()
        k1.sorting_by_shift()
        t_stop = time.perf_counter()
        print("Czas obliczeń:", "{:.7f}".format(t_stop - t_start))
        
    else:
        raise ValueError('Method must be number from {1, 2, 3}')


def main():
    test1(1)  # 1 -> sortowanie przez kopcowanie
    test2(1)
    print('')
    test1(2)  # 2 -> sortowanie przez wybieranie (swap)
    test2(2)
    print('')
    test1(3)  # 3 -> sortowanie przez wstawianie (shift)
    test2(3)


if __name__ == '__main__':
    main()

# Możemy zauważyć, że sortowanie przez kopcowanie jest zdecydowanie najszybsze.