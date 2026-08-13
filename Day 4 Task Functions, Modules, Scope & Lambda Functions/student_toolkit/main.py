from student_toolkit import student_info, academic, utility

GLOBAL_NOTE = 'This is a global variable'

def add_student_interactive():
    sid = input('Enter student id: ')
    name = input('Enter student name: ')
    n = input('Enter number of subjects: ')
    try:
        n = int(n)
    except:
        n = 3
    marks = []
    for i in range(n):
        m = input(f'Enter mark for subject {i+1}: ')
        try:
            marks.append(int(m))
        except:
            marks.append(0)
    student = student_info.add_student_info(sid, name, marks)
    print('Added', student)

def display_students():
    students = student_info.display_student_information()
    if not students:
        print('No students found')
        return
    for s in students:
        total = academic.calculate_total(s['marks'])
        avg = academic.calculate_average(s['marks'])
        perc = academic.calculate_percentage(s['marks'])
        grade = academic.calculate_grade(perc)
        print(s, 'Total:', total, 'Average:', avg, 'Percentage:', perc, 'Grade:', grade)

def update_student_interactive():
    sid = input('Enter student id to update: ')
    s = student_info.get_student_by_id(sid)
    if not s:
        print('Student not found')
        return
    name = input('Enter new name (leave blank to keep): ')
    marks_input = input('Enter new marks separated by space (leave blank to keep): ')
    marks = None
    if marks_input.strip():
        parts = marks_input.split()
        marks = []
        for p in parts:
            try:
                marks.append(int(p))
            except:
                marks.append(0)
    updated = student_info.update_student_information(sid, name or None, marks)
    print('Updated', updated)

def academic_operations():
    sid = input('Enter student id for academic operations: ')
    s = student_info.get_student_by_id(sid)
    if not s:
        print('Student not found')
        return
    marks = s['marks']
    total = academic.calculate_total(marks)
    avg = academic.calculate_average(marks)
    perc = academic.calculate_percentage(marks)
    grade = academic.calculate_grade(perc)
    print('Total:', total, 'Average:', avg, 'Percentage:', perc, 'Grade:', grade)

def utility_operations():
    students = student_info.display_student_information()
    if not students:
        print('No students available')
        return
    print('1 Find highest marks')
    print('2 Find lowest marks')
    print('3 Sort student marks for a student')
    print('4 Search student record')
    print('5 Sort students by name (lambda)')
    print('6 Custom data processing (lambda)')
    choice = input('Choose: ')
    if choice == '1':
        h = utility.find_highest_marks(students)
        print('Highest', h)
    elif choice == '2':
        l = utility.find_lowest_marks(students)
        print('Lowest', l)
    elif choice == '3':
        sid = input('Enter student id: ')
        s = student_info.get_student_by_id(sid)
        if not s:
            print('Not found')
            return
        print('Sorted marks', utility.sort_student_marks(s['marks']))
    elif choice == '4':
        term = input('Enter id or name to search: ')
        res = utility.search_student_record(students, term)
        print('Search results', res)
    elif choice == '5':
        sorted_list = utility.sort_students_by_name(students)
        print('Sorted students', sorted_list)
    elif choice == '6':
        res = utility.custom_data_processing(students, lambda s: {'id': s['id'], 'name': s['name'].upper()})
        print('Custom processed', res)
    else:
        print('Invalid choice')

def demonstrate_scope():
    print('Global before:', GLOBAL_NOTE)
    local_note = 'This is a local variable'
    print('Local inside function:', local_note)
    def modify_local():
        note = 'modified local'
        return note
    modified = modify_local()
    print('Modified local returned:', modified)
    def modify_global():
        global GLOBAL_NOTE
        GLOBAL_NOTE = 'Global modified inside function'
    modify_global()
    print('Global after modification:', GLOBAL_NOTE)

def menu():
    while True:
        print('\nStudent Utility Toolkit')
        print('1 Add Student Information')
        print('2 Display Student Information')
        print('3 Update Student Information')
        print('4 Academic Operations')
        print('5 Utility Operations')
        print('6 Scope Demonstration')
        print('7 Exit')
        choice = input('Enter choice: ')
        if choice == '1':
            add_student_interactive()
        elif choice == '2':
            display_students()
        elif choice == '3':
            update_student_interactive()
        elif choice == '4':
            academic_operations()
        elif choice == '5':
            utility_operations()
        elif choice == '6':
            demonstrate_scope()
        elif choice == '7':
            print('Exiting')
            break
        else:
            print('Invalid choice')

if __name__ == '__main__':
    menu()
