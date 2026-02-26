# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            clear_screen()
            print("Goodbye")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Add Stock ---")
        symbol = input("Enter Ticker Symbol: ").upper()
        name = input("Enter Company Name: ")
        shares = float(input("Enter Number of Shares: "))

        stock_list.append(Stock(symbol, name, shares))

        print("Stock Added – Enter to Add Another or 0 to Stop")
        option = input()

        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")

        option = input("Enter Menu Option: ")

        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)

# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print("Stock List: [", end="")
    print(", ".join([stock.symbol for stock in stock_list]), "]")

    symbol = input("Which stock do you want to buy?: ").upper()
    shares = float(input("How many shares do you want to buy?: "))

    for stock in stock_list:
        if stock.symbol == symbol:
            stock.buy(shares)
            print("Shares purchased.")
            input("Press Enter to Continue")
            return

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    print("Stock List: [", end="")
    print(", ".join([stock.symbol for stock in stock_list]), "]")

    symbol = input("Which stock do you want to sell?: ").upper()
    shares = float(input("How many shares do you want to sell?: "))

    for stock in stock_list:
        if stock.symbol == symbol:
            stock.sell(shares)
            print("Shares sold.")
            input("Press Enter to Continue")
            return

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    print("Stock List: [", ", ".join([s.symbol for s in stock_list]), "]")

    symbol = input("Which stock do you want to delete?: ").upper()

    for stock in stock_list:
        if stock.symbol == symbol:
            stock_list.remove(stock)
            print("Stock deleted.")
            input("Press Enter to Continue")
            return

# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("Stock List ----")
    print("SYMBOL      NAME                SHARES")
    print("======================================")

    for stock in stock_list:
        print(f"{stock.symbol:<10} {stock.name:<20} {stock.shares}")

    input("\nPress Enter to Continue ***")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ----")
    print("Stock List: [", ", ".join([s.symbol for s in stock_list]), "]")
    symbol = input("Which stock do you want to use?: ").upper()

    for stock in stock_list:
        if stock.symbol == symbol:
            print(f"Ready to add data for: {symbol}")
            print("Enter Data Separated by Commas – Do Not Use Spaces")
            print("Enter Blank Line to Quit")
            print("Example: 8/28/20,47.85,10550")

            while True:
                line = input("Enter Date,Price,Volume: ")
                if line.strip() == "":
                    return
                date, price, vol = line.split(",")
                daily = DailyData(datetime.strptime(date, "%m/%d/%y"), float(price), float(vol))
                stock.add_data(daily)

# Display Report for All Stocks
def display_report(stock_list):
    clear_screen()
    print("Stock Report ---")

    for stock in stock_list:
        print(f"\nReport for: {stock.symbol} {stock.name}")
        print(f"Shares:  {stock.shares}")
        if len(stock.DataList) == 0:
            print("*** No daily history.")
        else:
            for d in stock.DataList:
                print(d.date.strftime("%m/%d/%y"), d.close, d.volume)

    print("\n--- Report Complete ---")
    input("Press Enter to Continue")

def display_chart(stock_list):
    clear_screen()
    print("Stock List: [", ", ".join([s.symbol for s in stock_list]), "]")

    symbol = ""
    while symbol == "":
        symbol = input("Which stock do you want to graph?: ").upper().strip()
        if symbol == "":
            print("Please enter a valid symbol.\n")

    display_stock_chart(stock_list, symbol)
    input("Press Enter to Continue")



# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")

        if option == "1":
            stock_data.save_stock_data(stock_list)
            print("Data Saved")
            input("Press Enter to Continue")
        elif option == "2":
            stock_data.load_stock_data(stock_list)
            print("Data Loaded")
            input("Press Enter to Continue")
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)

# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieving Stock Data from Yahoo! Finance ---")
    dateStart = input("Enter starting date (MM/DD/YY): ")
    dateEnd = input("Enter ending date (MM/DD/YY): ")

    count = stock_data.retrieve_stock_web(dateStart, dateEnd, stock_list)
    print(f"Records Retrieved: {count}")
    input("Press Enter to Continue")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import From CSV ---")
    print("Stock List: [", ", ".join([s.symbol for s in stock_list]), "]")

    symbol = input("Enter Symbol: ").upper()
    filename = input("Enter Filename (full path): ")

    stock_data.import_stock_web_csv(stock_list, symbol, filename)

    print("Import complete.")
    input("Press Enter to Continue")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()