def calculate_total(marks):
    return sum(marks)

def calculate_average(marks):
    return sum(marks) / len(marks) if marks else 0

def calculate_percentage(marks, max_per_subject=100):
    total = calculate_total(marks)
    count = len(marks)
    if count == 0:
        return 0
    return (total / (count * max_per_subject)) * 100

def calculate_grade(percentage):
    if percentage >= 90:
        return 'A+'
    if percentage >= 80:
        return 'A'
    if percentage >= 70:
        return 'B'
    if percentage >= 60:
        return 'C'
    if percentage >= 50:
        return 'D'
    return 'F'
