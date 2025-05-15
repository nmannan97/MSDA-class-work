# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        if not path.exists("stocks.db"):
            stock_data.create_database()

        self.root = Tk()
        self.root.title("MyName Stock Manager")

        self.menubar = Menu(self.root)

        fileMenu = Menu(self.menubar, tearoff=0)
        fileMenu.add_command(label="Load", command=self.load)
        fileMenu.add_command(label="Save", command=self.save)
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=self.root.destroy)
        self.menubar.add_cascade(label="File", menu=fileMenu)

        webMenu = Menu(self.menubar, tearoff=0)
        webMenu.add_command(label="Import CSV Data", command=self.importCSV_web_data)
        webMenu.add_command(label="Get Web Data", command=self.scrape_web_data)
        self.menubar.add_cascade(label="Web", menu=webMenu)

        chartMenu = Menu(self.menubar, tearoff=0)
        chartMenu.add_command(label="Display Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=chartMenu)

        self.root.config(menu=self.menubar)

        self.headingLabel = Label(self.root, text="Welcome to the Stock Manager", font=("Helvetica", 14))
        self.headingLabel.pack(pady=5)

        self.stockList = Listbox(self.root, width=25)
        self.stockList.pack(side=LEFT, fill=Y, padx=10)
        self.stockList.bind("<<ListboxSelect>>", self.update_data)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill=BOTH, expand=1)

        self.mainTab = Frame(self.tabs)
        self.tabs.add(self.mainTab, text="Main")

        self.historyTab = Frame(self.tabs)
        self.tabs.add(self.historyTab, text="History")

        self.reportTab = Frame(self.tabs)
        self.tabs.add(self.reportTab, text="Report")

        Label(self.mainTab, text="Symbol:").grid(row=0, column=0, sticky=E)
        self.addSymbolEntry = Entry(self.mainTab)
        self.addSymbolEntry.grid(row=0, column=1)

        Label(self.mainTab, text="Name:").grid(row=1, column=0, sticky=E)
        self.addNameEntry = Entry(self.mainTab)
        self.addNameEntry.grid(row=1, column=1)

        Label(self.mainTab, text="Shares:").grid(row=2, column=0, sticky=E)
        self.addSharesEntry = Entry(self.mainTab)
        self.addSharesEntry.grid(row=2, column=1)

        Button(self.mainTab, text="Add Stock", command=self.add_stock).grid(row=3, column=0, columnspan=2, pady=5)

        Label(self.mainTab, text="Buy/Sell Shares:").grid(row=4, column=0, sticky=E)
        self.updateSharesEntry = Entry(self.mainTab)
        self.updateSharesEntry.grid(row=4, column=1)

        Button(self.mainTab, text="Buy", command=self.buy_shares).grid(row=5, column=0, pady=2)
        Button(self.mainTab, text="Sell", command=self.sell_shares).grid(row=5, column=1, pady=2)
        Button(self.mainTab, text="Delete Stock", command=self.delete_stock).grid(row=6, column=0, columnspan=2, pady=5)

        self.dailyDataList = Text(self.historyTab, width=80, height=20)
        self.dailyDataList.pack(padx=10, pady=10)

        self.stockReport = Text(self.reportTab, width=80, height=20)
        self.stockReport.pack(padx=10, pady=10)

        self.root.mainloop()

    def load(self):
        self.stockList.delete(0, END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)
        messagebox.showinfo("Load Data", "Data Loaded")

    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data", "Data Saved")

    def update_data(self, evt):
        self.display_stock_data()

    def display_stock_data(self):
        if not self.stockList.curselection():
            messagebox.showwarning("No Selection", "Please select a stock from the list.")
            return

        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0", END)
                self.stockReport.delete("1.0", END)
                self.dailyDataList.insert(END, "- Date -   - Price -   - Volume -\n")
                self.dailyDataList.insert(END, "=================================\n")
                for daily_data in stock.dataList:
                    row = (
                        daily_data.date.strftime("%m/%d/%y") + "   " +
                        '${:0,.2f}'.format(daily_data.close) + "   " +
                        str(daily_data.volume) + "\n"
                    )
                    self.dailyDataList.insert(END, row)

                if stock.dataList:
                    total_volume = sum(d.volume for d in stock.dataList)
                    average_close = sum(d.close for d in stock.dataList) / len(stock.dataList)
                    max_close = max(d.close for d in stock.dataList)
                    min_close = min(d.close for d in stock.dataList)

                    report_text = (
                        f"📊 Stock Summary Report for {stock.symbol}\n"
                        f"--------------------------------------\n"
                        f"Total Data Points: {len(stock.dataList)}\n"
                        f"Average Close: ${average_close:.2f}\n"
                        f"Max Close: ${max_close:.2f}\n"
                        f"Min Close: ${min_close:.2f}\n"
                        f"Total Volume: {int(total_volume):,}\n"
                    )
                    self.stockReport.insert(END, report_text)

    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get(), self.addNameEntry.get(), float(str(self.addSharesEntry.get())))
        self.stock_list.append(new_stock)
        self.stockList.insert(END, self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0, END)
        self.addNameEntry.delete(0, END)
        self.addSharesEntry.delete(0, END)

    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares", "Shares Purchased")
        self.updateSharesEntry.delete(0, END)

    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Sell Shares", "Shares Sold")
        self.updateSharesEntry.delete(0, END)

    def delete_stock(self):
        if not self.stockList.curselection():
            messagebox.showwarning("No Selection", "Please select a stock to delete.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        self.stockList.delete(ANCHOR)
        self.stock_list = [s for s in self.stock_list if s.symbol != symbol]
        self.headingLabel.config(text="Stock Deleted")
        self.dailyDataList.delete("1.0", END)
        self.stockReport.delete("1.0", END)

    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date", "Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date", "Enter Ending Date (m/d/yy)")

        if not dateFrom or not dateTo:
            messagebox.showwarning("Missing Input", "You must enter both start and end dates.")
            return

        try:
            stock_data.retrieve_stock_web(dateFrom, dateTo, self.stock_list)
        except Exception as e:
            import traceback
            print("DEBUG: Failed to fetch stock data")
            traceback.print_exc()
            messagebox.showerror("Cannot Get Data from Web", f"Error:\n{e}")
            return

        self.display_stock_data()
        messagebox.showinfo("Get Data From Web", "Data Retrieved")

    def importCSV_web_data(self):
        if not self.stockList.curselection():
            messagebox.showwarning("No Selection", "Please select a stock first.")
            return

        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import", filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename:
            stock_data.import_stock_web_csv(self.stock_list, symbol, filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete", symbol + " Import Complete")

    def display_chart(self):
        if not self.stockList.curselection():
            messagebox.showwarning("No Selection", "Please select a stock.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list, symbol)

def main():
    app = StockApp()

if __name__ == "__main__":
    main()
