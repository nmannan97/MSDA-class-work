import sys
import yfinance as yf
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit
)


class StockFetcherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Yahoo Finance Stock Fetcher")
        self.setGeometry(200, 200, 700, 400)

        self.hist = None  # Store stock data for plotting

        layout = QVBoxLayout()

        self.label = QLabel("Enter Stock Ticker (e.g., AAPL, MSFT):")
        layout.addWidget(self.label)

        self.ticker_input = QLineEdit()
        layout.addWidget(self.ticker_input)

        self.fetch_button = QPushButton("Fetch Stock Data")
        self.fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.fetch_button)

        self.plot_button = QPushButton("Plot Closing Prices")
        self.plot_button.clicked.connect(self.plot_data)
        layout.addWidget(self.plot_button)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def fetch_data(self):
        ticker = self.ticker_input.text().strip().upper()
        if not ticker:
            self.output.setText("Please enter a stock ticker.")
            return

        try:
            self.output.setText(f"Fetching data for {ticker}...")
            stock = yf.Ticker(ticker)
            self.hist = stock.history(period="1mo")  # Save to class attribute

            if self.hist.empty:
                self.output.setText(f"No data found for {ticker}.")
                return

            output_text = f"📊 {ticker} - Last 5 Trading Days:\n\n"
            for index, row in self.hist.tail(5).iterrows():
                output_text += (
                    f"{index.strftime('%Y-%m-%d')}: Open={row['Open']:.2f}, "
                    f"High={row['High']:.2f}, Low={row['Low']:.2f}, "
                    f"Close={row['Close']:.2f}, Volume={int(row['Volume'])}\n"
                )

            self.output.setText(output_text)
        except Exception as e:
            self.output.setText(f"❌ Error: {str(e)}")

    def plot_data(self):
        if self.hist is None or self.hist.empty:
            self.output.setText("No stock data available to plot.")
            return

        try:
            self.hist['Close'].plot(title="Closing Prices", figsize=(10, 5), legend=True)
            plt.xlabel("Date")
            plt.ylabel("Close Price (USD)")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            self.output.setText(f"❌ Plotting error: {str(e)}")


# Run the GUI
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockFetcherApp()
    window.show()
    sys.exit(app.exec_())
