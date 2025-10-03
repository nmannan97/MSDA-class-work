MAX_SIZE = 200

# Define the class Node which will have left,right and data
class node:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

# You need queue to maintain FIFO
class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
        self.array = []

# Class Binary Tree
class BinaryTree:
    def __init__(self):
        self.queue = Queue()
        self.queue.front = self.queue.rear = -1
        self.queue.size = MAX_SIZE
        self.queue.array = [None for _ in range(self.queue.size)]

    def newNode(self, data):
        return node(data)

    # Standard Queue Functions 
    def _isEmpty(self):
        return self.queue.front == -1

    def _isFull(self):
        return self.queue.rear == self.queue.size - 1

    def _hasOnlyOneItem(self):
        return self.queue.front == self.queue.rear

    def _Enqueue(self, root):
        if self._isFull():
            return
        self.queue.rear += 1
        self.queue.array[self.queue.rear] = root
        if self._isEmpty():
            self.queue.front += 1

    def _Dequeue(self):
        if self._isEmpty():
            return None
        temp = self.queue.array[self.queue.front]
        if self._hasOnlyOneItem():
            self.queue.front = self.queue.rear = -1
        else:
            self.queue.front += 1
        return temp

    def _getFront(self):
        return self.queue.array[self.queue.front]

    def _hasBothChild(self, temp):
        return temp and temp.left and temp.right

    def insert(self, root, data):
        temp = self.newNode(data)
        if not root:
            root = temp
        else:
            front = self._getFront()
            if not front.left:
                front.left = temp
            elif not front.right:
                front.right = temp
            if self._hasBothChild(front):
                self._Dequeue()
        self._Enqueue(temp)
        return root

    def _find_height(self, root):
        if not root:
            return -1
        left_height = self._find_height(root.left)
        right_height = self._find_height(root.right)
        return max(left_height, right_height) + 1

    def _inorder(self, root, tRow, tCol, tHeight, tMatrix):
        if not root:
            return
        tMatrix[tRow][tCol] = str(root.data)
        offset = 2 ** (tHeight - tRow - 1) if tHeight - tRow - 1 >= 0 else 0
        self._inorder(root.left, tRow + 1, tCol - offset, tHeight, tMatrix)
        self._inorder(root.right, tRow + 1, tCol + offset, tHeight, tMatrix)

    def _preOrder(self, root, row, col, height, ans):
        if not root:
            return
        ans.append(root.data)
        self._preOrder(root.left, row + 1, col - 1, height, ans)
        self._preOrder(root.right, row + 1, col + 1, height, ans)

    def _postOrder(self, root, row, col, height, ans):
        if not root:
            return
        self._postOrder(root.left, row + 1, col - 1, height, ans)
        self._postOrder(root.right, row + 1, col + 1, height, ans)
        ans.append(root.data)

    def _eulerOrder(self, root, row, col, height, ans):
        if not root:
            return
        ans.append(root.data)
        self._eulerOrder(root.left, row + 1, col - 1, height, ans)
        ans.append(root.data)
        self._eulerOrder(root.right, row + 1, col + 1, height, ans)
        ans.append(root.data)

    def bfsOrder(self, root, row, col, height, ans):
        if not root:
            return
        q = [root]
        while q:
            node_ = q.pop(0)
            ans.append(node_.data)
            if node_.left:
                q.append(node_.left)
            if node_.right:
                q.append(node_.right)

    def convertTreeToMatrix(self, root):
        tHeight = self._find_height(root)
        tRows = tHeight + 1
        tCols = 2 ** (tHeight + 1) - 1
        tMatrix = [["" for _ in range(tCols)] for _ in range(tRows)]
        self._inorder(root, 0, (tCols - 1) // 2, tHeight, tMatrix)
        return tMatrix

    def printMatrix(self, arr):
        for row in arr:
            for cell in row:
                print(cell if cell != "" else " ", end="")
            print()

def binaryTree():
    root = None
    binTree = BinaryTree()
    for i in range(1, 16):
        root = binTree.insert(root, i)

    print("\nPreOrder:")
    pre = []
    binTree._preOrder(root, 0, 0, 0, pre)
    print(pre)

    print("\nPostOrder:")
    post = []
    binTree._postOrder(root, 0, 0, 0, post)
    print(post)

    print("\nEulerOrder:")
    euler = []
    binTree._eulerOrder(root, 0, 0, 0, euler)
    print(euler)

    print("\nBFS Order:")
    bfs = []
    binTree.bfsOrder(root, 0, 0, 0, bfs)
    print(bfs)

    print("\nTree Structure:")
    result = binTree.convertTreeToMatrix(root)
    binTree.printMatrix(result)

if __name__ == "__main__":
    binaryTree()
