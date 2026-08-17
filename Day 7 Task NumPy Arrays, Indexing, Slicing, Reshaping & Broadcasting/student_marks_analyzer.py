import numpy as np

student_names = np.array([
    'Ali', 'Fatima', 'Hassan', 'Zainab', 'Ahmed',
    'Sara', 'Muhammad', 'Ayesha', 'Usman', 'Noor', 'Bilal', 'Hira'
])

subjects = np.array(['Mathematics', 'English', 'Physics', 'Chemistry', 'Biology'])

marks = np.array([
    [95, 88, 92, 85, 90],
    [87, 92, 88, 91, 89],
    [78, 85, 80, 82, 84],
    [92, 89, 94, 90, 93],
    [85, 84, 82, 88, 86],
    [90, 91, 89, 87, 88],
    [88, 86, 85, 84, 87],
    [93, 95, 91, 92, 94],
    [82, 80, 83, 81, 79],
    [89, 87, 90, 86, 88],
    [91, 90, 89, 91, 90],
    [84, 83, 86, 85, 82]
])

def display_title():
    print("\n" + "="*70)
    print(" "*15 + "STUDENT MARKS ANALYZER")
    print("="*70 + "\n")

def display_all_students():
    print("\n" + "-"*70)
    print("ALL STUDENTS' MARKS")
    print("-"*70)
    print(f"{'Student Name':<15} {subjects[0]:<15} {subjects[1]:<15} {subjects[2]:<15} {subjects[3]:<15} {subjects[4]:<15}")
    print("-"*70)
    for i in range(len(student_names)):
        print(f"{student_names[i]:<15} {marks[i,0]:<15} {marks[i,1]:<15} {marks[i,2]:<15} {marks[i,3]:<15} {marks[i,4]:<15}")
    print("-"*70 + "\n")

def display_selected_students():
    print("\n" + "-"*70)
    print("FIRST 5 STUDENTS' MARKS (Using Slicing)")
    print("-"*70)
    selected_marks = marks[0:5]
    print(f"{'Student Name':<15} {subjects[0]:<15} {subjects[1]:<15} {subjects[2]:<15} {subjects[3]:<15} {subjects[4]:<15}")
    print("-"*70)
    for i in range(5):
        print(f"{student_names[i]:<15} {selected_marks[i,0]:<15} {selected_marks[i,1]:<15} {selected_marks[i,2]:<15} {selected_marks[i,3]:<15} {selected_marks[i,4]:<15}")
    print("-"*70 + "\n")

def display_subject_wise_marks():
    print("\n" + "-"*70)
    print("SUBJECT-WISE MARKS")
    print("-"*70)
    for j in range(len(subjects)):
        subject_marks = marks[:, j]
        print(f"\n{subjects[j]}:")
        print(f"  {subject_marks}")
    print("\n" + "-"*70 + "\n")

def display_student_with_indexing():
    print("\n" + "-"*70)
    print("SPECIFIC STUDENT RECORDS (Using Indexing)")
    print("-"*70)
    
    student_2 = marks[1]
    print(f"\nStudent: {student_names[1]}")
    print(f"Marks: {student_2}")
    
    student_5 = marks[4]
    print(f"\nStudent: {student_names[4]}")
    print(f"Marks: {student_5}")
    
    print("\n" + "-"*70 + "\n")

def display_marks_reshaping():
    print("\n" + "-"*70)
    print("RESHAPED MARKS DATA")
    print("-"*70)
    print("\nOriginal Shape:", marks.shape)
    reshaped_marks = marks.reshape(60)
    print("Reshaped to 1D array (60 elements):", reshaped_marks[:10], "...")
    reshaped_back = reshaped_marks.reshape(12, 5)
    print("Reshaped back to original (12, 5):")
    print(reshaped_back[:3])
    print("...")
    print("\n" + "-"*70 + "\n")

def display_highest_marks():
    print("\n" + "-"*70)
    print("HIGHEST MARKS ANALYSIS")
    print("-"*70)
    
    overall_highest = np.max(marks)
    student_with_highest, subject_with_highest = np.unravel_index(np.argmax(marks), marks.shape)
    print(f"\nOverall Highest Marks: {overall_highest}")
    print(f"Student: {student_names[student_with_highest]}")
    print(f"Subject: {subjects[subject_with_highest]}")
    
    print("\nHighest marks in each subject:")
    for j in range(len(subjects)):
        highest_in_subject = np.max(marks[:, j])
        student_index = np.argmax(marks[:, j])
        print(f"  {subjects[j]}: {highest_in_subject} - {student_names[student_index]}")
    
    print("\nHighest marks for each student:")
    for i in range(len(student_names)):
        highest_for_student = np.max(marks[i, :])
        subject_index = np.argmax(marks[i, :])
        print(f"  {student_names[i]}: {highest_for_student} ({subjects[subject_index]})")
    
    print("\n" + "-"*70 + "\n")

def display_lowest_marks():
    print("\n" + "-"*70)
    print("LOWEST MARKS ANALYSIS")
    print("-"*70)
    
    overall_lowest = np.min(marks)
    student_with_lowest, subject_with_lowest = np.unravel_index(np.argmin(marks), marks.shape)
    print(f"\nOverall Lowest Marks: {overall_lowest}")
    print(f"Student: {student_names[student_with_lowest]}")
    print(f"Subject: {subjects[subject_with_lowest]}")
    
    print("\nLowest marks in each subject:")
    for j in range(len(subjects)):
        lowest_in_subject = np.min(marks[:, j])
        student_index = np.argmin(marks[:, j])
        print(f"  {subjects[j]}: {lowest_in_subject} - {student_names[student_index]}")
    
    print("\nLowest marks for each student:")
    for i in range(len(student_names)):
        lowest_for_student = np.min(marks[i, :])
        subject_index = np.argmin(marks[i, :])
        print(f"  {student_names[i]}: {lowest_for_student} ({subjects[subject_index]})")
    
    print("\n" + "-"*70 + "\n")

def display_average_marks():
    print("\n" + "-"*70)
    print("AVERAGE MARKS ANALYSIS")
    print("-"*70)
    
    overall_average = np.mean(marks)
    print(f"\nOverall Average Marks: {overall_average:.2f}")
    
    print("\nAverage marks for each student:")
    student_averages = np.mean(marks, axis=1)
    for i in range(len(student_names)):
        print(f"  {student_names[i]}: {student_averages[i]:.2f}")
    
    print("\nAverage marks in each subject:")
    subject_averages = np.mean(marks, axis=0)
    for j in range(len(subjects)):
        print(f"  {subjects[j]}: {subject_averages[j]:.2f}")
    
    print("\n" + "-"*70 + "\n")

def display_total_marks():
    print("\n" + "-"*70)
    print("TOTAL MARKS ANALYSIS")
    print("-"*70)
    
    print("\nTotal marks for each student:")
    student_totals = np.sum(marks, axis=1)
    for i in range(len(student_names)):
        print(f"  {student_names[i]}: {student_totals[i]}")
    
    print("\nTotal marks in each subject:")
    subject_totals = np.sum(marks, axis=0)
    for j in range(len(subjects)):
        print(f"  {subjects[j]}: {subject_totals[j]}")
    
    print("\nOverall Total Marks: ", np.sum(marks))
    
    print("\n" + "-"*70 + "\n")

def display_broadcasting_example():
    print("\n" + "-"*70)
    print("BROADCASTING EXAMPLE - BONUS MARKS")
    print("-"*70)
    
    bonus_marks = np.array([2, 3, 1, 2, 3])
    marks_with_bonus = marks + bonus_marks
    
    print("\nBonus marks array:", bonus_marks)
    print("Applied to all students (Broadcasting):")
    print("\nFirst 3 students with bonus:")
    for i in range(3):
        print(f"{student_names[i]}: {marks_with_bonus[i]}")
    
    print("\n" + "-"*70 + "\n")

def display_performance_summary():
    print("\n" + "-"*70)
    print("PERFORMANCE SUMMARY")
    print("-"*70)
    
    student_averages = np.mean(marks, axis=1)
    
    excellent = np.sum(student_averages >= 90)
    good = np.sum((student_averages >= 80) & (student_averages < 90))
    average = np.sum((student_averages >= 70) & (student_averages < 80))
    below_avg = np.sum(student_averages < 70)
    
    print(f"\nExcellent (Average >= 90): {excellent} students")
    for i in range(len(student_names)):
        if student_averages[i] >= 90:
            print(f"  {student_names[i]} - {student_averages[i]:.2f}")
    
    print(f"\nGood (Average 80-89): {good} students")
    for i in range(len(student_names)):
        if 80 <= student_averages[i] < 90:
            print(f"  {student_names[i]} - {student_averages[i]:.2f}")
    
    print(f"\nAverage (Average 70-79): {average} students")
    for i in range(len(student_names)):
        if 70 <= student_averages[i] < 80:
            print(f"  {student_names[i]} - {student_averages[i]:.2f}")
    
    print(f"\nBelow Average (Average < 70): {below_avg} students")
    for i in range(len(student_names)):
        if student_averages[i] < 70:
            print(f"  {student_names[i]} - {student_averages[i]:.2f}")
    
    print("\n" + "-"*70 + "\n")

def main():
    display_title()
    
    display_all_students()
    
    display_selected_students()
    
    display_subject_wise_marks()
    
    display_student_with_indexing()
    
    display_marks_reshaping()
    
    display_highest_marks()
    
    display_lowest_marks()
    
    display_average_marks()
    
    display_total_marks()
    
    display_broadcasting_example()
    
    display_performance_summary()
    
    print("="*70)
    print(" "*20 + "END OF REPORT")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
