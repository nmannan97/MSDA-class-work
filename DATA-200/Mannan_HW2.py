import pandas as pd

#Class for assignment 2
class assignment2:

    class file_resvers:
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
    
    class gdp:

        def __init__(self, csv:str):
            self.df = pd.read_csv(csv)
            pd.set_option('display.max_columns', None)

        #print data of the total CSV
        def print_data(self):
            print(self.df)
        
        #Get data of two countries (3)
        def get_data(self, country1: str, country2: str):
            print(self.df[self.df['name'] == country1])
            print(self.df[self.df['name'] == country2])

        def get_combined_purchasing(self, *countries):
            purchasing = 0
            for items in countries:
                temp = self.df[self.df['name'] == items]['value'].iloc[0]
                #print(temp)
                purchasing += int(temp.replace("$", "").replace(',', ""))
            print(purchasing)

        def delete_data(self, *countries):
            pass

#assignment2().file_resvers("C:\\Users\\nmann\\OneDrive\\Desktop\\MSDA material\\MSDA-class-work\\DATA-200\\mary.txt").file_reverse() #input file herer

q4 = assignment2().gdp("E:\\Masters Data Analytics\\MSDA-class-work\\DATA-200\\Real GDP (purchasing power parity).csv")
#q4.get_data("China", "United States")
q4.get_combined_purchasing("China", "United States","India")