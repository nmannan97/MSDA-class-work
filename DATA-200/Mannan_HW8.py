
class quickSort:

    def __init__(self):
        self.array = [23, 6, 4, -1, 0, 12, 8, 3, 1]

    def sort(self, List=[], i=0, j=0, pivot=0):
        pivot = len(List) - 1
        if (List[j] <= List[pivot]):
            print("Entering pivot")
            temp = List[i]
            List[i] = List[j]
            List[j] = temp
            if j == i:
                j += 1
            else:
                j += 1
                i += 1 
            self.sort(List, i, j, pivot)
        else:
            print("RETURNING pivot")
            return List

if __name__ == "__main__":
    Sort = quickSort()
    print("output: ", Sort.sort(Sort.array))