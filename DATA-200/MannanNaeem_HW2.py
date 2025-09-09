import csv
import json
import os

class hw_2():
    
    def Q3(self):
        output = ""
        temp = None
        with open("DATA-200\Files\MaryLamb.txt", 'r') as f:
            temp = f.readlines()
            for i in range(len(temp) - 1, 0, -1):
                output += temp[i]
            f.close()      

        with open("output.txt", 'w') as f:
            f.write(output)
            f.close()   

class Q4:

    def __init__(self, filename):
        self.filename = filename
        self.deleted_file = "deleted_info.csv"
        self.cache = self.load_data()

        if not os.path.exists(self.deleted_file):
            with open(self.deleted_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["name", "slug", "value", "date_of_information", "ranking", "region"])

    def load_data(self):
        data = {}
        with open(self.filename, "r", encoding="utf-8-sig") as f:  # BOM safe
            reader = csv.DictReader(f)
            for row in reader:
                country = row["name"].strip()

                # clean value field
                clean_value = row["value"].replace("$", "").replace(",", "").strip()
                try:
                    value = float(clean_value)
                except ValueError:
                    value = 0.0

                data[country] = {
                    "slug": row["slug"],
                    "Value": value,
                    "Date": row["date_of_information"],
                    "Rank": int(row["ranking"]),
                    "Region": row["region"]
                }
        return data

    def save_data(self):
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            fieldnames = ["name", "slug", "value", "date_of_information", "ranking", "region"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for country, info in self.cache.items():
                writer.writerow({
                    "name": country,
                    "slug": info["slug"],
                    "value": info["Value"],
                    "date_of_information": info["Date"],
                    "ranking": info["Rank"],
                    "region": info["Region"]
                })

    def get_country(self, country):
        return self.cache.get(country, "Not found")

    def modify_country(self, country, value, rank):
        if country in self.cache:
            self.cache[country]["Value"] = value
            self.cache[country]["Rank"] = rank
            self.save_data()

    def compare_countries(self, c1, c2):
        d1, d2 = self.cache.get(c1), self.cache.get(c2)
        if d1 and d2:
            print(f"{c1}: Value={d1['Value']}, Rank={d1['Rank']}")
            print(f"{c2}: Value={d2['Value']}, Rank={d2['Rank']}")
        else:
            print("One or both countries not found.")

    def combine_countries(self, countries):
        total_value = sum(self.cache[c]["Value"] for c in countries if c in self.cache)
        print("Combined PPP value:", total_value)

    def delete_country(self, country):
        if country in self.cache:
            deleted_data = self.cache.pop(country)
            file_exists = os.path.exists(self.deleted_file)

            with open(self.deleted_file, "a", newline="", encoding="utf-8") as f:
                fieldnames = ["name", "slug", "value", "date_of_information", "ranking", "region"]
                writer = csv.DictWriter(f, fieldnames=fieldnames)

                # Write header if file is new or empty
                if not file_exists or os.path.getsize(self.deleted_file) == 0:
                    writer.writeheader()

                writer.writerow({
                    "name": country,
                    "slug": deleted_data["slug"],
                    "value": deleted_data["Value"],
                    "date_of_information": deleted_data["Date"],
                    "ranking": deleted_data["Rank"],
                    "region": deleted_data["Region"]
                })

            self.save_data()
            print(f"{country} deleted and stored in {self.deleted_file}")



    def restore_deleted(self):
        with open(self.deleted_file, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            # Debug: print headers to confirm
            print("Restore headers:", reader.fieldnames)

            if "name" not in reader.fieldnames:
                print("Error: deleted_info.csv missing headers. Please delete the file and try again.")
                return

            for row in reader:
                country = row["name"]
                if country not in self.cache:
                    try:
                        value = float(str(row["value"]).replace("$", "").replace(",", ""))
                    except ValueError:
                        value = 0.0
                    self.cache[country] = {
                        "slug": row["slug"],
                        "Value": value,
                        "Date": row["date_of_information"],
                        "Rank": int(row["ranking"]),
                        "Region": row["region"]
                    }
        self.save_data()
        print("Deleted data restored successfully!")

if __name__ == "__main__":
    print(hw_2().Q3())
    # Example usage
    system = Q4("DATA-200\Files\Real GDP (purchasing power parity).csv")
    system.compare_countries("United States", "China")
    system.combine_countries(["India", "Pakistan"])
    system.delete_country("France")
    system.restore_deleted()

"""
Q1 What is the difference between raising an exception and handling an exception ( Explain with example)? 5 (Marks)

Q2 What happens when an exception is raised, the code of a finally clause executes, and that code raises an exception of a different kind than the original one? Which one is caught by a surrounding clause? ( Explain with example) (5 Marks)

Q3 Write a program that reads each line in a file, reverses its lines, and writes them to another file. Also, print the total character count and word count on the screen.  For example, if the file file.txt contains the lines (Marks 5)

Mary had a little lamb
Its fleece was white as snow
And everywhere that Mary went
The lamb was sure to go.
and you run

reverse file.txt result.txt
then result.txt contains

run you and

The lamb was sure to go.
And everywhere that Mary went
Its fleece was white as snow
Mary had a little lamb

Q4: You work for XYZ company and you need to design a purchasing power parity system based system based on countries. You can get the data from https://www.cia.gov/the-world-factbook/field/real-gdp-purchasing-power-parity/country-comparison/Links to an external site. download the file from this location. Your program must have following capabilities (5 Mark):

    1) You must have caching system i.e. store the file data in memory and if someone request data for a country, you can quickly print it.

    2) You must have a way to modify the data in memory and as well in file so that ranking and value can be modified. 

    3) You must have function to accept the input from user to show the comparison between 2 countries which must show values and ranking
      
    4) You must have a function to accept the input of countries and show their combined purchasing power parity

    5) You must have function to delete the enteries from the file and memory and you should store the deleted data in a file called deleted_info.csv Download deleted_info.csvand if someone want to merge the data they should be able to update the memory and original file without duplicate enteries.
"""