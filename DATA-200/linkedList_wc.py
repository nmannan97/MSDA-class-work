# Node class to be a part of Linked List
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_first(self, data):
        """Add node at the beginning"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def add_last(self, data):
        """Add node at the end"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def add_at_index(self, target_data, new_data):
        """Replace a node's data if it matches target_data"""
        current = self.head
        while current:
            if current.data == target_data:
                current.data = new_data
                return
            current = current.next

    def print_linked_list(self):
        """Print the linked list"""
        temp = self.head
        while temp:
            print(temp.data, end=" -> " if temp.next else "")
            temp = temp.next
        print()

    def check_head(self):
        return self.head is not None

    def linked_size(self):
        """Return the size of the linked list"""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        print(f"Size of linked list: {count}")

    def delete_node(self, data):
        """Delete a node with a specific value"""
        current = self.head
        prev = None
        while current:
            if current.data == data:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return
            prev = current
            current = current.next

    def delete_first_node(self):
        """Delete the first node"""
        if self.head:
            self.head = self.head.next

    def delete_last_node(self):
        """Delete the last node"""
        if self.head is None:
            return
        if self.head.next is None:
            self.head = None
            return
        current = self.head
        while current.next and current.next.next:
            current = current.next
        current.next = None

    def delete_at_index(self, index):
        """Delete a node at a specific index (0-based)"""
        if index < 0 or self.head is None:
            return
        if index == 0:
            self.head = self.head.next
            return
        current = self.head
        for _ in range(index - 1):
            if current.next is None:
                return
            current = current.next
        if current.next:
            current.next = current.next.next

    def reverse(self):
        """Reverse the linked list"""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev


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
    ll.delete_first_node()
    print("Linked List 3rd time")
    ll.print_linked_list()
    ll.delete_at_index(1)
    ll.print_linked_list()
    ll.linked_size()   
    
    ll=LinkedList()
    ll.add_first(10)
    ll.add_first(7)
    ll.add_first(8)
    ll.add_first(5)
    ll.add_first(9)
    ll.print_linked_list()  
    ll.reverse()
    ll.print_linked_list()  

if __name__ == "__main__":
    linkedList()