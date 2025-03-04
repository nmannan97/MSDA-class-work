# Node class to be a part of Linked List
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Create a class called LinkedList
class LinkedList:

    def __init__(self):
        self.head = None

    # Add a node at the beginning
    def add_first(self, data):
        """ Add First Node """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    # Insert at the end
    def add_last(self, data):
        """ Add node at last position """
        if self.head is None:
            self.head = Node(data)
        else:
            c1 = self.head
            while c1.next is not None:
                c1 = c1.next
            c1.next = Node(data)

    def add_at_index(self, data, newdata):
        """ Add node at a specific position after 'data' """
        if not self.check_head():
            print("List is empty")
            return

        c1 = self.head
        while c1 is not None:
            if c1.data == data:
                nn = Node(newdata)
                nn.next = c1.next
                c1.next = nn
                return
            c1 = c1.next

        print("No data element found in linked list")

    def print_linked_list(self):
        """ Print the linked list (Fixed infinite loop issue) """
        if self.check_head():
            c1 = self.head
            while c1 is not None:
                print(c1.data, end=" -> ")
                c1 = c1.next  # Move pointer forward
            print("None")  # End of the list

    def check_head(self):
        return self.head is not None
    
    def linked_size(self):
        """ Get the size of linked list """
        count = 0
        c1 = self.head
        while c1:
            count += 1
            c1 = c1.next
        print("The linked list size is", count)

    def delete_node(self, data):
        """ delete the linked linked list node """
        pass

    def delete_first_node(self):
        """ delete the linked linked list first node """
        if not self.check_head():
            print("List is empty")
            return
        self.head = self.head.next  # Move head to the next node


    def delete_last_node(self):
        """ delete the linked linked list last node """
        pass

    def delete_at_index(self,data):
        """ delete the linked linked list node """
        if not self.check_head():
            print("List is empty")
            return

        c1 = self.head
        prev_head = None
        while c1 is not None:
            if c1.data == data:
                print(prev_head)
                return
            prev_head = c1
            c1 = c1.next

    def reverse(self):
        """ This function reverse the list """
        c1 = self.head  
        while c1:
            
            c1 = c1.next

def linkedList() -> None:
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

def linkedList2() -> None:
    ll=LinkedList()
    ll.add_first(10)
    ll.add_first(7)
    ll.add_first(8)
    ll.add_first(5)
    ll.add_first(9)
    print("\nLinked List")
    ll.print_linked_list()

    ll.delete_at_index(8)
    print("\nLinked List 2")
    ll.print_linked_list()

if __name__ == "__main__":
    #linkedList()
    linkedList2()