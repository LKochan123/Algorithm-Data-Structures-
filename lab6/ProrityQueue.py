# skończone


class PriorityQueue:

    def __init__(self):
        self.lst = []
        self.size = 0

    def is_empty(self):
        if self.size == 0:
            return True
        return False

    def peek(self):
        if not self.is_empty():
            return self.lst[0].data  # najwiekszy element zawsze bedzie na poczatku naszej listy

    def dequeue(self):
        if self.is_empty():
            return None

        elif self.size == 1:
            data = self.lst[0].data
            self.lst.pop()
            self.size -= 1
            return data

        else:
            delete_element = self.lst[0].data
            last_element = self.lst.pop()
            self.lst[0] = last_element
            self.size -= 1

            actual_element = 0
            left_child = self.left(actual_element)
            right_child = self.right(actual_element)

            while left_child <= self.size - 1:
                if (right_child <= self.size-1) and (self.lst[right_child] > self.lst[left_child]):
                    if self.lst[actual_element] < self.lst[right_child]:
                        self.lst[actual_element], self.lst[right_child] = self.lst[right_child], self.lst[actual_element]
                        actual_element = right_child
                        left_child = self.left(actual_element)
                        right_child = self.right(actual_element)
                    else:
                        break
                else:
                    if right_child > self.size - 1:  # rodzic ma tylko lewego syna
                        if self.lst[actual_element] < self.lst[left_child]:
                            self.lst[actual_element], self.lst[left_child] = self.lst[left_child], self.lst[actual_element]
                            actual_element = left_child
                            left_child = self.left(actual_element)
                            right_child = self.right(actual_element)
                        else:
                            break
                    elif self.lst[left_child].priority >= self.lst[right_child].priority:
                        if self.lst[actual_element] < self.lst[left_child]:
                            self.lst[actual_element], self.lst[left_child] = self.lst[left_child], self.lst[actual_element]
                            actual_element = left_child
                            left_child = self.left(actual_element)
                            right_child = self.right(actual_element)
                        else:
                            break

        return delete_element

    def enqueue(self, priority, data):
        if self.is_empty():
            new_el = Element(priority, data)
            self.lst.append(new_el)
            self.size += 1
        else:
            new_element = Element(priority, data)
            self.lst.append(new_element)
            self.size += 1

            n = self.size - 1  # indeks ostatnio wstawionego wierzcholka
            idx_parent = self.parent(n)

            while self.lst[n] > self.lst[idx_parent]:  # sprawdzamy po kolei wszystkich rodzicow
                self.lst[n], self.lst[idx_parent] = self.lst[idx_parent], self.lst[n]
                n = idx_parent
                idx_parent = self.parent(idx_parent)

    def left(self, idx):
        n = 2*idx + 1
        return n

    def right(self, idx):
        n = 2*idx+2
        return n

    def parent(self, idx):
        n = int((idx-1)/2)
        return n

    def print_tab(self):
        if self.is_empty():
            print('{}')
        else:
            print ('{', end='')
            for i in range(self.size-1):
                print(self.lst[i], end = ', ')
            if self.lst[self.size-1]: print(self.lst[self.size-1] , end = '')
            print('}')

    def print_tree(self, idx, lvl):
        if idx < self.size:
            self.print_tree(self.right(idx), lvl+1)
            print(2*lvl*'  ', self.lst[idx] if self.lst[idx] else None)
            self.print_tree(self.left(idx), lvl+1)


class Element:

    def __init__(self, priority, data):
        self.priority = priority
        self.data = data

    def __gt__(self, other):  # grater than >
        if self.priority > other:
            return True
        return False

    def __lt__(self, other):  # lower than <
        if self.priority < other:
            return True
        return False

    def __str__(self):
        return f"{self.priority}: {self.data}"


if __name__ == '__main__':
    k = PriorityQueue()
    lst = [4, 7, 6, 7, 5, 2, 2, 1]
    str1 = "ALGORYTM"

    for i in range(len(lst)):
        k.enqueue(lst[i], str1[i])
        
    k.print_tree(0, 0)
    k.print_tab()
    print(k.dequeue())
    print(k.peek())
    k.print_tab()

    while not k.is_empty():
        print(k.dequeue())

    k.print_tab()