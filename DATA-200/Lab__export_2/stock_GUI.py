# Summary: This module contains the user interface and logic for a graphical
# user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData


class StockApp:
    def __init__(self):
        self.stock_list = []
        # check for database, create if not exists
        if path.exists("stocks.db") is False:
            stock_data.create_database()

        # ==============================
        #   CREATE MAIN WINDOW
        # ==============================
        self.root = Tk()
        self.root.title("Stock Manager")

        # ==============================
        #   MENUBAR
        # ==============================
        self.menubar = Menu(self.root)

        # ----- File Menu -----
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Load Data", command=self.load)
        filemenu.add_command(label="Save Data", command=self.save)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        # ----- Web Menu -----
        webmenu = Menu(self.menubar, tearoff=0)
        webmenu.add_command(
            label="Scrape Data from Yahoo! Finance...",
            command=self.scrape_web_data
        )
        webmenu.add_command(
            label="Import CSV From Yahoo! Finance...",
            command=self.importCSV_web_data
        )
        self.menubar.add_cascade(label="Web", menu=webmenu)

        # ----- Chart Menu -----
        chartmenu = Menu(self.menubar, tearoff=0)
        chartmenu.add_command(label="Show Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=chartmenu)

        # Attach the menubar to the window
        self.root.config(menu=self.menubar)

        # ==============================
        #   LAYOUT FRAMES
        # ==============================

        # Left frame: stock list & controls
        leftFrame = Frame(self.root)
        leftFrame.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        # Right frame: tabs (main/history/report)
        rightFrame = Frame(self.root)
        rightFrame.grid(row=0, column=1, padx=10, pady=10)

        # ==============================
        #   LEFT SIDE - STOCK LIST
        # ==============================
        Label(leftFrame, text="Tracked Stocks").pack()

        self.stockList = Listbox(leftFrame, width=20, height=20)
        self.stockList.pack()
        self.stockList.bind("<<ListboxSelect>>", self.update_data)

        # ----- Add Stock Section -----
        Label(leftFrame, text="Add Stock").pack(pady=(10, 0))
        Label(leftFrame, text="Symbol:").pack()
        self.addSymbolEntry = Entry(leftFrame)
        self.addSymbolEntry.pack()
        Label(leftFrame, text="Name:").pack()
        self.addNameEntry = Entry(leftFrame)
        self.addNameEntry.pack()
        Label(leftFrame, text="Shares:").pack()
        self.addSharesEntry = Entry(leftFrame)
        self.addSharesEntry.pack()
        Button(leftFrame, text="Add Stock", command=self.add_stock).pack(pady=5)

        # ----- Buy/Sell Section -----
        Label(leftFrame, text="Buy / Sell Shares").pack(pady=(10, 0))
        Label(leftFrame, text="Shares:").pack()
        self.updateSharesEntry = Entry(leftFrame)
        self.updateSharesEntry.pack()
        Button(leftFrame, text="Buy", command=self.buy_shares).pack(pady=2)
        Button(leftFrame, text="Sell", command=self.sell_shares).pack(pady=2)

        # ----- Delete Stock -----
        Button(leftFrame, text="Delete Stock", command=self.delete_stock).pack(pady=10)

        # ==============================
        #   RIGHT SIDE - TABS
        # ==============================

        self.tabs = ttk.Notebook(rightFrame)
        self.tabMain = Frame(self.tabs)
        self.tabHistory = Frame(self.tabs)
        self.tabReport = Frame(self.tabs)

        self.tabs.add(self.tabMain, text="Main")
        self.tabs.add(self.tabHistory, text="History")
        self.tabs.add(self.tabReport, text="Report")

        self.tabs.pack(expand=1, fill="both")

        # ----- Main Tab -----
        self.headingLabel = Label(self.tabMain, text="Select a Stock", font=("Arial", 16))
        self.headingLabel.pack(pady=20)

        Label(
            self.tabMain,
            text="Use the Web menu to retrieve data, or import CSV from Yahoo! Finance."
        ).pack()

        # ----- History Tab -----
        self.dailyDataList = Text(self.tabHistory, width=60, height=20)
        self.dailyDataList.pack()

        # ----- Report Tab -----
        self.stockReport = Text(self.tabReport, width=60, height=20)
        self.stockReport.pack()

        # Start the Tkinter event loop
        self.root.mainloop()

    # ============================
    #   FUNCTIONALITY
    # ============================

    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0, END)
        self.stock_list.clear()
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)
        messagebox.showinfo("Load Data", "Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data", "Data Saved")

    # Refresh history and report tabs when a stock is selected.
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history & report.
    def display_stock_data(self):
        if not self.stockList.curselection():
            return  # nothing selected yet
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                # Heading
                self.headingLabel["text"] = (
                    stock.name + " - " + str(stock.shares) + " Shares"
                )

                # Clear text fields
                self.dailyDataList.delete("1.0", END)
                self.stockReport.delete("1.0", END)

                # History tab header
                self.dailyDataList.insert(
                    END, "- Date -   - Price -   - Volume -\n"
                )
                self.dailyDataList.insert(
                    END, "=================================\n"
                )

                # Fill history
                for daily_data in stock.DataList:
                    row = (
                        daily_data.date.strftime("%m/%d/%y")
                        + "   "
                        + "${:0,.2f}".format(daily_data.close)
                        + "   "
                        + str(daily_data.volume)
                        + "\n"
                    )
                    self.dailyDataList.insert(END, row)

                # ----- Report Tab -----
                self.stockReport.insert(
                    END, f"Report for {stock.symbol} - {stock.name}\n"
                )
                self.stockReport.insert(END, f"Shares: {stock.shares}\n\n")

                if len(stock.DataList) == 0:
                    self.stockReport.insert(END, "*** No daily history.\n")
                else:
                    for daily in stock.DataList:
                        row = (
                            daily.date.strftime("%m/%d/%y")
                            + "    "
                            + "${:0,.2f}".format(daily.close)
                            + "    "
                            + str(daily.volume)
                            + "\n"
                        )
                        self.stockReport.insert(END, row)
                break

    # Add new stock to track.
    def add_stock(self):
        try:
            symbol = self.addSymbolEntry.get().upper()
            name = self.addNameEntry.get()
            shares = float(str(self.addSharesEntry.get()))
            if symbol == "" or name == "":
                raise ValueError
        except:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid symbol, name, and numeric share value.",
            )
            return

        new_stock = Stock(symbol, name, shares)
        self.stock_list.append(new_stock)
        sortStocks(self.stock_list)

        # refresh listbox sorted
        self.stockList.delete(0, END)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)

        self.addSymbolEntry.delete(0, END)
        self.addNameEntry.delete(0, END)
        self.addSharesEntry.delete(0, END)

    # Buy shares of stock.
    def buy_shares(self):
        if not self.stockList.curselection():
            messagebox.showerror("No Stock Selected", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        try:
            shares = float(self.updateSharesEntry.get())
        except:
            messagebox.showerror("Invalid Input", "Enter a numeric share amount.")
            return

        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(shares)
                self.headingLabel["text"] = (
                    stock.name + " - " + str(stock.shares) + " Shares"
                )
                break
        messagebox.showinfo("Buy Shares", "Shares Purchased")
        self.updateSharesEntry.delete(0, END)

    # Sell shares of stock.
    def sell_shares(self):
        if not self.stockList.curselection():
            messagebox.showerror("No Stock Selected", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        try:
            shares = float(self.updateSharesEntry.get())
        except:
            messagebox.showerror("Invalid Input", "Enter a numeric share amount.")
            return

        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(shares)
                self.headingLabel["text"] = (
                    stock.name + " - " + str(stock.shares) + " Shares"
                )
                break
        messagebox.showinfo("Sell Shares", "Shares Sold")
        self.updateSharesEntry.delete(0, END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
        if not self.stockList.curselection():
            messagebox.showerror("No Stock Selected", "Please select a stock to delete.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stock_list.remove(stock)
                break

        # Refresh listbox
        self.stockList.delete(0, END)
        for stock in self.stock_list:
            self.stockList.insert(END, stock.symbol)

        # Clear display
        self.headingLabel["text"] = "Select a Stock"
        self.dailyDataList.delete("1.0", END)
        self.stockReport.delete("1.0", END)

        messagebox.showinfo("Delete Stock", f"{symbol} removed.")

    # Get data from web scraping (Yahoo! Finance).
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring(
            "Starting Date", "Enter Starting Date (m/d/yy)"
        )
        dateTo = simpledialog.askstring(
            "Ending Date", "Enter Ending Date (m/d/yy)"
        )
        if not dateFrom or not dateTo:
            return
        try:
            records = stock_data.retrieve_stock_web(
                dateFrom, dateTo, self.stock_list
            )
            sortDailyData(self.stock_list)
        except:
            messagebox.showerror(
                "Cannot Get Data from Web",
                "Check PATH for Chrome Driver and your dates.",
            )
            return

        # Refresh display if a stock is selected
        if self.stockList.curselection():
            self.display_stock_data()
        messagebox.showinfo(
            "Get Data From Web", f"Data Retrieved. Records: {records}"
        )

    # Import CSV stock history file downloaded from Yahoo! Finance.
    def importCSV_web_data(self):
        if not self.stockList.curselection():
            messagebox.showerror("No Stock Selected", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(
            title="Select " + symbol + " File to Import",
            filetypes=[("Yahoo Finance! CSV", "*.csv")],
        )
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list, symbol, filename)
            sortDailyData(self.stock_list)
            self.display_stock_data()
            messagebox.showinfo("Import Complete", symbol + " Import Complete")

    # Display stock price chart.
    def display_chart(self):
        if not self.stockList.curselection():
            messagebox.showerror("No Stock Selected", "Please select a stock first.")
            return
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list, symbol)

def main():
    app = StockApp()

if __name__ == "__main__":
    # execute only if run as a script
    main()