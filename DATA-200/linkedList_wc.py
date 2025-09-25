# Node class to be a part of Linked List
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Create a class called LinkedList 
class LinkedList:
    def __init__(self):
        self.head = None

    # Add a node at the begining
    def add_first(self, data):
        """ Add Firdt Node"""
        if self.head is None: 
            self.head = Node(data)
            self.head.next = None
            return
        temp = self.head
        self.head = Node(data)
        self.head.next = temp
            

    ### Insert at the end
    def add_last(self, data):
        """ Add node at last position"""
        temp = self.head
        temp2 = None
        while temp.next is not None:
            temp2 = temp.next
            temp = temp.next
        temp2.next = Node(data)
        self.head = temp2


    def add_at_index(self, data,newdata):
        """Add node at a specifiec newdata"""
        pass


    def print_linked_list(self):
        """ print the  linked list"""
        temp = self.head
        print(temp.data)
        while temp.next is not None:
            temp = temp.next
            print(temp.data)
            
    def check_head(self):
        return True if self.head is not None else False

    def linked_size(self):
        """ Get the size of linked list"""
        temp = self.head
        count = 1
        while temp.next is not None:
            temp = temp.next
            count += 1
        print(f"The size of the linked list: {count}")

    def delete_node(self,data):
        """ delete the linked linked list node"""
        pass

    def delete_first_node(self):
        """ delete the linked linked list first node"""
        pass
      
    def delete_last_node(self):
        """ delete the linked linked list last node"""
        pass

    def delete_at_index(self,data):
        """ delete the linked linked list node"""
        pass
    
    def reverse(self):
        """ This function reverse the list"""


def linkedList():
    ll=LinkedList()
    ll.add_first(4)
    ll.add_first(5)
    ll.add_first(7)
    ll.add_first(8)
    ll.add_first(9)
    ll.add_last(20)
    ll.add_at_index(4,21)
    ll.add_at_index(11,3)
    print("\nLinked List 1st time")
    ll.print_linked_list()
    print("Linked List 2nd time")
    ll.print_linked_list()
    ll.linked_size()

if __name__ == "__main__":
    linkedList()