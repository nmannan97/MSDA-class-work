import sys
from PyQt5.QtWidgets import *

class Assignment1:
    def __init__(self):
        self.customers = {
            "customer1": {
                "password": "12345",
                "ratings": {
                    "TV": 0,
                    "Radio": 0,
                    "mobile phone": 0,
                    "laptop": 0
                }
            }
        }
        self.admins = {
            "admin1": {
                "password": "12345",
                "ID": "001",
                "failedLogins": 0,
                "successfulLogins": 0
            },
            "admin2": {
                "password": "12345",
                "ID": "002",
                "failedLogins": 0,
                "successfulLogins": 0
            }
        }

    class ErrorWindow(QWidget):
        def __init__(self, text=""):
            super().__init__()
            self.setWindowTitle("Error")
            self.resize(300, 200)

            layout = QVBoxLayout()
            label = QLabel(text if text else "ERROR! Try again.")
            layout.addWidget(label)
            self.setLayout(layout)

    class CustomerWindow(QWidget):
        def __init__(self, parent_instance):
            super().__init__()
            self.setWindowTitle("Customer Rating")
            self.resize(450, 350)
            self.data = parent_instance.customers  # Store reference to main data

            # Dropdown menu
            self.dropdown = QComboBox()
            self.dropdown.addItems(["TV", "Radio", "mobile phone", "laptop"])

            # Radio buttons for ratings
            self.rating_group = QButtonGroup(self)
            self.radio_buttons = []
            for i in range(1, 6):
                btn = QRadioButton(f"{i} stars")
                self.rating_group.addButton(btn, i)
                self.radio_buttons.append(btn)

            # Button to submit rating
            self.button = QPushButton("Submit Rating")
            self.button.clicked.connect(self.submit_rating)

            # Layout setup
            layout = QVBoxLayout()
            layout.addWidget(QLabel("Select Product:"))
            layout.addWidget(self.dropdown)
            layout.addWidget(QLabel("Rate the Product:"))
            for btn in self.radio_buttons:
                layout.addWidget(btn)
            layout.addWidget(self.button)
            self.setLayout(layout)

        def submit_rating(self):
            selected_product = self.dropdown.currentText()
            selected_rating = self.rating_group.checkedId()  # Get selected rating

            # Store rating
            self.data["customer1"]["ratings"][selected_product] = selected_rating
            QMessageBox.information(self, "Success", f"You rated {selected_product} as {selected_rating} stars!")

    class AdminIDWindow(QMainWindow):
        def __init__(self, parent_instance, admin_user):
            super().__init__()
            self.setWindowTitle("Admin Login")
            self.resize(400, 200)
            self.parent_instance = parent_instance  # Store reference
            self.admin_user = admin_user

            self.adminid_input = QLineEdit()
            self.adminid_input.setPlaceholderText("Enter Admin ID")
            self.button = QPushButton("Submit")
            self.button.clicked.connect(self.verify_admin)

            layout = QVBoxLayout()
            layout.addWidget(self.adminid_input)
            layout.addWidget(self.button)
            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        def verify_admin(self):
            admin_id = self.adminid_input.text()
            for admin, details in self.parent_instance.admins.items():
                if details["ID"] == admin_id and admin == self.admin_user:
                    self.parent_instance.admins[admin]['successfulLogins'] += 1
                    self.admin_window = Assignment1.AdminPortalWindow(self.parent_instance, admin_id)
                    self.admin_window.show()
                    self.close()
                    return
            self.parent_instance.admins[admin]['failedLogins'] += 1
            QMessageBox.warning(self, "Error", "Invalid Admin ID!")

    class AdminPortalWindow(QMainWindow):
        def __init__(self, parent_instance, admin_id):
            super().__init__()
            self.setWindowTitle("Admin Portal")
            self.resize(400, 400)
            self.data = parent_instance.customers  # Get customer data
            self.admin_data = parent_instance.admins

            # Get login details
            admin_name = [name for name, details in self.admin_data.items() if details["ID"] == admin_id][0]
            failed_logins = self.admin_data[admin_name]["failedLogins"]
            successful_logins = self.admin_data[admin_name]["successfulLogins"]

            # Labels for login stats
            label = QLabel(f"Welcome Admin: {admin_name}")
            login_fail_label = QLabel(f"Failed Logins: {failed_logins}")
            login_pass_label = QLabel(f"Successful Logins: {successful_logins}")

            # Display customer ratings
            ratings_labels = []
            for customer, info in self.data.items():
                text = f"{customer} Ratings:\n" + "\n".join(f"{item}: {rating}" for item, rating in info["ratings"].items())
                ratings_labels.append(QLabel(text))

            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(login_fail_label)
            layout.addWidget(login_pass_label)
            for lbl in ratings_labels:
                layout.addWidget(lbl)

            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

    class MainWindow(QMainWindow):
        def __init__(self, parent_instance):
            super().__init__()
            self.setWindowTitle("Login")
            self.resize(400, 200)
            self.parent_instance = parent_instance  # Store reference

            # Input fields
            self.username_input = QLineEdit()
            self.password_input = QLineEdit()
            self.username_input.setPlaceholderText("Enter username")
            self.password_input.setPlaceholderText("Enter password")
            self.password_input.setEchoMode(QLineEdit.Password)  # Hide password input

            # Submit button
            self.button = QPushButton("Submit")
            self.button.clicked.connect(self.authenticate)

            layout = QVBoxLayout()
            layout.addWidget(self.username_input)
            layout.addWidget(self.password_input)
            layout.addWidget(self.button)
            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

        def authenticate(self):
            username = self.username_input.text()
            password = self.password_input.text()

            if username in self.parent_instance.customers and password == self.parent_instance.customers[username]["password"]:
                self.customer_window = Assignment1.CustomerWindow(self.parent_instance)
                self.customer_window.show()
            elif username in self.parent_instance.admins and password == self.parent_instance.admins[username]["password"]:
                self.admin_id_window = Assignment1.AdminIDWindow(self.parent_instance, username)
                self.admin_id_window.show()
            else:
                QMessageBox.warning(self, "Error", "Invalid username/password!")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_instance = Assignment1()
    main_win = app_instance.MainWindow(app_instance)
    main_win.show()
    sys.exit(app.exec_())

"""
Customer login:
Username: customer1
password: 12345

admin 1 login:
username: admin1
password: 12345
ID: 001

admin 2 login:
username: admin2
password: 12345
ID: 002
"""