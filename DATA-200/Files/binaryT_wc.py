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
        self.queue = Queue();
        self.queue.front = self.queue.rear = -1; 
        self.queue.size = MAX_SIZE; 
        self.queue.array = [None for i in range(self.queue.size)]

    def newNode(self,data):
        temp = node(data)
        return temp
     
    # Standard Queue Functions 
    def _isEmpty(self):
        return self.queue.front == -1       
 
    def _isFull(self):
         return self.queue.rear == self.queue.size - 1; 
 
    def _hasOnlyOneItem(self):
        return self.queue.front == self.queue.rear; 
 
    def _Enqueue(self,root):
        if (self._isFull()):
            return; 
        self.queue.rear+=1
        self.queue.array[self.queue.rear] = root; 
    
        if (self._isEmpty()):
            self.queue.front+=1; 
 
    def _Dequeue(self):
        if (self._isEmpty()):
            return None; 
        temp = self.queue.array[self.queue.front]; 
    
        if(self._hasOnlyOneItem()):
            self.queue.front = self.queue.rear = -1; 
        else:
            self.queue.front+=1
    
        return temp; 
 
    def _getFront(self):
        return self.queue.array[self.queue.front];
 

    def _hasBothChild(self,temp):
        return (temp and temp.left and
                temp.right); 
     
    # Function to insert a new node in complete binary tree 
    def insert(self,root, data):
        # Create a new node for given data 
        temp = self.newNode(data); 
        # If the tree is empty, initialize the root with new node. 
        if not root:
            root = temp
        else:
            # get the front node of the queue. 
            front = self._getFront(); 
            # If the left child of this front node doesn’t exist,set the left child as the new node 
            if (not front.left):
                front.left = temp; 
            # If the right child of this front node doesn’t exist, set the right child as the new node 
            elif (not front.right):
                front.right = temp; 
            # If the front node has both the left child and right child, _Dequeue() it. 
            if (self._hasBothChild(front)): 
                self._Dequeue()
    
        # _Enqueue() the new node for later insertions 
        self._Enqueue(temp); 
        return root
   

    def _find_height(self,root):
        if not root:
            return -1
        left_height = self._find_height(root.left)
        right_height = self._find_height(root.right)

        return max(left_height, right_height) + 1

    def _inorder(self,root, tRow, tCol, tHeight, tMatrix):
       pass
            

    def _preOrder(self,root, row, col, height, ans):
         pass

    def _postOrder(self,root, row, col, height, ans):
        pass

    def _eulerOrder(self,root, row, col, height, ans):
        pass

    def bfsOrder(self,root, row, col, height, ans):
        pass

    def convertTreeToMatrix(self,root):
        tHeight = self._find_height(root)
        # Rows are height + 1; nodes are 2^(height+1) - 1
        tRows = tHeight + 1
        tCols = 2 ** (tHeight + 1) - 1
        # Initialize 2D matrix with empty strings
        tMatrix = [["" for _ in range(tCols)] for _ in range(tRows)]
        # Populate the matrix using _inorder traversal
        self._inorder(root, 0, (tCols - 1) // 2, tHeight, tMatrix)
        return tMatrix

    def printMatrix(self,arr):
        for row in arr:
            for cell in row:
                if cell == "":
                    print(" ", end="")
                else:
                    print(cell, end="")
            print()

def binaryTree():
   root = None
   binTree=BinaryTree()
   for i in range(1, 16):
        root=binTree.insert(root,i); 
      
   result=binTree.convertTreeToMatrix(root)
   binTree.printMatrix(result)


# Main
if __name__ == "__main__":
   # Calling binaryTree
   binaryTree()
     


