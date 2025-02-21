class MyStack:
    """LIFO Stack implementation using a Python list as underlying storage."""
  
    def __init__(self):
        """Create an empty stack."""
        self.stack = []                           
  
    def __len__(self):
        """Return the number of elements in the stack."""
        return len(self.stack)
  
    def is_empty(self):
        """Return True if the stack is empty."""
        return self.__len__() == 0
  
    def push(self, e):
        """Add element e to the top of the stack."""
        self.stack.append(e)

    def top(self):
        """Return (but do not remove) the element at the top of the stack.
  
        Raise Empty exception if the stack is empty.
        """
        return self.stack[-1]

    def pop(self):
        """Remove and return the element from the top of the stack (i.e., LIFO).
  
        Raise Empty exception if the stack is empty.
        """
        if self.is_empty():  
            raise Exception("Empty stack, error")
        else:
            return self.stack.pop()
            


def reverse_file(filename):
    """Overwrite given file with its contents line-by-line reversed."""
    S = MyStack()
    __output = ""
    with open(filename, 'r') as file:
        for line in file.readlines():
            S.push(line.strip('\n'))
        while not S.is_empty():
            __output += S.pop() + "\n"
        file.close()
    print(__output)


def test_stack():
    """ test the stack"""
    S = MyStack()
    print("Stack length {}".format(S.__len__()))
    print("Is stack empty: {}".format(S.is_empty()))
    S.push("A")  
    S.push("B") 
    S.push("C")
    print("Stack top {}".format(S.top()))
    print("Is stack empty: {}".format(S.is_empty()))
    print("Stack length {}".format(S.__len__()))
    print("Element popped: {}".format(S.pop()))
    print("Element popped: {}".format(S.pop()))
    print("Element popped: {}".format(S.pop()))
    print("Element popped: {}".format(S.pop()))

if __name__ == "__main__":
    filename="E:\Masters Data Analytics\MSDA-class-work\DATA-200\poem.txt"
    reverse_file(filename)
    test_stack()

