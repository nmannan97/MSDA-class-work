def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)

# Test the array
arr = [23, 6, 4, -1, 0, 12, 8, 3, 1]
sorted_arr = quick_sort(arr)
print("Sorted array:", sorted_arr)

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
        if not self.root:
            self.root = Node(data)
        else:
            self.insert_node(data, self.root)

    def insert_node(self, data, node):
        if data < node.data:
            if node.left_node:
                self.insert_node(data, node.left_node)
            else:
                node.left_node = Node(data, node)
        else:
            if node.right_node:
                self.insert_node(data, node.right_node)
            else:
                node.right_node = Node(data, node)

    def get_min(self):
        if self.root:
            return self.get_min_value(self.root)

    def get_min_value(self, node):
        if node.left_node:
            return self.get_min_value(node.left_node)
        return node.data

    def get_max(self):
        if self.root:
            return self.get_max_value(self.root)

    def get_max_value(self, node):
        if node.right_node:
            return self.get_max_value(node.right_node)
        return node.data

    def traverse_in_order(self, node):
        if node:
            self.traverse_in_order(node.left_node)
            print(node.data, end=' ')
            self.traverse_in_order(node.right_node)

    def remove(self, data):
        if self.root:
            self.root = self.remove_node(data, self.root)

    def remove_node(self, data, node):
        if not node:
            return node

        if data < node.data:
            node.left_node = self.remove_node(data, node.left_node)
        elif data > node.data:
            node.right_node = self.remove_node(data, node.right_node)
        else:
            # Node with no children
            if not node.left_node and not node.right_node:
                return None
            # Node with one child
            elif not node.left_node:
                temp = node.right_node
                temp.parent = node.parent
                return temp
            elif not node.right_node:
                temp = node.left_node
                temp.parent = node.parent
                return temp
            # Node with two children
            temp = self.get_predecessor(node.left_node)
            node.data = temp.data
            node.left_node = self.remove_node(temp.data, node.left_node)

        return node

    def get_predecessor(self, node):
        if node.right_node:
            return self.get_predecessor(node.right_node)
        return node


if __name__ == "__main__":
    bst = BST()
    bst.insert(10)
    bst.insert(5)
    bst.insert(8)
    bst.insert(12)
    bst.insert(-5)
    bst.insert(44)
    bst.insert(-12)
    bst.insert(19)
    bst.insert(22)

    print("In-order before deletion:")
    bst.traverse_in_order(bst.root)
    print("\n\nRemoving 10...\n")
    bst.remove(10)

    print("In-order after deletion:")
    bst.traverse_in_order(bst.root)