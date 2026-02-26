#Helper Functions

import matplotlib.pyplot as plt

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    stock_list.sort(key=lambda stock: stock.symbol.upper())


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda d: d.date)


def display_stock_chart(stock_list, symbol):
    # Find the selected stock
    for stock in stock_list:
        if stock.symbol == symbol:
            dates = [data.date for data in stock.DataList]
            prices = [data.close for data in stock.DataList]

            if len(dates) == 0:
                print("No daily data available for chart.")
                return

            # Sort by date (optional but recommended)
            dates, prices = zip(*sorted(zip(dates, prices)))

            plt.figure(figsize=(10,5))
            plt.plot(dates, prices, marker='o')
            plt.title(stock.name.upper())
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
            return

    print("Stock symbol not found.")
