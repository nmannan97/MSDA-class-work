import math

class hw_01():

    def __init__(self):
        self.output = None

    def q2(self):
        count = 0
        self.output = []
        while count<4:
            try:
                temp2 = input("enter a number: ")
                self.output.append(int(temp2))
                count += 1
            except ValueError:
                print("number not detected")
        return max(self.output)

    def q3(self):
        str1 = """ The team leader repeatedly repeated the same instructions over and over again to the team, but the team still made the same mistake again. Despite the team leader's repeated instructions, the team still made the same mistake."""
        str1 = str1.lower()
        self.output = {value: str1.count(value) for value in str1.split()}
        #print(self.output)
        print("Word | Count")
        for item in self.output:
            print("{} {}".format(self.output[item], item))

    def q4(self):
        barList = [5,3,2,7,4]
        print("Index | Value | Bar")
        count = 0
        while len(barList) != 0:
            temp = barList.pop(0)
            temp2 = ""
            for _ in range(temp):
                temp2 += "*"
            print("{} | {} | {}".format(count, temp, temp2))
            count += 1

thing = hw_01()
print(thing.q2())
thing.q3()
thing.q4()

"""
Solve Q2: Write a program to accept 4 numbers and you need to print the minimum out of 4 numbers. Please make sure you use comments and Docstring. (5 Marks)

Solve Q3:  Write a program in python to print the count of ocurrenrces of each unique word. (in str1 above) (5 Marks)


OUTPUT (Sample)

WORD  COUNT

Over        2

team      4 

 

You need to completed the above output. Try to use list and dictionary to implement this program.

 

Q4: Write the following program : Marks (5)

Print the bar chart based on barList = [5,3,2,7,4]

 

Sample Output

Index     Value      Bar

 0.            5            *****

 1.            3            ***

  2            2           **

  3           7            ******

  4           4          ****
"""