class Node:
    def __init__(self,data,parent=None):
        self.data=data
        self.left_node= None
        self.right_node= None
        self.parent= parent
class BST:
    def __init__(self):
        self.root=None

    def insert(self,data):
        pass


    def insert_node(self,data,node):
        pass

    def get_min(self):
      pass
        

    def get_min_value(self,node):
        pass
        
  

    def get_max(self):
        pass
        

    def get_max_value(self,node):
        pass
    
    def traverse_in_order(self,node):
        pass

    def remove(self,data):
        pass

    def remove_node(self,data,node):
        pass
      

    def get_predecessor(self,node):
      pass



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

    bst.remove(10)


    bst.traverse_in_order(bst.root)
