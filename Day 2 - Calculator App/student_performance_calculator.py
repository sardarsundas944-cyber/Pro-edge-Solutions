# Student Performance Calculator
# Simple beginner Python Day 2 project

# Collect student information
student_name = input("Enter student name: ")
student_id = input("Enter student ID: ")
department = input("Enter department: ")
semester = input("Enter semester: ")

# Collect marks
math = int(input("Enter Mathematics marks: "))
science = int(input("Enter Science marks: "))
english = int(input("Enter English marks: "))
computer = int(input("Enter Computer marks: "))
history = int(input("Enter History marks: "))

# Calculate total, average and percentage
subjects = 5
total_marks = math + science + english + computer + history
average_marks = total_marks / subjects
percentage = (total_marks / 500) * 100

# Determine pass/fail
if percentage >= 40:
    result = "PASS"
else:
    result = "FAIL"

# Print final report
print("\nStudent Performance Report")
print("---------------------------")
print("Student Name:", student_name)
print("Student ID:", student_id)
print("Department:", department)
print("Semester:", semester)
print("\nMarks")
print("Mathematics:", math)
print("Science:", science)
print("English:", english)
print("Computer:", computer)
print("History:", history)
print("\nTotal Marks:", total_marks)
print("Average Marks:", average_marks)
print("Percentage:", percentage, "%")
print("Result:", result)
