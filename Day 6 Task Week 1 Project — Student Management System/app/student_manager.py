from app.student_data import load_students, save_students


SUBJECTS = ["Math", "Science", "English", "Computer", "History"]


def input_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Please enter a valid value.")


def input_int(prompt, minimum=0, maximum=None):
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Value must be at least {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Value must not be more than {maximum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid integer.")


def display_title():
    print("\n" + "=" * 60)
    print("Student Management System")
    print("=" * 60)


def find_student_by_id(student_id):
    students = load_students()
    for student in students:
        if student.get("student_id") == student_id:
            return student
    return None


def add_student():
    display_title()
    student_id = input_text("Enter Student ID: ")
    if find_student_by_id(student_id):
        print("Student ID already exists.")
        return

    name = input_text("Enter Student Name: ")
    department = input_text("Enter Department: ")
    age = input_int("Enter Age: ", 1, 100)
    email = input_text("Enter Email Address: ")

    student = {
        "student_id": student_id,
        "name": name,
        "department": department,
        "age": age,
        "email": email,
        "marks": {}
    }

    students = load_students()
    students.append(student)
    if save_students(students):
        print("Student added successfully.")
    else:
        print("Unable to save student data.")


def view_all_students():
    display_title()
    students = load_students()
    if not students:
        print("No student records found.")
        return

    print("{:<12} {:<20} {:<15} {:<6} {:<25}".format(
        "Student ID", "Name", "Department", "Age", "Email"
    ))
    for student in students:
        print("{:<12} {:<20} {:<15} {:<6} {:<25}".format(
            student.get("student_id", "N/A"),
            student.get("name", "N/A"),
            student.get("department", "N/A"),
            student.get("age", "N/A"),
            student.get("email", "N/A")
        ))


def search_student_by_id():
    display_title()
    student_id = input_text("Enter Student ID to search: ")
    student = find_student_by_id(student_id)
    if not student:
        print("Student not found.")
        return

    print_student(student)


def print_student(student):
    print("\nStudent Information")
    print("-" * 40)
    print(f"Student ID: {student.get('student_id')}")
    print(f"Name: {student.get('name')}")
    print(f"Department: {student.get('department')}")
    print(f"Age: {student.get('age')}")
    print(f"Email: {student.get('email')}")
    print(f"Marks: {student.get('marks', {})}")


def update_student():
    display_title()
    student_id = input_text("Enter Student ID to update: ")
    students = load_students()
    for student in students:
        if student.get("student_id") == student_id:
            print("Choose field to update:")
            print("1. Name")
            print("2. Department")
            print("3. Age")
            print("4. Email")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                student["name"] = input_text("Enter new name: ")
            elif choice == "2":
                student["department"] = input_text("Enter new department: ")
            elif choice == "3":
                student["age"] = input_int("Enter new age: ", 1, 100)
            elif choice == "4":
                student["email"] = input_text("Enter new email: ")
            else:
                print("Invalid choice.")
                return

            if save_students(students):
                print("Student information updated successfully.")
            else:
                print("Unable to update student information.")
            return

    print("Student not found.")


def delete_student():
    display_title()
    student_id = input_text("Enter Student ID to delete: ")
    students = load_students()
    updated_students = [student for student in students if student.get("student_id") != student_id]
    if len(updated_students) == len(students):
        print("Student not found.")
        return

    if save_students(updated_students):
        print("Student record deleted successfully.")
    else:
        print("Unable to delete student record.")


def enter_student_marks():
    display_title()
    student_id = input_text("Enter Student ID: ")
    student = find_student_by_id(student_id)
    if not student:
        print("Student not found.")
        return

    marks = {}
    for subject in SUBJECTS:
        marks[subject] = input_int(f"Enter mark for {subject}: ", 0, 100)
    student["marks"] = marks

    students = load_students()
    for item in students:
        if item.get("student_id") == student_id:
            item["marks"] = marks
            break

    if save_students(students):
        print("Marks saved successfully.")
    else:
        print("Unable to save marks.")


def calculate_total_marks(student_id):
    student = find_student_by_id(student_id)
    if not student:
        return 0
    marks = student.get("marks", {})
    if not marks:
        return 0
    return sum(marks.values())


def calculate_percentage(student_id):
    student = find_student_by_id(student_id)
    if not student:
        return 0
    marks = student.get("marks", {})
    if not marks:
        return 0
    total = sum(marks.values())
    return (total / (len(marks) * 100)) * 100


def generate_grade(percentage):
    if percentage >= 90:
        return "A+"
    if percentage >= 80:
        return "A"
    if percentage >= 70:
        return "B"
    if percentage >= 60:
        return "C"
    if percentage >= 50:
        return "D"
    return "F"


def display_academic_status():
    display_title()
    student_id = input_text("Enter Student ID: ")
    student = find_student_by_id(student_id)
    if not student:
        print("Student not found.")
        return

    if not student.get("marks"):
        print("No marks entered for this student.")
        return

    total = calculate_total_marks(student_id)
    percentage = calculate_percentage(student_id)
    grade = generate_grade(percentage)

    print("\nAcademic Status")
    print("-" * 40)
    print(f"Student ID: {student_id}")
    print(f"Student Name: {student.get('name')}")
    print(f"Total Marks: {total}")
    print(f"Percentage: {percentage:.2f}%")
    print(f"Grade: {grade}")

    if percentage >= 50:
        print("Status: Pass")
    else:
        print("Status: Fail")


def student_academic_menu():
    while True:
        print("\nAcademic Operations")
        print("1. Enter Student Marks")
        print("2. Calculate Total Marks")
        print("3. Calculate Percentage")
        print("4. Generate Grade")
        print("5. Display Academic Status")
        print("6. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            enter_student_marks()
        elif choice == "2":
            student_id = input_text("Enter Student ID: ")
            marks = calculate_total_marks(student_id)
            print(f"Total Marks: {marks}")
        elif choice == "3":
            student_id = input_text("Enter Student ID: ")
            percent = calculate_percentage(student_id)
            print(f"Percentage: {percent:.2f}%")
        elif choice == "4":
            student_id = input_text("Enter Student ID: ")
            student = find_student_by_id(student_id)
            if not student or not student.get("marks"):
                print("No marks found for this student.")
            else:
                percent = calculate_percentage(student_id)
                print(f"Grade: {generate_grade(percent)}")
        elif choice == "5":
            display_academic_status()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


def main():
    while True:
        display_title()
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Update Student Information")
        print("5. Delete Student Record")
        print("6. Academic Operations")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                add_student()
            elif choice == "2":
                view_all_students()
            elif choice == "3":
                search_student_by_id()
            elif choice == "4":
                update_student()
            elif choice == "5":
                delete_student()
            elif choice == "6":
                student_academic_menu()
            elif choice == "7":
                print("Thank you for using Student Management System.")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception:
            print("An unexpected error occurred. Please try again.")

        input("\nPress Enter to continue...")
