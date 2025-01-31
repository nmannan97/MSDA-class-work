import sys
import os
from PyQt5.QtWidgets import *

# Define error window
class errorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Error")
        self.resize(300, 200)

        layout = QVBoxLayout()
        label = QLabel("ERROR! Try again.")
        layout.addWidget(label)
        self.setLayout(layout)

# Define the second window
class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin ID window")
        self.resize(300, 200)
        self.items = ["TV", "Radio", "mbile phone", "laptop"]

        self.dropdown = QComboBox()
        self.dropdown.addItems(self.items)  # Add options

        layout = QVBoxLayout()
        layout.addWidget(self.dropdown)
        self.setLayout(layout)

# Define the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login customer/admin")
        self.resize(400, 300)

        # Create a text input field
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.password_input.setPlaceholderText("Enter password")

        # Create a button to open the second window
        self.button = QPushButton("submit")
        self.button.clicked.connect(self.open_second_window)

        # Set layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        self.second_window = None  # Initialize second window as None

    def open_second_window(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if "customer" in username and password=="12345":
            self.second_window = SecondWindow()
            self.second_window.show()
        else:
            self.second_window = errorWindow()
            self.second_window.show()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = SecondWindow() #Change to login once done
    main_win.show()
    sys.exit(app.exec_())
