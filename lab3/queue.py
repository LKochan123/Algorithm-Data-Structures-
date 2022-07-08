# skończone, poprawa

class Queue:

    def __init__(self, size=5):
        self.size = size
        self.idx_to_save, self.idx_to_read = 0, 0
        self.lst = [None for _ in range(size)]

    def is_empty(self):
        if self.idx_to_save != self.idx_to_read:
            return False
        return True

    def peek(self):
        if self.is_empty():
            return None
        return self.lst[self.idx_to_read]

    def dequeue(self):
        if self.is_empty():
            return None
        else:
            to_return = self.lst[self.idx_to_read]
            self.lst[self.idx_to_read] = None
            self.idx_to_read += 1

            if self.idx_to_read == self.size:
                self.idx_to_read = 0

            return to_return

    def enqueue(self, data):
        if self.is_empty():
            self.lst[self.idx_to_save] = data
            self.idx_to_save += 1
        else:
            self.lst[self.idx_to_save] = data
            self.idx_to_save += 1

            if self.idx_to_save == self.idx_to_read:  # jeśli spotykają się indeksy
                k = len(self.lst)
                self.lst = Queue.realloc(self, self.lst, 2*k)

                how_many = k - self.idx_to_save
                self.lst[-how_many:], self.lst[how_many:k] = self.lst[how_many:k], self.lst[-how_many:]

                self.idx_to_read = self.idx_to_read + k
                self.size = len(self.lst)

            elif self.idx_to_save == self.size:  # przypadek, jeśli kończy nam się miejsce w wyjściowej liście
                n = self.size
                self.lst = Queue.realloc(self, self.lst, 2*n)
                self.lst[0:n], self.lst[n:] = self.lst[n:], self.lst[0:n]
                self.idx_to_read = n + self.idx_to_read
                self.idx_to_save = 0
                self.size = len(self.lst)

    def print_queue(self):
        if self.is_empty():
            print("[]")
        else:
            show_queue = '['
            start_point = self.idx_to_read

            while self.lst[start_point] is not None:
                show_queue += f'{self.lst[start_point]} '
                start_point += 1

                if start_point == self.size:
                    start_point = 0

            show_queue += ']'
            final_queue = show_queue.strip(' ]')
            final_queue += ']'

            print(final_queue)

    def print_lst(self):
        print(self.lst)

    def realloc(self, tab, size):
        oldsize = len(tab)
        return [tab[i] if i < oldsize else None for i in range(size)]


if __name__ == '__main__':
    q1 = Queue()
    for i in range(1, 5):
        q1.enqueue(i)

    print(q1.dequeue())
    print(q1.peek())
    q1.print_queue()
    
    for j in range(5, 9):
        q1.enqueue(j)

    q1.print_lst()

    while not q1.is_empty():
        print(q1.dequeue())

    q1.print_queue()