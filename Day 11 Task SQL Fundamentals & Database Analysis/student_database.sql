-- Day 11: Student Database Analysis System
-- SQLite-compatible schema, sample data, and analysis queries.

PRAGMA foreign_keys = ON;

-- Reset the objects so this script can be run repeatedly.
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Courses;
DROP TABLE IF EXISTS Departments;

-- Store the academic departments available to students.
CREATE TABLE Departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE,
    building TEXT NOT NULL
);

-- Store the courses offered by each department.
CREATE TABLE Courses (
    course_id INTEGER PRIMARY KEY,
    course_code TEXT NOT NULL UNIQUE,
    course_name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    credit_hours INTEGER NOT NULL CHECK (credit_hours BETWEEN 1 AND 6),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Store each student's academic information.
CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    age INTEGER NOT NULL CHECK (age BETWEEN 16 AND 60),
    marks REAL NOT NULL CHECK (marks BETWEEN 0 AND 100),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Sample department data. The Mathematics department intentionally has no students
-- so the LEFT JOIN query demonstrates departments with zero enrollment.
INSERT INTO Departments (department_id, department_name, building) VALUES
    (1, 'Computer Science', 'Technology Block'),
    (2, 'Business Administration', 'Commerce Block'),
    (3, 'Electrical Engineering', 'Engineering Block'),
    (4, 'Mathematics', 'Science Block'),
    (5, 'Data Science', 'Technology Block');

INSERT INTO Courses (course_id, course_code, course_name, department_id, credit_hours) VALUES
    (101, 'CS101', 'Introduction to Programming', 1, 3),
    (102, 'CS205', 'Database Systems', 1, 3),
    (103, 'BBA110', 'Principles of Management', 2, 3),
    (104, 'EE120', 'Circuit Analysis', 3, 4),
    (105, 'MTH101', 'Calculus I', 4, 3),
    (106, 'DS201', 'Statistics for Data Science', 5, 3),
    (107, 'DS220', 'Machine Learning Foundations', 5, 4),
    (108, 'CS310', 'Artificial Intelligence', 1, 3);

INSERT INTO Students (student_id, student_name, department_id, semester, age, marks) VALUES
    (1001, 'Ayesha Khan', 1, 4, 21, 91.5),
    (1002, 'Bilal Ahmed', 1, 2, 19, 78.0),
    (1003, 'Hina Malik', 2, 6, 22, 84.5),
    (1004, 'Omar Farooq', 3, 3, 20, 67.0),
    (1005, 'Sara Iqbal', 5, 4, 21, 95.0),
    (1006, 'Usman Tariq', 2, 2, 19, 72.5),
    (1007, 'Maham Raza', 5, 2, 19, 88.0),
    (1008, 'Zainab Noor', 1, 6, 22, 91.5),
    (1009, 'Hamza Siddiqui', 3, 5, 21, 74.0),
    (1010, 'Laiba Shah', 5, 6, 23, 82.0),
    (1011, 'Daniyal Ali', 2, 4, 21, 89.0),
    (1012, 'Minal Yousaf', 1, 1, 18, 63.5);

-- 1. Display all student records.
SELECT * FROM Students ORDER BY student_id;

-- 2. Filter students who scored at least 80 marks.
SELECT student_id, student_name, marks
FROM Students
WHERE marks >= 80
ORDER BY marks DESC;

-- 3. Sort all students from highest to lowest marks.
SELECT student_id, student_name, marks
FROM Students
ORDER BY marks DESC, student_name;

-- 4. Count the total number of students.
SELECT COUNT(*) AS total_students FROM Students;

-- 5. Calculate the overall average marks.
SELECT ROUND(AVG(marks), 2) AS average_marks FROM Students;

-- 6. Find the highest and lowest marks.
SELECT MAX(marks) AS highest_marks, MIN(marks) AS lowest_marks
FROM Students;

-- 7. Display department-wise student count, including empty departments.
SELECT d.department_name, COUNT(s.student_id) AS student_count
FROM Departments AS d
LEFT JOIN Students AS s ON s.department_id = d.department_id
GROUP BY d.department_id, d.department_name
ORDER BY student_count DESC, d.department_name;

-- 8. Display department-wise average marks, including empty departments.
SELECT d.department_name, ROUND(AVG(s.marks), 2) AS average_marks
FROM Departments AS d
LEFT JOIN Students AS s ON s.department_id = d.department_id
GROUP BY d.department_id, d.department_name
ORDER BY average_marks DESC;

-- 9. INNER JOIN students with their departments.
SELECT s.student_id, s.student_name, d.department_name, s.semester, s.marks
FROM Students AS s
INNER JOIN Departments AS d ON d.department_id = s.department_id
ORDER BY s.student_id;

-- 10. Display top-performing students (marks of 90 or higher).
SELECT student_id, student_name, marks
FROM Students
WHERE marks >= 90
ORDER BY marks DESC, student_name;

-- Advanced 1: GROUP BY and HAVING identify departments whose average is at least 80.
SELECT d.department_name, COUNT(*) AS student_count, ROUND(AVG(s.marks), 2) AS average_marks
FROM Students AS s
INNER JOIN Departments AS d ON d.department_id = s.department_id
GROUP BY d.department_id, d.department_name
HAVING AVG(s.marks) >= 80
ORDER BY average_marks DESC;

-- Advanced 2: A subquery finds students scoring above the overall average.
SELECT student_id, student_name, marks
FROM Students
WHERE marks > (SELECT AVG(marks) FROM Students)
ORDER BY marks DESC;

-- Advanced 3: ROW_NUMBER gives every student a unique rank within their department.
SELECT department_name, student_name, marks,
       ROW_NUMBER() OVER (
           PARTITION BY department_name ORDER BY marks DESC, student_id
       ) AS department_row_number
FROM Students AS s
INNER JOIN Departments AS d ON d.department_id = s.department_id
ORDER BY department_name, department_row_number;

-- Advanced 4: RANK preserves ties, so equal marks receive the same position.
SELECT student_name, marks,
       RANK() OVER (ORDER BY marks DESC) AS overall_rank
FROM Students
ORDER BY overall_rank, student_name;

-- Advanced 5: A CTE calculates department summaries before filtering them.
WITH DepartmentSummary AS (
    SELECT d.department_name,
           COUNT(s.student_id) AS student_count,
           ROUND(AVG(s.marks), 2) AS average_marks
    FROM Departments AS d
    LEFT JOIN Students AS s ON s.department_id = d.department_id
    GROUP BY d.department_id, d.department_name
)
SELECT department_name, student_count, average_marks
FROM DepartmentSummary
WHERE student_count > 0
ORDER BY average_marks DESC;