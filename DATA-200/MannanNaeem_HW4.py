class MyStack:

    def __init__(self):
        self.stack = []

    def pop(self):
        if self.is_empty():
            return "no elements in stack"
        else:
            return self.stack.pop()

    def push(self, item):
        self.stack.append(item)

    def is_empty(self):
        return True if len(self.stack) == 0 else False

    def last_element(self):
        if self.is_empty():
            return "no elements in stack"
        else:
            return self.stack[-1]

List = [0, 1, 2, 4]
stack = MyStack()
for items in List:
    print("Stack is empty: {}".format(stack.is_empty()))
    stack.push(items)
    print(stack.stack)
    print("Last element in stack: {}".format(stack.last_element()))

for items in List:
    print("Stack is empty: {}".format(stack.is_empty()))
    stack.pop()
    print(stack.stack)
    print("Last element in stack: {}".format(stack.last_element()))