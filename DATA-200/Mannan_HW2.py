#Reservse class that will reverse the lines in a file
class reverse:

    def __init__(self, file:str):
        self.file = file
        self.output = []

    #Method that will reverse and sort the file
    def file_reverse(self):
        count = {'word':0, 'chars':0}
        with open(self.file, 'r') as file:
            self.output = file.read()
            #print(self.output)
            count['word'] = len(self.output.split())
            #print(self.output)
            for items in self.output:
                for character in items:
                    count['chars'] += 1
            self.output = self.output.split('\n')
            for index in range(len(self.output)):
                self.output[index] = self.output[index] + '\n'
            file.close()

        with open('result.txt', 'w') as file:
            self.output = self.output[len(self.output)-1:0:-1]
            print("word count %d"%(count['word']))
            print("Character count %d"%(count['chars']))
            file.writelines(self.output)
            file.close()


reverse("C:\\Users\\nmann\\OneDrive\\Desktop\\MSDA material\\MSDA-class-work\\DATA-200\\mary.txt").file_reverse() #input file herer