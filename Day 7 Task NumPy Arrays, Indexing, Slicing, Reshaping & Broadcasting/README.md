# Student Marks Analyzer

## Project Overview
Student Marks Analyzer is a Python application built with NumPy that efficiently stores and analyzes marks of multiple students across different subjects. The application demonstrates practical use of NumPy arrays for data manipulation and analysis operations commonly used in Data Analysis and Machine Learning.

## Features

### 1. Student Dataset
- Stores marks of 12 students
- 5 different subjects: Mathematics, English, Physics, Chemistry, Biology
- All data organized using NumPy arrays

### 2. Array Operations
- **Indexing**: Access specific student records and individual marks
- **Slicing**: Display first 5 students, specific subject marks
- **Reshaping**: Convert 2D array to 1D and reshape back to original
- **Broadcasting**: Apply bonus marks to all students simultaneously

### 3. Marks Analysis
- **Highest Marks**: Overall highest and highest in each subject
- **Lowest Marks**: Overall lowest and lowest in each subject
- **Average Marks**: Average for each student and each subject
- **Total Marks**: Total marks for each student and each subject
- **Performance Summary**: Categorize students into performance levels

### 4. Display Features
- All students' marks in tabular format
- Subject-wise marks display
- Specific student records
- Reshaped data demonstration
- Broadcasting example
- Clear and organized output with proper labels

## Requirements
- Python 3.x
- NumPy library

## Installation

```bash
pip install numpy
```

## Usage

Run the script:

```bash
python student_marks_analyzer.py
```

## Project Structure

```
student_marks_analyzer.py  - Main application file
README.md                  - Project documentation
```

## Code Structure

### Main Functions

1. **display_title()** - Displays application header

2. **display_all_students()** - Shows marks of all 12 students in table format

3. **display_selected_students()** - Uses slicing to show first 5 students

4. **display_subject_wise_marks()** - Shows marks organized by subject using indexing

5. **display_student_with_indexing()** - Demonstrates indexing for specific students

6. **display_marks_reshaping()** - Shows reshaping from (12,5) to 1D and back

7. **display_highest_marks()** - Analyzes highest marks using np.max() and np.argmax()

8. **display_lowest_marks()** - Analyzes lowest marks using np.min() and np.argmin()

9. **display_average_marks()** - Calculates averages using np.mean()

10. **display_total_marks()** - Calculates totals using np.sum()

11. **display_broadcasting_example()** - Demonstrates broadcasting with bonus marks

12. **display_performance_summary()** - Categorizes students by performance level

## Sample Output

```
======================================================================
               STUDENT MARKS ANALYZER
======================================================================


----------------------------------------------------------------------
ALL STUDENTS' MARKS
----------------------------------------------------------------------
Student Name    Mathematics     English         Physics         Chemistry       Biology        
----------------------------------------------------------------------
Ali             95              88              92              85              90             
Fatima          87              92              88              91              89             
Hassan          78              85              80              82              84             
Zainab          92              89              94              90              93             
Ahmed           85              84              82              88              86             
Sara            90              91              89              87              88             
Muhammad        88              86              85              84              87             
Ayesha          93              95              91              92              94             
Usman           82              80              83              81              79             
Noor            89              87              90              86              88             
Bilal           91              90              89              91              90             
Hira            84              83              86              85              82             
----------------------------------------------------------------------


----------------------------------------------------------------------
SUBJECT-WISE MARKS
----------------------------------------------------------------------

Mathematics:
  [95 87 78 92 85 90 88 93 82 89 91 84]

English:
  [88 92 85 89 84 91 86 95 80 87 90 83]

Physics:
  [92 88 80 94 82 89 85 91 83 90 89 86]

Chemistry:
  [85 91 82 90 88 87 84 92 81 86 91 85]

Biology:
  [90 89 84 93 86 88 87 94 79 88 90 82]

----------------------------------------------------------------------


----------------------------------------------------------------------
HIGHEST MARKS ANALYSIS
----------------------------------------------------------------------

Overall Highest Marks: 95
Student: Ali
Subject: Mathematics

Highest marks in each subject:
  Mathematics: 95 - Ali
  English: 95 - Ayesha
  Physics: 94 - Zainab
  Chemistry: 92 - Ayesha
  Biology: 94 - Ayesha

Highest marks for each student:
  Ali: 95 (Mathematics)
  Fatima: 92 (English)
  Hassan: 85 (English)
  Zainab: 94 (Physics)
  Ahmed: 88 (Chemistry)
  Sara: 91 (English)
  Muhammad: 88 (Mathematics)
  Ayesha: 95 (English)
  Usman: 83 (Physics)
  Noor: 90 (Physics)
  Bilal: 91 (Mathematics)
  Hira: 86 (Physics)

----------------------------------------------------------------------


----------------------------------------------------------------------
AVERAGE MARKS ANALYSIS
----------------------------------------------------------------------

Overall Average Marks: 87.42

Average marks for each student:
  Ali: 90.00
  Fatima: 89.40
  Hassan: 81.80
  Zainab: 91.60
  Ahmed: 85.00
  Sara: 89.00
  Muhammad: 86.00
  Ayesha: 93.00
  Usman: 81.00
  Noor: 88.00
  Bilal: 90.20
  Hira: 84.00

Average marks in each subject:
  Mathematics: 87.83
  English: 87.50
  Physics: 87.42
  Chemistry: 86.83
  Biology: 87.50

----------------------------------------------------------------------


----------------------------------------------------------------------
BROADCASTING EXAMPLE - BONUS MARKS
----------------------------------------------------------------------

Bonus marks array: [2 3 1 2 3]
Applied to all students (Broadcasting):

First 3 students with bonus:
Ali: [97 91 93 87 93]
Fatima: [89 95 89 93 92]
Hassan: [80 88 81 84 87]

----------------------------------------------------------------------


----------------------------------------------------------------------
PERFORMANCE SUMMARY
----------------------------------------------------------------------

Excellent (Average >= 90): 4 students
  Ali - 90.00
  Zainab - 91.60
  Ayesha - 93.00
  Bilal - 90.20

Good (Average 80-89): 8 students
  Fatima - 89.40
  Hassan - 81.80
  Ahmed - 85.00
  Sara - 89.00
  Muhammad - 86.00
  Usman - 81.00
  Noor: 88.00
  Hira - 84.00

======================================================================
                    END OF REPORT
======================================================================
```

## Key NumPy Features Used

1. **np.array()** - Create 1D and 2D arrays
2. **Indexing** - Access specific elements (e.g., marks[i, j])
3. **Slicing** - Extract ranges (e.g., marks[0:5])
4. **reshape()** - Change array dimensions
5. **np.max()** - Find maximum values
6. **np.argmax()** - Find index of maximum value
7. **np.unravel_index()** - Convert linear index to multi-dimensional coordinates
8. **np.min()** - Find minimum values
9. **np.argmin()** - Find index of minimum value
10. **np.mean()** - Calculate average values
11. **np.sum()** - Calculate sum of values
12. **Broadcasting** - Apply operations across arrays

## Learning Outcomes

This project teaches:
- How to create and organize data using NumPy arrays
- Proper use of indexing and slicing for data extraction
- Array reshaping for different data representations
- Broadcasting for efficient batch operations
- Using NumPy functions for statistical analysis
- Organizing code into reusable functions
- Professional data presentation and reporting

## Submission Checklist

✅ Student Marks Analyzer runs successfully without errors
✅ NumPy arrays used as primary data structure
✅ Indexing, slicing, reshaping, and broadcasting operations implemented
✅ Clear and organized output with proper labels
✅ README.md updated with project details
✅ Code organized into reusable functions
✅ Changes committed and ready for GitHub push

## Author
Student Marks Analyzer Project

## License
MIT License
