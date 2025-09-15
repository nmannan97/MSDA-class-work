# Summary: This module contains the functions used by both console and GUI programs to manage stock data.

import sqlite3
import urllib3
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import csv
import time
from datetime import datetime
from utilities import clear_screen
from utilities import sortDailyData
from stock_class import Stock, DailyData
import yfinance as yf

# Create the SQLite database
def create_database():
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    createStockTableCmd = """CREATE TABLE IF NOT EXISTS stocks (
                            symbol TEXT NOT NULL PRIMARY KEY,
                            name TEXT,
                            shares REAL
                        );"""
    createDailyDataTableCmd = """CREATE TABLE IF NOT EXISTS dailyData (
                                symbol TEXT NOT NULL,
                                date TEXT NOT NULL,
                                price REAL NOT NULL,
                                volume REAL NOT NULL,
                                PRIMARY KEY (symbol, date)
                        );"""   
    cur.execute(createStockTableCmd)
    cur.execute(createDailyDataTableCmd)

# Save stocks and daily data into database
def save_stock_data(stock_list):
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    insertStockCmd = """INSERT INTO stocks
                            (symbol, name, shares)
                            VALUES
                            (?, ?, ?); """
    insertDailyDataCmd = """INSERT INTO dailyData
                                    (symbol, date, price, volume)
                                    VALUES
                                    (?, ?, ?, ?);"""
    for stock in stock_list:
        insertValues = (stock.symbol, stock.name, stock.shares)
        try:
            cur.execute(insertStockCmd, insertValues)
            cur.execute("COMMIT;")
        except:
            pass
        for daily_data in stock.dataList: 
            insertValues = (stock.symbol,daily_data.date.strftime("%m/%d/%y"),daily_data.close,daily_data.volume)
            try:
                cur.execute(insertDailyDataCmd, insertValues)
                cur.execute("COMMIT;")
            except:
                pass

# Load stocks and daily data from database
def load_stock_data(stock_list):
    stock_list.clear()
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    stockCur = conn.cursor()
    stockSelectCmd = """SELECT symbol, name, shares
                    FROM stocks; """
    stockCur.execute(stockSelectCmd)
    stockRows = stockCur.fetchall()
    for row in stockRows:
        new_stock = Stock(row[0],row[1],row[2])
        dailyDataCur = conn.cursor()
        dailyDataCmd = """SELECT date, price, volume
                        FROM dailyData
                        WHERE symbol=?; """
        selectValue = (new_stock.symbol,)
        dailyDataCur.execute(dailyDataCmd, selectValue)
        dailyDataRows = dailyDataCur.fetchall()
        for dailyRow in dailyDataRows:
            daily_data = DailyData(datetime.strptime(dailyRow[0],"%m/%d/%y"),float(dailyRow[1]),float(dailyRow[2]))
            new_stock.add_data(daily_data)
        stock_list.append(new_stock)
    sortDailyData(stock_list)

# Get stock price history from web using urllib3 + BeautifulSoup

def retrieve_stock_web(dateStart, dateEnd, stock_list):
    recordCount = 0

    # Parse date strings
    try:
        start_date = datetime.strptime(dateStart, "%m/%d/%Y")
        end_date = datetime.strptime(dateEnd, "%m/%d/%Y")
    except ValueError:
        print("Invalid date format. Please use MM/DD/YYYY.")
        return recordCount

    for stock in stock_list:
        try:
            print(f"📡 Fetching data for {stock.symbol}...")
            df = yf.download(stock.symbol, start=start_date, end=end_date)

            if df.empty:
                print(f"⚠️ No data found for {stock.symbol}")
                continue

            for date, row in df.iterrows():
                try:
                    close = float(row["Close"])
                    volume = float(row["Volume"])
                    stock.add_data(DailyData(date, close, volume))
                    recordCount += 1
                except Exception as row_error:
                    print(f"⚠️ Skipping row error: {row_error}")

            print(f"✅ Loaded {len(df)} records for {stock.symbol}")
        except Exception as e:
            print(f"❌ Failed to fetch {stock.symbol}: {e}")

    return recordCount


# Get price and volume history from Yahoo! Finance using CSV import.
def import_stock_web_csv(stock_list,symbol,filename):
    for stock in stock_list:
            if stock.symbol == symbol:
                with open(filename, newline='') as stockdata:
                    datareader = csv.reader(stockdata,delimiter=',')
                    next(datareader)
                    for row in datareader:
                        daily_data = DailyData(datetime.strptime(row[0],"%Y-%m-%d"),float(row[4]),float(row[6]))
                        stock.add_data(daily_data)

def main():
    clear_screen()
    print("This module will handle data storage and retrieval.")

if __name__ == "__main__":
    main()
