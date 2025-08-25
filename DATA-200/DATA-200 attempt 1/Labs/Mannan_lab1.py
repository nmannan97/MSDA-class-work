import csv
import hashlib
import time

class Student:
    def __init__(self, first_name, last_name, email, course_id, grade, marks):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.course_id = course_id
        self.grade = grade
        self.marks = marks

    def to_list(self):
        return [self.email, self.first_name, self.last_name, self.course_id, self.grade, self.marks]

class CheckMyGrade:
    def __init__(self):
        self.students = []
        self.load_data()

    def load_data(self):
        self.students = self.load_csv('students.csv')

    def load_csv(self, filename):
        try:
            with open(filename, 'r') as file:
                reader = csv.reader(file)
                data = list(reader)
                return data[1:] if len(data) > 1 else []  # Skip header if data exists
        except FileNotFoundError:
            return []

    def save_csv(self, filename, data, headers):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(data)

    def add_student(self):
        email = input("Enter Student Email: ")
        first_name = input("Enter First Name: ")
        last_name = input("Enter Last Name: ")
        course_id = input("Enter Course ID: ")
        grade = input("Enter Grade: ")
        marks = input("Enter Marks: ")
        new_student = Student(first_name, last_name, email, course_id, grade, marks)
        self.students.append(new_student.to_list())
        self.save_csv('students.csv', self.students, ['Email', 'First Name', 'Last Name', 'Course ID', 'Grade', 'Marks'])
        print("Student added successfully!\n")

    def modify_student(self):
        email = input("Enter Student Email to Modify: ")
        for i, student in enumerate(self.students):
            if student[0] == email:
                print("Modifying student record...")
                first_name = input(f"Enter First Name ({student[1]}): ") or student[1]
                last_name = input(f"Enter Last Name ({student[2]}): ") or student[2]
                course_id = input(f"Enter Course ID ({student[3]}): ") or student[3]
                grade = input(f"Enter Grade ({student[4]}): ") or student[4]
                marks = input(f"Enter Marks ({student[5]}): ") or student[5]
                self.students[i] = [email, first_name, last_name, course_id, grade, marks]
                self.save_csv('students.csv', self.students, ['Email', 'First Name', 'Last Name', 'Course ID', 'Grade', 'Marks'])
                print("Student record updated successfully!\n")
                return
        print("Student not found!\n")

    def delete_student(self):
        email = input("Enter Student Email to Delete: ")
        self.students = [student for student in self.students if student[0] != email]
        self.save_csv('students.csv', self.students, ['Email', 'First Name', 'Last Name', 'Course ID', 'Grade', 'Marks'])
        print("Student deleted successfully!\n")

    def search_student(self):
        email = input("Enter Student Email to Search: ")
        start_time = time.time()
        for student in self.students:
            if student[0] == email:
                end_time = time.time()
                print(f"Search Time: {end_time - start_time:.5f} seconds")
                print("Student Record: ", student)
                return
        print("Student not found!\n")

    def run(self):
        while True:
            print("\nCheckMyGrade Menu:")
            print("1. Add Student")
            print("2. Modify Student")
            print("3. Delete Student")
            print("4. Search Student")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.modify_student()
            elif choice == "3":
                self.delete_student()
            elif choice == "4":
                self.search_student()
            elif choice == "5":
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid choice! Please select a valid option.\n")

if __name__ == "__main__":
    app = CheckMyGrade()
    app.run()
