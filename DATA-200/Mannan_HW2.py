import pandas as pd
import csv

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

        def get_combined_purchasing(self, countries:list):
            purchasing = 0
            for items in countries:
                temp = self.df[self.df['name'] == items]['value'].to_string()
                purchasing += int(temp.replace("$", "").replace(",", "").replace(" ",""))
            print("Combined output: " + purchasing)

        def delete_data(self, *countries):
            output_df = pd.DataFrame()
            for country in countries:
                output_df = pd.concat([output_df, self.df[self.df['name'] == country]])
                self.df = self.df[self.df['name'] != country]
            output_df.head
            self.df.to_csv("DATA-200\\Real GDP (purchasing power parity).csv", index=False)
            output_df.to_csv("DATA-200\\deleted_info.csv", index=False)

        def merge_files(self):
            csv_data_output = []
            csv_data_input = []
            with open("DATA-200\\Real GDP (purchasing power parity).csv", 'r') as file:
                temp = csv.reader(file)
                for row in temp:
                    csv_data_output.append(row)    
                file.close()

            with open("DATA-200\\deleted_info.csv", 'r') as file:
                temp = csv.reader(file)
                for row in temp:
                    csv_data_input.append(row)  
                csv_data_input = csv_data_input[1:]  
                file.close()
            print(csv_data_input)

            while len(csv_data_input) != 0:
                temp = csv_data_input.pop()
                for index in range(1, len(csv_data_output)):
                    if int(temp[4]) < int(csv_data_output[index][4]):
                        csv_data_output.insert(index, temp)
                        break
                if int(temp[4]) > int(csv_data_output[len(csv_data_output)-1][4]):
                    csv_data_output.append(temp)
            #print(csv_data_output)

            with open("DATA-200\\Real GDP (purchasing power parity).csv", 'w',  newline='') as file:   
                writer = csv.writer(file)
                writer.writerows(csv_data_output)
                file.close()
        
        def run(self):
            run = True
            while run:
                command = input("type your next command\n-print data\n-combined purchasing power\n-delete countries\n-merge data\n-Exit\n")
                if command.lower() == "print data":
                    self.print_data()
                elif command.lower() == "combined purchasing power":
                    Input = []
                    while True:
                        country = input("Enter a country (press just enter to end): ")
                        if country == "":
                            break
                        else:
                            Input.append(country)
                    self.get_combined_purchasing(Input)
                elif command.lower() == "delete countries":
                    pass
                elif command.lower() == "merge data":
                    pass
                elif command.lower() == 'exit':
                    run = False
                else:
                    input("No command detected, try typing it again. Press enter to continue")

            print("Thank you for running the program")

if __name__ == "__main__":
    assignment2().gdp("E:\\Masters Data Analytics\\MSDA-class-work\\DATA-200\\Real GDP (purchasing power parity).csv").run()
    assignment2().file_resvers("C:\\Users\\nmann\\OneDrive\\Desktop\\MSDA material\\MSDA-class-work\\DATA-200\\mary.txt").file_reverse() #input file herer