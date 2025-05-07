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
    ## Sort the stock list
    pass


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    pass

# Function to create stock chart
def display_stock_chart(stock_list,symbol):
    pass