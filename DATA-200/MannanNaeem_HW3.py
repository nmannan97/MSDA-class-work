import json
import os
import uuid
import hashlib

DATA_FILE = "store.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"users": {}, "products": {}, "orders": {}}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


class User:
    def __init__(self, email, name, password, is_admin=False):
        self.email = email
        self.name = name
        self.password = hash_pw(password)
        self.is_admin = is_admin

    def to_dict(self):
        return {"email": self.email, "name": self.name,
                "password": self.password, "is_admin": self.is_admin}


class Product:
    def __init__(self, name, price, inventory):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.inventory = inventory

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "inventory": self.inventory}


class ShoppingCart:
    def __init__(self):
        self.items = []

    def add(self, product_id, qty):
        self.items.append({"product_id": product_id, "qty": qty})


class Order:
    def __init__(self, customer_email, items):
        self.id = str(uuid.uuid4())
        self.customer_email = customer_email
        self.items = items

    def to_dict(self):
        return {"id": self.id, "customer_email": self.customer_email, "items": self.items}


class StoreApp:
    def __init__(self):
        self.data = load_data()
        if not any(u.get("is_admin") for u in self.data["users"].values()):
            admin = User("admin@store.com", "Admin", "admin123", True)
            self.data["users"][admin.email] = admin.to_dict()
            save_data(self.data)

    def run(self):
        while True:
            print("\n--- Welcome to XYZ Electronics ---")
            print("1) Admin Login\n2) Customer Login / Register\n0) Exit")
            choice = input("Choose: ")
            if choice == "1":
                self.admin_login()
            elif choice == "2":
                self.customer_login()
            elif choice == "0":
                break

    def admin_login(self):
        email = input("Email: ")
        pw = input("Password: ")
        user = self.data["users"].get(email)
        if not user or not user["is_admin"] or hash_pw(pw) != user["password"]:
            print("Invalid admin login")
            return
        while True:
            print("\n--- Admin Menu ---")
            print("1) Add product\n2) Delete product\n3) List products\n4) List users\n0) Logout")
            choice = input("Choose: ")
            if choice == "1":
                name = input("Name: ")
                price = float(input("Price: "))
                inv = int(input("Inventory: "))
                p = Product(name, price, inv)
                self.data["products"][p.id] = p.to_dict()
                save_data(self.data)
            elif choice == "2":
                pid = input("Product ID to delete: ")
                if pid in self.data["products"]:
                    del self.data["products"][pid]
                    save_data(self.data)
            elif choice == "3":
                print(json.dumps(list(self.data["products"].values()), indent=2))
            elif choice == "4":
                print(json.dumps(list(self.data["users"].values()), indent=2))
            elif choice == "0":
                break

    def customer_login(self):
        print("1) Login\n2) Register\n0) Back")
        choice = input("Choose: ")
        if choice == "1":
            email = input("Email: ")
            pw = input("Password: ")
            user = self.data["users"].get(email)
            if not user or hash_pw(pw) != user["password"]:
                print("Invalid login")
                return
            self.customer_menu(user)
        elif choice == "2":
            email = input("Email: ")
            name = input("Name: ")
            pw = input("Password: ")
            if email in self.data["users"]:
                print("Email already exists")
                return
            u = User(email, name, pw)
            self.data["users"][email] = u.to_dict()
            save_data(self.data)
            print("Account created!")

    def customer_menu(self, user):
        cart = ShoppingCart()
        while True:
            print("\n--- Customer Menu ---")
            print("1) Show products\n2) Add to cart\n3) View cart\n4) Checkout\n5) View my orders\n0) Logout")
            choice = input("Choose: ")
            if choice == "1":
                print(json.dumps(list(self.data["products"].values()), indent=2))
            elif choice == "2":
                pid = input("Product ID: ")
                qty = int(input("Qty: "))
                if pid not in self.data["products"] or self.data["products"][pid]["inventory"] < qty:
                    print("Not enough stock")
                    continue
                cart.add(pid, qty)
            elif choice == "3":
                for item in cart.items:
                    p = self.data["products"][item["product_id"]]
                    print(f"{p['name']} x {item['qty']} @ {p['price']}")
            elif choice == "4":
                if not cart.items:
                    print("Cart empty")
                    continue
                # place order
                for item in cart.items:
                    self.data["products"][item["product_id"]]["inventory"] -= item["qty"]
                order = Order(user["email"], cart.items)
                self.data["orders"][order.id] = order.to_dict()
                cart.items.clear()
                save_data(self.data)
                print(f"Order placed! ID: {order.id}")
            elif choice == "5":
                orders = [o for o in self.data["orders"].values() if o["customer_email"] == user["email"]]
                print(json.dumps(orders, indent=2))
            elif choice == "0":
                break

if __name__ == "__main__":
    app = StoreApp()
    app.run()
