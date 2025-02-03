import sys
from PyQt5.QtWidgets import *

# Define error window
class assignment1():

    def __init__(self):
        self.customers = {
                            "customer 1":{
                                "password":"12345", 
                                "ratings":{
                                    "TV": 0,
                                    "Radio" : 0, 
                                    "mobile phone": 0, 
                                    "laptop": 0
                                }
                            }
                        }
        self.admins ={
                        "admin1": 
                        {
                            "password": "12345", 
                            "ID": "001",
                            "failedLogins": 0,
                            'successfulLogins': 0
                        }, 
                        "admin2": 
                        {
                            "password": "12345", 
                            "ID": "002",
                            "failedLogins": 0,
                            'successfulLogins': 0
                        }
                    }

    class errorWindow(QWidget):
        def __init__(self, text=""):
            super().__init__()
            self.setWindowTitle("Error")
            self.resize(300, 200)

            layout = QVBoxLayout()
            if text == "":
                label = QLabel("ERROR! Try again.")
            else:
                label = QLabel("{}".format(text))
            layout.addWidget(label)
            self.setLayout(layout)

    # Define the customer window
    class customerWindow(QWidget):
        def __init__(self, parents_instance):
            super().__init__()
            self.setWindowTitle("Admin ID window")
            self.resize(450, 350)
            self.items = {"TV":0, "Radio":0, "mbile phone":0, "laptop":0}
            self.data = parents_instance.customers

            # Set dropdown menu
            self.dropdown = QComboBox()
            self.dropdown.addItems(self.items)  # Add options

            # Define radio buttons
            self.radio1 = QRadioButton("1 rating")
            self.radio2 = QRadioButton("2 rating")
            self.radio3 = QRadioButton("3 rating")
            self.radio4 = QRadioButton("4 rating")
            self.radio5 = QRadioButton("5 rating")

            # Create a button to display the selected option
            self.button = QPushButton("Show Selected Option")
            self.button.clicked.connect(self.show_selected)

            layout = QVBoxLayout()
            layout.addWidget(self.dropdown)
            layout.addWidget(self.radio1)
            layout.addWidget(self.radio2)
            layout.addWidget(self.radio3)
            layout.addWidget(self.radio4)
            layout.addWidget(self.radio5)
            layout.addWidget(self.button)
            self.setLayout(layout)

        def show_selected(self):
            # Check which radio button is selected
            for key in self.data:
                print(self.data[key])
            if self.radio1.isChecked():
                selected_option = "1 stars"
                self.data['customer 1']["ratings"][self.dropdown.currentText()] = 1
            elif self.radio2.isChecked():
                selected_option = "2 stars"
                self.data['customer 1']["ratings"][self.dropdown.currentText()] = 2
            elif self.radio3.isChecked():
                selected_option = "3 stars"
                self.data['customer 1']["ratings"][self.dropdown.currentText()] = 3
            elif self.radio4.isChecked():
                selected_option = "4 stars"
                self.data['customer 1']["ratings"][self.dropdown.currentText()] = 4
            elif self.radio5.isChecked():
                selected_option = "5 stars"
                self.data['customer 1']["ratings"][self.dropdown.currentText()] = 5
            else:
                selected_option = "No option selected"

            # Show a message box with the selected option
            QMessageBox.information(self, "Selected Option", f"You selected: {selected_option}")

    # Define admin ID window
    class AdminIDWindow(QMainWindow):
        def __init__(self, parents_instance):
            super().__init__()
            self.setWindowTitle("Login admin ID")
            self.resize(400, 300)

            # Create a text input field
            self.adminid_input = QLineEdit()
            self.adminid_input.setPlaceholderText("Enter admin ID")

            # Create a button to open the customer window
            self.button = QPushButton("submit")
            self.button.clicked.connect(self.open_admin_window)

            # Set layout
            central_widget = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(self.adminid_input)
            layout.addWidget(self.button)
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        def open_admin_window(self):
            adminid = self.adminid_input.text()
            if "001" in adminid:
                window_instanceAdmin = assignment1()
                self.customer_window = window_instanceAdmin.AdminPortalWindow(window_instanceAdmin, adminid="001")
                self.customer_window.show()
            else:
                self.customer_window = assignment1.errorWindow("Error!\nInvalid admin ID entered")
                self.customer_window.show()

    # Define admin ID window
    class AdminPortalWindow(QMainWindow):
        def __init__(self, parents_instance, adminid:int):
            super().__init__()
            self.setWindowTitle("Admin portal")
            self.resize(400, 300)
            self.data = {**parents_instance.admins, **parents_instance.customers}
            labels = {}
            logins = {}
            for keys in self.data:
                if "admin" in keys:
                    for key in self.data[keys]:
                        #print(self.data[keys]["admin id"])
                        if self.data[keys]['ID'] == adminid:
                            logins["admin"] = keys
                            logins['failedLogins'] = self.data[keys]['failedLogins']
                            logins['successfulLogins'] = self.data[keys]['successfulLogins']
                    continue
                temp_string = "{} rating\n".format(keys)
                for key in self.data[keys]["ratings"]:
                    print(key)
                    temp_string += "Customer rating for {}={}\n".format(key, str(self.data[keys]["ratings"][key]))
                labels[keys] = QLabel(temp_string)

            label = QLabel("Welcome to the admin portal, admin: {}".format(logins['admin']))
            LoginFailLabel = QLabel("Failed Logins: {}".format(logins['failedLogins']))
            LoginPassLabel = QLabel("Successful Logins: {}".format(logins['successfulLogins']))

            # Set layout
            central_widget = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(LoginFailLabel)
            layout.addWidget(LoginPassLabel)
            for item in labels:
                layout.addWidget(labels[item])
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)


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

            # Create a button to open the customer window
            self.button = QPushButton("submit")
            self.button.clicked.connect(self.open_window)

            # Set layout
            central_widget = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(self.username_input)
            layout.addWidget(self.password_input)
            layout.addWidget(self.button)
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
            #print(parent_instance.customers)

            self.customer_window = None  # Initialize customer window as None

        def open_window(self):
            username = self.username_input.text()
            password = self.password_input.text()
            window_instance = assignment1()
            if username == "customer" and password=="12345":
                self.customer_window = window_instance.customerWindow(window_instance)
                self.customer_window.show()
            elif username == "admin1" and password == "12345":
                self.adminID_window = window_instance.AdminIDWindow(window_instance)
                self.adminID_window.show()
            else:
                self.error_window = assignment1.errorWindow(text="Error!\nInvalid username/password")
                self.error_window.show()

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app_instance = assignment1()
    #main_win = app_instance.AdminPortalWindow(app_instance) #Change to login once done
    main_win = assignment1().MainWindow() #Change to login once done
    main_win.show()
    sys.exit(app.exec_())
