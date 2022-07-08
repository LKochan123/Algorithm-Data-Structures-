#skończone

class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self):
        self.head = None

    def destroy(self):  # destroy all linkedlist
        self.head = None

    def add(self, data):  # insert at 0 index
        new_node = Node(data, self.head)
        self.head = new_node

    def remove(self):  # destroy element at index 0
        self.head = self.head.next

    def is_empty(self):
        if LinkedList.length(self) == 0:
            return True
        else:
            return False

    def length(self):
        act_itr = self.head
        how_many = 0

        while act_itr:
            act_itr = act_itr.next
            how_many += 1

        return how_many

    def get(self):
        return self.head.data

    def print_method(self):
        to_string = ''
        act_itr = self.head

        while act_itr:
            to_string += str(act_itr.data) + '-->'
            act_itr = act_itr.next

        print(to_string)

    def insert_at_the_end(self, data):
        act_itr = self.head
        i = 0
        n = LinkedList.length(self)

        while act_itr:
            act_itr = act_itr.next
            i += 1
            if i == n - 1:
                new_node = Node(data, None)
                act_itr.next = new_node

    def delete_el_at_the_end(self):
        act_itr = self.head
        n = LinkedList.length(self)
        i = 0

        while act_itr:
            act_itr = act_itr.next
            i += 1
            if i == n - 2:
                act_itr.next = None

    def taken(self, n: int):
        lst_2 = LinkedList()
        act_itr = self.head
        i = 0
        help_lst = []

        if n < 1:
            return Exception('N should be >= 1')
        else:
            while act_itr:
                if i < n:
                    help_lst.append(act_itr.data)
                i += 1
                act_itr = act_itr.next

        for j in range(len(help_lst)-1, -1, -1):
            lst_2.add(help_lst[j])

        return lst_2

    def drop(self, n: int):
        lst_3 = LinkedList()
        act_itr = self.head
        help_lst = []
        i = 0

        if n > LinkedList.length(self):
            return LinkedList()
        else:
            while act_itr:
                if i >= n:
                    help_lst.append(act_itr.data)

                i += 1
                act_itr = act_itr.next

        for j in range(len(help_lst)-1, -1, -1):
            lst_3.add(help_lst[j])

        return lst_3


if __name__ == '__main__':
    lst = LinkedList()
    test_lst = [('AGH', 'Kraków', 1919), ('UJ', 'Kraków', 1364),
                ('PW', 'Warszawa', 1915), ('UW', 'Warszawa', 1915),
                ('UP', 'Poznań', 1919), ('PG', 'Gdańsk', 1945)]

    for i in reversed(test_lst):
        lst.add(i)

    print('Test wypisania listy wiązanej: ')
    lst.print_method(), print("")

    lst.remove(), print('Test metody remove: ')
    lst.print_method(), print("")

    lst.insert_at_the_end(66), print('Test metody insert_at_the_end: ')
    lst.print_method(), print("")

    lst.delete_el_at_the_end(), print('Test metody delete_el_at_the_end: ')
    lst.print_method(), print("")

    print(f'Test metody is_empty: {lst.is_empty()}')
    print(f'Test metody length: {lst.length()}')
    print(f'Test metody get: {lst.get()}'), print("")

    n = 3
    k = lst.taken(n)
    print(f'Test metody taken dla n={n}: ')
    k.print_method(), print("")

    t = lst.drop(n)
    print(f'Test metody drop dla n={n}')
    t.print_method()