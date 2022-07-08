# skończone

class BinaryTree:

    def __init__(self):
        self.root = None

    def search(self, key):
        if self.root is None:
            return None
        elif self.root.key == key:
            return self.root.data
        else:
            return self.help_search(key, self.root)

    @staticmethod
    def help_search(key, act_node):
        while key != act_node.key:
            if key < act_node.key:
                if act_node.left_child is None:
                    break
                act_node = act_node.left_child
            elif key > act_node.key:
                if act_node.right_child is None:
                    break
                act_node = act_node.right_child

        if act_node.key == key:
            return act_node.data
        else:
            return None

    def insert(self, key, data):
        if self.root is None:
            self.root = Node(key, data)
        else:
            self.help_insert(key, data, self.root)

    def help_insert(self, key, data, act_node, parent=None):
        if key < act_node.key:
            if act_node.left_child is None:
                act_node.left_child = Node(key, data)
            else:
                self.help_insert(key, data, act_node.left_child)
        elif key > act_node.key:
            if act_node.right_child is None:
                act_node.right_child = Node(key, data)
            else:
                self.help_insert(key, data, act_node.right_child)
        else:
            act_node.key, act_node.data = key, data

    def delete(self, key):
        check = self.search(key)
        if check:
            self.help_delete(key, self.root)

    def help_delete(self, key, act_node, parent=None):
        while key != act_node.key:
            if key < act_node.key:
                parent = act_node
                act_node = act_node.left_child
            elif key > act_node.key:
                parent = act_node
                act_node = act_node.right_child

        if act_node.left_child is None and act_node.right_child is None:  # 0 dzieci
            if key < parent.key:
                parent.left_child = None
            else:
                parent.right_child = None

        elif act_node.left_child and act_node.right_child:  # 2 dzieci
            to_change, parent_changer = act_node.right_child, act_node
            while to_change.left_child:
                parent_changer = to_change  # rodzic el który trzeba zamienić
                to_change = to_change.left_child  # element który trzeba będzie zamienić
            act_node.key, act_node.data = to_change.key, to_change.data
            if to_change.right_child:
                if parent_changer.key > to_change.key:
                    parent_changer.left_child = to_change.right_child
                else:
                    parent_changer.right_child = to_change.right_child
            else:
                if to_change.key < parent_changer.key:
                    parent_changer.left_child = None
                else:
                    parent_changer.right_child = None

        elif (act_node.left_child and act_node.right_child is None) or \
                (act_node.right_child and act_node.left_child is None):  # 1 dziecko
            if key < parent.key:
                if act_node.right_child is None:
                    parent.left_child = act_node.left_child
                else:
                    parent.left_child = act_node.right_child
            else:
                if act_node.right_child is None:
                    parent.right_child = act_node.left_child
                else:
                    parent.right_child = act_node.right_child

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if None != node:
            self._print_tree(node.right_child, lvl + 5)

            print()
            print(lvl * " ", node.key, node.data)

            self._print_tree(node.left_child, lvl + 5)

    def height(self):
        if self.root is None:
            return 0
        elif self.root.left_child is None and self.root.right_child is None:
            return 1
        else:
            return self.height_help(self.root)

    def height_help(self, act_node, how_many=0):
        if act_node is None:
            return how_many
        left_child = self.height_help(act_node.left_child, how_many + 1)
        right_child = self.height_help(act_node.right_child, how_many + 1)
        return max(left_child, right_child)

    def print_like_a_list(self):
        stack, result, lst_to_print = [self.root], [], "["
        while len(stack):  # pre-order traversal
            root = stack.pop()
            result += [(root.key, root.data)]
            if root.right_child:
                stack.append(root.right_child)
            if root.left_child:
                stack.append(root.left_child)
        result.sort(key=lambda x: x[0])  # sortujemy według klucza

        for key1, value1 in result:
            lst_to_print += f"{key1}:{value1}, "
        lst_to_print = lst_to_print[0:-2]
        lst_to_print += "]"

        print(lst_to_print)


class Node:

    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left_child = None
        self.right_child = None


if __name__ == '__main__':
    d1 = {50: 'A', 15: 'B', 62: 'C', 5: 'D', 20: 'E', 58: 'F', 91: 'G', 3: 'H', 8: 'I', 37: 'J', 60: 'K', 24: 'L'}
    b = BinaryTree()
    for key, value in d1.items():
        b.insert(key, value)
    b.print_tree()
    b.print_like_a_list()
    print(b.search(24))
    b.insert(20, 'AA')
    b.insert(6, 'M')
    b.delete(62)
    b.insert(59, 'N')
    b.insert(100, 'P')
    b.delete(8)
    b.delete(15)
    b.insert(55, 'R')
    b.delete(50)
    b.delete(5)
    b.delete(24)
    print(b.height())
    b.print_like_a_list()
    b.print_tree()