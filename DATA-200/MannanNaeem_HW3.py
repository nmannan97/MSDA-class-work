import os
import json

class HW3:

    def __init__(self, start="screen1"):
        self.window = start
        self.JSON = None
        if not os.path.isfile("DATA-200/Files/hw3.json"):
            with open("DATA-200/Files/hw3.json", 'w') as f:
                f.write({})
                f.close()

        with open("DATA-200/Files/hw3.json", 'r') as f:
            self.JSON = json.load(f)

    def screen_1(self):
        print("welcome to the admin or customer screen")
        output = input("Are you customer or admin? Or type exit\n")
        while self.window == "screen1":
            if output.lower() == "customer":
                self.window = "screen3"
            elif output.lower() == "admin":
                self.window = "screen2"
            elif output.lower() == "exit":
                self.window = "exit"
            else:
                print("try again")
                output = input("Are you customer or admin? Or type exit\n")
            print(f"self.window screen:\n{self.window}")

    def screen_2(self): #Admin screen
        print("welcome to the admin screen")
        print("Select the number of what you want to do:\n" \
        "(1) reset a password\n(2) reset a username\n(3) product addition" \
        "(4) product deletion\n(5)product inventory update\n(6) list users\n(7) list product detail\n" \
        "(8) list order details\n(9) list product by catagory\n(10) EXIT")
        output = input("Select number now\n")
        while self.window != "exit":
            if output.lower() == "customer":
                self.window = "screen3"
            elif output.lower() == "admin":
                self.window = "screen2"
            elif output.lower() == "exit":
                self.window = "exit"
            else:
                print("try again")
                output = input("Are you customer or admin? Or type exit\n")
            print(f"self.window screen:\n{self.window}")

    def screen_3(self): #Customer screen
        pass

if __name__ == "__main__":
    program = HW3()

    while program.window != "exit":
        if program.window == "screen1":
            program.screen_1()
        elif program.window == "screen2":
            program.screen_2()
        elif program.window == "screen3":
            program.screen_1()


"""
Question 1 Marks (10)

Note: You do not need to build GUI based pages for this, you need to design it as a console based application. All the data can be stored in json data for representation and text files for the databases. If someone wants to use MYSQL or any other databases, please feel free to use but not a hard requirement for this HW.

You need to design online store based application which has following feature.Primarily, the scope pertains to the E-Store product features for making XYZ Electronics and Home Entertainment project live. It focuses on the company, the stakeholders and applications,  which allow for online sales, distribution and marketing of electronics. It has following subsystem:

The online store can show all the products that are available. You can list this in Json format when user prompt to show the available products. User can choose the product by entering the number in console, and user must be able to see the json output of the product detail. This online application must be capable to add/delete the products from list of products. User can login in the system using his email and password, you can maintain the list in file where the primary key is email id of the user. Also, user password is encrypted and can be encrypted during login for the comparison. Once user is logged in the application, he is able to checkout and order the product. Once the order is placed, inventory at the XYZ company must update and order must dispatch.

You need to implement it using object oriented design and develop classes like Category, Product, ShoppingCart, SelectedProduct, OrderDetails, Customer etc and make sure you have proper inheritance/composition for this program.  You need to attach the output of following screens:

Implmentation Details

1) Screen One  (Admin Screen and Welcome Screen)

     Showing the Welcome Screen and option to login in the system as Customer or Admin

   Once Logged in as Admin, you can manage the reset user password/users/product addition/deletion/inventory update and list user details, product details , order details and product by category.

2) Screen Two ( Customer Screen)

    Login screen , customer enters the email id and password. If the record matches, he should be able to login. Otherwise, user must have an option to create his account.

    Customer can see all order details he placed

     Customer can see all the products and choose the product, he can also place the order and checkout. Once the order is placed, inventory must update at the product inventory.

Capture all the screen output and show IS-A/HAS-A relationship diagram along with other class diagram. Also, check gif you are using association/aggregation? If yes, explain why we need it.

 

Q2: Discuss the Aggregation/Association/IS-A/HAS-A class relationship in python with diagrams and small example code. You can upload the PDF. ( 5 Marks)

 

Q3:  You need to develop this program in Object Oriented Programming App ( 5 Marks)

Develop a tool for MealPlan. The main idea is that Health app should create a meal plan for the customers based on their health condition. Customers have targets such as reducing weight and customer must be able to track the progress.
Basic Requirements
The Health app must support add, edit, delete and list customers.
The Health app should be able to check detailed information for a selected client, this includes the meals plan, body type and weight etc.
The Health app must be able to design mean plan based on calories and nutrients.
The health app can provide weekly report and should be able to different meals such as Dinner/Breakfast/Lunch

"""

