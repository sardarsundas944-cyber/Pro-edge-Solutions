STUDENTS = []

def add_student_info(student_id, name, marks):
    student = {'id': str(student_id), 'name': name, 'marks': marks}
    STUDENTS.append(student)
    return student

def display_student_information():
    return STUDENTS

def update_student_information(student_id, name=None, marks=None):
    for s in STUDENTS:
        if s['id'] == str(student_id):
            if name is not None:
                s['name'] = name
            if marks is not None:
                s['marks'] = marks
            return s
    return None

def get_student_by_id(student_id):
    for s in STUDENTS:
        if s['id'] == str(student_id):
            return s
    return None
