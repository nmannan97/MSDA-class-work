
class quickSort:

    def __init__(self):
        self.array = [23, 6, 4, -1, 0, 12, 8, 3, 1]

    def sort(self, List=[], i=-1, j=0, pivot=0, count=0):
        pivot = len(List) - 1
        if (len(List) - 1 == j):
            print("Piviting at Len")
            List[i + 1], List[j] = List[j], List[i + 1]
            print(List)       
            return self.sort(List, pivot=pivot)

        elif (List[j] <= List[pivot]):
            print("Entering pivot")
            i += 1 
            List[i], List[j] = List[j], List[i]
            print(List)
            print("i & j", i, j)
            count += 1
            if (count == len(List) - 1):
                returnList = List
                return returnList
            return self.sort(List, i, j=j+1, pivot=pivot, count=count)

        elif (List[j] > List[pivot]):
            print("Entering pivot part B")
            print(List)
            return self.sort(List, i, j=j+1, pivot=pivot)

if __name__ == "__main__":
    Sort = quickSort()
    print("output: ", Sort.sort(Sort.array))