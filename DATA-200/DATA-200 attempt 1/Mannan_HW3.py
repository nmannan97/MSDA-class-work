import json
import os
import hashlib

current_directory = os.getcwd()

# Database files
USER_DB = os.path.join(current_directory, "DATA-200", "users.json")
PRODUCT_DB = os.path.join(current_directory, "DATA-200", "products.json")
ORDER_DB = os.path.join(current_directory, "DATA-200", "orders.json")

class assignment3_q1:
    class User:
        def __init__(self, email, password, is_admin=False):
            self.email = email
            self.password = password
            self.is_admin = is_admin

        def save_user(self):
            users = self.load_users()
            users[self.email] = {"password": self.password, "is_admin": self.is_admin}
            with open(USER_DB, "w") as file:
                json.dump(users, file, indent=4)

        def load_users(self):
            try:
                with open(USER_DB, "r") as file:
                    return json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}

        def login(self):
            users = self.load_users()
            if self.email in users and users[self.email]["password"] == self.password:
                return True, users[self.email]["is_admin"]
            return False, False

    class Product:
        def __init__(self, product_id=None, name=None, category=None, price=None, stock=None):
            self.product_id = product_id
            self.name = name
            self.category = category
            self.price = price
            self.stock = stock

        def save_product(self):
            products = self.load_products()
            products[self.product_id] = {
                "name": self.name, "category": self.category, "price": self.price, "stock": self.stock
            }
            with open(PRODUCT_DB, "w") as file:
                json.dump(products, file, indent=4)

        def load_products(self):
            try:
                with open(PRODUCT_DB, "r") as file:
                    content = file.read().strip()
                    if not content:
                        return {}
                    return json.loads(content)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}

        def display_products(self):
            products = self.load_products()
            print(json.dumps(products, indent=4))

    class ShoppingCart:
        def __init__(self):
            self.items = []

        def add_product(self, product_id):
            product_instance = assignment3_q1().Product()
            products = product_instance.load_products()
            if product_id in products and products[product_id]["stock"] > 0:
                self.items.append(products[product_id])
                print(f"Added {products[product_id]['name']} to cart.")
            else:
                print("Product not available.")

        def checkout(self, user_email):
            if not self.items:
                print("Cart is empty.")
                return
            order_instance = assignment3_q1().Order()
            orders = order_instance.load_orders()
            orders[user_email] = self.items
            with open(ORDER_DB, "w") as file:
                json.dump(orders, file, indent=4)
            print("Order placed successfully!")

    class Order:
        def load_orders(self):
            try:
                with open(ORDER_DB, "r") as file:
                    return json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                return {}

    def add_product(self):
        product_id = input("Enter Product ID: ")
        name = input("Enter Product Name: ")
        category = input("Enter Category: ")
        price = float(input("Enter Price: "))
        stock = int(input("Enter Stock Quantity: "))

        product_instance = self.Product(product_id, name, category, price, stock)
        product_instance.save_product()
        print(f"{name} added successfully!")

    def remove_product(self):
        product_instance = self.Product()
        products = product_instance.load_products()
        product_id = input("Enter Product ID to remove: ")
        if product_id in products:
            del products[product_id]
            with open(PRODUCT_DB, "w") as file:
                json.dump(products, file, indent=4)
            print("Product removed successfully!")
        else:
            print("Product not found!")

    def view_all_users(self):
        user_instance = self.User(email="", password="")
        users = user_instance.load_users()
        print(json.dumps(users, indent=4))

    def reset_user_password(self):
        user_instance = self.User(email="", password="")
        users = user_instance.load_users()
        email = input("Enter user email: ")
        if email in users:
            new_password = input("Enter new password: ")
            users[email]["password"] = hashlib.sha256(new_password.encode()).hexdigest()
            with open(USER_DB, "w") as file:
                json.dump(users, file, indent=4)
            print("Password reset successfully!")
        else:
            print("User not found!")

    def admin_menu():
        while True:
            print("\n~~ Admin Dashboard ~~")
            print("1. Add Product")
            print("2. Remove Product")
            print("3. View All Users")
            print("4. Reset User Password")
            print("5. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                assignment3_q1().add_product()
            elif choice == "2":
                assignment3_q1().remove_product()
            elif choice == "3":
                assignment3_q1().view_all_users()
            elif choice == "4":
                assignment3_q1().reset_user_password()
            elif choice == "5":
                print("Logging out...\n")
                break
            else:
                print("Invalid choice, try again!")

class assignment3_q3:

    class Customer:
        def __init__(self, name, age, weight, body_type, target):
            self.name = name
            self.age = age
            self.weight = weight
            self.body_type = body_type
            self.target = target
            self.meal_plan = []

        def update_weight(self, new_weight):
            self.weight = new_weight

        def set_meal_plan(self, meal_plan):
            self.meal_plan = meal_plan

        def get_details(self):
            return {
                "Name": self.name,
                "Age": self.age,
                "Weight": self.weight,
                "Body Type": self.body_type,
                "Target": self.target,
                "Meal Plan": self.meal_plan
            }


    class HealthApp:
        def __init__(self):
            self.customers = []

        def add_customer(self, customer):
            self.customers.append(customer)

        def edit_customer(self, name, new_weight=None, new_target=None):
            for customer in self.customers:
                if customer.name == name:
                    if new_weight:
                        customer.update_weight(new_weight)
                    if new_target:
                        customer.target = new_target
                    return f"{name}'s details updated."
            return "Customer not found."

        def delete_customer(self, name):
            self.customers = [c for c in self.customers if c.name != name]
            return f"{name} has been removed."

        def list_customers(self):
            return [customer.get_details() for customer in self.customers]

        def generate_meal_plan(self, name, meals):
            for customer in self.customers:
                if customer.name == name:
                    customer.set_meal_plan(meals)
                    return f"Meal plan updated for {name}."
            return "Customer not found."

        def weekly_report(self, name):
            for customer in self.customers:
                if customer.name == name:
                    return f"Weekly Report for {name}: {customer.get_details()}"
            return "Customer not found."

if __name__ == "__main__":
    # Example Usage
    app = assignment3_q3().HealthApp()
    cust1 = assignment3_q3().Customer("John Doe", 30, 85, "Ectomorph", "Lose Weight")
    app.add_customer(cust1)
    app.generate_meal_plan("John Doe", ["Breakfast: Oatmeal", "Lunch: Salad", "Dinner: Grilled Chicken"])
    print(app.weekly_report("John Doe"))

    """
    print("Welcome to the Electronics Store!")
    while True:
        choice = input("Are you an Admin or a Customer? (admin/customer/exit): ").lower()
        if choice == "exit":
            break
        elif choice in ["admin", "customer"]:
            email = input("Enter email: ")
            password = input("Enter password: ")
            user = assignment3_q1.User(email, password)
            success, is_admin = user.login()
            if success:
                if is_admin:
                    assignment3_q1.admin_menu()
                else:
                    print("Welcome, Customer!")
                    cart = assignment3_q1.ShoppingCart()
                    product_instance = assignment3_q1.Product()
                    while True:
                        action = input("View products (view), add to cart (add), checkout (checkout), exit (exit): ")
                        if action == "view":
                            product_instance.display_products()
                        elif action == "add":
                            product_id = input("Enter product ID to add: ")
                            cart.add_product(product_id)
                        elif action == "checkout":
                            cart.checkout(email)
                            break
                        elif action == "exit":
                            break
            else:
                print("Invalid credentials!")
    """