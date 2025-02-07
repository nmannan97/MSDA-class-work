
class reverse:

    def __init__(self, file:str):
        self.file = file
        self.output = []

    def file_reverse(self):

        with open(self.file, 'r') as file:
            for line in file:
                self.output.append(line.strip('\n') + "\n")        
            file.close()
        with open('result.txt', 'w') as file:
            self.output.sort(reverse=True)
            file.writelines(self.output)
            print(self.output)
            file.close()

    
reverse("C:\\Users\\nmann\\OneDrive\\Desktop\\MSDA material\\MSDA-class-work\\DATA-200\\mary.txt").file_reverse() #input file herer