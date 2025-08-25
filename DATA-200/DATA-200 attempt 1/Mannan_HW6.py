MAX_SIZE = 200

# Define the class Node which will have left, right, and data
class Node:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

# You need a queue to maintain FIFO
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
        return Node(data)
     
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
        self.queue.array[self.queue.rear] = root  # Store actual node
    
        if self.queue.front == -1:
            self.queue.front = 0  # Ensure the queue is initialized
 
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
        if self._isEmpty():
            return None
        return self.queue.array[self.queue.front]  # Should return a valid Node
 
    def _hasBothChild(self, temp):
        return temp and temp.left and temp.right
     
    # Function to insert a new node in a complete binary tree 
    def insert(self, root, data):
        temp = self.newNode(data) 
        if not root:
            return temp
        else:
            front = self._getFront()
            if front is None:  # If the queue is empty, assign root
                return temp
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

    def _inorder(self, root, row, col, height, matrix):
        if not root:
            return
        offset = 2 ** (height - row - 1)
        if root.left:
            self._inorder(root.left, row + 1, col - offset, height, matrix)
        matrix[row][col] = str(root.data)
        if root.right:
            self._inorder(root.right, row + 1, col + offset, height, matrix)

    def _preOrder(self, root, ans):
        if root:
            ans.append(str(root.data))
            self._preOrder(root.left, ans)
            self._preOrder(root.right, ans)
        return ans

    def _eulerOrder(self, root, ans):
        if root:
            ans.append(str(root.data))
            if root.left:
                self._eulerOrder(root.left, ans)
                ans.append(str(root.data))
            if root.right:
                self._eulerOrder(root.right, ans)
                ans.append(str(root.data))
        return ans

    def bfsOrder(self, root):
        if not root:
            return []
        queue = [root]
        ans = []
        while queue:
            node = queue.pop(0)
            ans.append(str(node.data))
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return ans

    def convertTreeToMatrix(self, root):
        tHeight = self._find_height(root)
        tRows = tHeight + 1
        tCols = 2 ** (tHeight + 1) - 1
        tMatrix = [["" for _ in range(tCols)] for _ in range(tRows)]
        self._inorder(root, 0, (tCols - 1) // 2, tHeight, tMatrix)
        return tMatrix

    def printMatrix(self, arr):
        for row in arr:
            print(" ".join(cell if cell else " " for cell in row))

def binaryTree():
    root = None
    binTree = BinaryTree()
    for i in range(1, 16):
        root = binTree.insert(root, i)
    
    result = binTree.convertTreeToMatrix(root)
    binTree.printMatrix(result)
    
    print("\nPreOrder Traversal:", " ".join(binTree._preOrder(root, [])))
    print("Euler Order Traversal:", " ".join(binTree._eulerOrder(root, [])))
    print("BFS Order Traversal:", " ".join(binTree.bfsOrder(root)))

def main():
    binaryTree()

if __name__ == "__main__":
    main()
