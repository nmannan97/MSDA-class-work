class quickSort:

    def __init__(self):
        self.array = [23, 6, 4, -1, 0, 12, 8, 3, 1]

    def sort(self, List=[], i=-1, j=0, pivot=0, count=0):
        pivot = len(List) - 1
        if (len(List) - 1 == j):
            #print("Piviting at Len")
            List[i + 1], List[j] = List[j], List[i + 1]
            #print(List)       
            return self.sort(List, pivot=pivot)

        elif (List[j] <= List[pivot]):
            #print("Entering pivot")
            i += 1 
            List[i], List[j] = List[j], List[i]
            #print(List)
            #print("i & j", i, j)
            count += 1
            if (count == len(List) - 1):
                return List
            return self.sort(List, i, j=j+1, pivot=pivot, count=count)

        elif (List[j] > List[pivot]):
            #print("Entering pivot part B")
            #print(List)
            return self.sort(List, i, j=j+1, pivot=pivot)

class Node:
    def __init__(self, data, parent=None):
        self.data = data
        self.left_node = None
        self.right_node = None
        self.parent = parent

class BST:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = Node(data)
            print(self.root)
        else:
            bst = self.root
            while True:
                if data < bst.data:
                    if bst.left_node is None:
                        bst.left_node = Node(data, bst)
                        return
                    else:
                        bst = bst.left_node

                elif data > bst.data:
                    if bst.right_node is None:
                        bst.right_node = Node(data, bst)
                        return
                    else:
                        bst = bst.right_node

    def insert_node(self, data, node):
        if data < node.data:
            if node.left_node:
                self.insert_node(data, node.left_node)
            else:
                node.left_node = Node(data, node)
        elif data > node.data:
            if node.right_node:
                self.insert_node(data, node.right_node)
            else:
                node.right_node = Node(data, node)

    def get_min(self):
        if self.root:
            return self.get_min_value(self.root)

    def get_min_value(self, node):
        while node.left_node:
            node = node.left_node
        return node.data

    def get_max(self):
        if self.root:
            return self.get_max_value(self.root)

    def get_max_value(self, node):
        while node.right_node:
            node = node.right_node
        return node.data

    def traverse_in_order(self, node):
        if node is None:
            return
        self.traverse_in_order(node.left_node)
        print(node.data, end=" ")
        self.traverse_in_order(node.right_node)

    def remove(self, data):
        if self.root:
            self.root = self.remove_node(data, self.root)

    def remove_node(self, data, node):
        if node is None:
            return node

        if data < node.data:
            node.left_node = self.remove_node(data, node.left_node)
        elif data > node.data:
            node.right_node = self.remove_node(data, node.right_node)
        else:
            # Node with no children
            if node.left_node is None and node.right_node is None:
                return None
            # Node with one child
            if node.left_node is None:
                return node.right_node
            elif node.right_node is None:
                return node.left_node

            # Node with two children
            predecessor = self.get_predecessor(node.left_node)
            node.data = predecessor.data
            node.left_node = self.remove_node(predecessor.data, node.left_node)

        return node

    def get_predecessor(self, node):
        while node.right_node:
            node = node.right_node
        return node

if __name__ == "__main__":
    bst=BST()
    bst.insert(10)
    bst.insert(5)
    bst.insert(8)
    bst.insert(12)
    bst.insert(-5)
    bst.insert(44)
    bst.insert(-12)
    bst.insert(19)
    bst.insert(22)

    bst.traverse_in_order(bst.root)
    print(" ")
    bst.remove(10)

    bst.traverse_in_order(bst.root)
    print(" ")

    Sort = quickSort()

    print("output quick sort: ", Sort.sort(Sort.array))
