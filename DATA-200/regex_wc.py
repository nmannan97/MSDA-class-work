import re

f = open(r"./DATA-200/bookshelf.txt")

string = f.read()

t=r""
result = re.findall(r"", string)

print(result)


## Write a pattern on line 7, in between the double quotes, that will match all the book titles in the file that end with the letter p.
## Write a pattern on line 7, in between the double quotes, that will match all the authors in the file whose last name starts with the letter B.
## Write a pattern on line 7, in between the double quotes, that will match all the books in the file that have been published between 1980 and 1999.
