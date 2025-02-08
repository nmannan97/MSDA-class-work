#Reservse class that will reverse the lines in a file
class reverse:

    def __init__(self, file:str):
        self.file = file
        self.output = []

    #Method that will reverse and sort the file
    def file_reverse(self):

        with open(self.file, 'r') as file:
            for line in file:
                self.output.append(line.strip('\n') + "\n")        
            file.close()

        with open('result.txt', 'w') as file:
            self.output = self.output[len(self.output)-1:0:-1]
            file.writelines(self.output)
            print(self.output)
            file.close()

    
reverse("C:\\Users\\nmann\\OneDrive\\Desktop\\MSDA material\\MSDA-class-work\\DATA-200\\mary.txt").file_reverse() #input file herer