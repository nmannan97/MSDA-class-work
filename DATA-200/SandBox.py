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


# Example Usage
app = HealthApp()
cust1 = Customer("John Doe", 30, 85, "Ectomorph", "Lose Weight")
app.add_customer(cust1)
app.generate_meal_plan("John Doe", ["Breakfast: Oatmeal", "Lunch: Salad", "Dinner: Grilled Chicken"])
print(app.weekly_report("John Doe"))
