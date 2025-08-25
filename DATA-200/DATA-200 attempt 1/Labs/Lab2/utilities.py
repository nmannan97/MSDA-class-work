#Helper Functions

import matplotlib.pyplot as plt
from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt":  # User is running Windows
        _ = system('cls')
    else:  # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    stock_list.sort(key=lambda x: x.symbol)

# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.dataList.sort(key=lambda x: x.date)

# Function to create stock chart
def display_stock_chart(stock_list, symbol):
    for stock in stock_list:
        if stock.symbol == symbol:
            if not stock.dataList:
                print("WARNING: No data available to plot.")
                return

            dates = [data.date for data in stock.dataList]
            closes = [data.close for data in stock.dataList]

            plt.figure(figsize=(10, 5))
            plt.plot(dates, closes, marker='o', linestyle='-', color='blue')
            plt.title(f"{symbol} - Closing Prices")
            plt.xlabel("Date")
            plt.ylabel("Closing Price (USD)")
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
            return

    print(f"Symbol '{symbol}' not found in stock list.")
