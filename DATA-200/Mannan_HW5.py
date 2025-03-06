# Node class to be a part of Linked List
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Create a class called LinkedList
class LinkedList:
    def __init__(self):
        self.head = None

    def add_first(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def add_last(self, data):
        if self.head is None:
            self.head = Node(data)
        else:
            c1 = self.head
            while c1.next is not None:
                c1 = c1.next
            c1.next = Node(data)

    def add_at_index(self, data, newdata):
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
        if self.check_head():
            c1 = self.head
            while c1 is not None:
                print(c1.data, end=" -> ")
                c1 = c1.next
            print("None")

    def check_head(self):
        return self.head is not None

    def linked_size(self):
        count = 0
        c1 = self.head
        while c1:
            count += 1
            c1 = c1.next
        print("The linked list size is", count)

    def delete_node(self, data):
        if not self.check_head():
            print("List is empty")
            return
        if self.head.data == data:
            self.head = self.head.next
            return
        c1 = self.head
        while c1.next is not None:
            if c1.next.data == data:
                c1.next = c1.next.next
                return
            c1 = c1.next
        print("Node with value", data, "not found.")

    def delete_first_node(self):
        if not self.check_head():
            print("List is empty")
            return
        self.head = self.head.next

    def delete_last_node(self):
        if not self.check_head():
            print("List is empty")
            return
        if self.head.next is None:
            self.head = None
            return
        c1 = self.head
        while c1.next.next is not None:
            c1 = c1.next
        c1.next = None

    def delete_at_index(self, data):
        if not self.check_head():
            print("List is empty")
            return
        c1 = self.head
        prev_head = None
        while c1 is not None:
            if c1.data == data:
                if prev_head is None:
                    self.head = c1.next
                else:
                    prev_head.next = c1.next
                return
            prev_head = c1
            c1 = c1.next
        print("Node with value", data, "not found.")

    def reverse(self):
        prev = None
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev


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

    ll.reverse()
    print("\nLinked List 2")
    ll.print_linked_list()

if __name__ == "__main__":
    linkedList()
    linkedList2()
