from functools import reduce

def find_highest_marks(students):
    if not students:
        return None
    return max(students, key=lambda s: sum(s['marks']))

def find_lowest_marks(students):
    if not students:
        return None
    return min(students, key=lambda s: sum(s['marks']))

def sort_student_marks(marks):
    return sorted(marks)

def search_student_record(students, term):
    term = str(term).lower()
    result = [s for s in students if term == s['id'].lower() or term in s['name'].lower()]
    return result

def sort_students_by_name(students):
    return sorted(students, key=lambda s: s['name'].lower())

def highest_marks_using_lambda(students):
    return max(students, key=lambda s: sum(s['marks'])) if students else None

def lowest_marks_using_lambda(students):
    return min(students, key=lambda s: sum(s['marks'])) if students else None

def custom_data_processing(students, func):
    return list(map(lambda s: func(s), students))
