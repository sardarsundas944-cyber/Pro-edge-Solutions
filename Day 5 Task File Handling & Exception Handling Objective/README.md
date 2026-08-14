# Personal Expense Tracker

A simple and easy-to-use Personal Expense Tracker application built with Python. This application helps you record, manage, and track your daily expenses with proper file storage and error handling.

## Features

- **Add New Expense**: Record daily expenses with title, category, amount, and date
- **View All Expenses**: Display all recorded expenses in a formatted table
- **Search by Category**: Find all expenses in a specific category
- **Delete Expense Record**: Remove unwanted expense records
- **View Expense Summary**: See total spending by category
- **File Storage**: All expenses are automatically saved to a JSON file
- **Exception Handling**: Robust error handling for invalid inputs and file operations

## Requirements

- Python 3.x
- No additional packages required (uses only built-in libraries)

## Installation

1. Clone the repository or download the files
2. Navigate to the project directory:
   ```
   cd "Day 5 Task File Handling & Exception Handling Objective"
   ```

## How to Run

Execute the application using:
```
python expense_tracker.py
```

## Usage

When you run the application, you'll see a menu with 6 options:

```
==================================================
PERSONAL EXPENSE TRACKER
==================================================

Options:
1. Add New Expense
2. View All Expenses
3. Search Expense by Category
4. Delete Expense Record
5. View Expense Summary
6. Exit
```

### Option 1: Add New Expense
- Enter expense title
- Enter expense category (e.g., Food, Transport, Entertainment, Shopping)
- Enter expense amount
- Enter expense date (YYYY-MM-DD format or press Enter for today's date)
- Expense is automatically saved to file

### Option 2: View All Expenses
- Displays all recorded expenses in a table format
- Shows date, title, category, and amount
- Displays total expenses at the bottom

### Option 3: Search by Category
- Enter a category name to find
- Shows all expenses in that category
- Displays the total amount spent in that category

### Option 4: Delete Expense Record
- Shows all expenses with index numbers
- Enter the index number of the expense you want to delete
- The expense is removed and file is updated

### Option 5: View Expense Summary
- Shows total spending by each category
- Displays overall total expenses

### Option 6: Exit
- Closes the application

## File Storage

All expenses are stored in `expenses.json` file in the same directory as the application. This file is automatically created when you add the first expense and updated with each modification.

Example `expenses.json` format:
```json
[
    {
        "title": "Lunch at restaurant",
        "category": "Food",
        "amount": 500,
        "date": "2024-01-15"
    },
    {
        "title": "Taxi fare",
        "category": "Transport",
        "amount": 200,
        "date": "2024-01-15"
    }
]
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid input validation (empty fields, non-numeric amounts)
- Invalid date format
- File read/write errors
- Corrupted JSON file recovery
- Unexpected errors during operations

## Sample Output

### View All Expenses
```
======================================================================
Date        Title                Category         Amount    
======================================================================
2024-01-15  Lunch at restaurant  Food             Rs 500       
2024-01-15  Taxi fare            Transport        Rs 200       
2024-01-16  Movie tickets        Entertainment    Rs 800       
======================================================================
Total Expenses: Rs 1500
======================================================================
```

### Expense Summary
```
==================================================
EXPENSE SUMMARY
==================================================
Entertainment        Rs 800
Food                 Rs 500
Transport            Rs 200
==================================================
Total                Rs 1500
==================================================
```

## Technical Implementation

- **Language**: Python 3.x
- **Libraries Used**:
  - `json`: For file storage and retrieval
  - `os`: For file existence checking
  - `datetime`: For date handling
- **Exception Handling**: Uses try-except-else-finally blocks for all file and input operations
- **Data Validation**: All user inputs are validated before storage

## Project Structure

```
Day 5 Task File Handling & Exception Handling Objective/
├── expense_tracker.py      (Main application file)
├── expenses.json           (Auto-generated data file)
└── README.md              (This file)
```

## Learning Outcomes

This project demonstrates:
1. File handling in Python (JSON format)
2. Exception handling with try-except blocks
3. Input validation and error prevention
4. Data structure management (lists and dictionaries)
5. User interface design with menu-driven application
6. Data persistence across program executions

## Author

Created for Day 5 Task: File Handling & Exception Handling Objective

## Notes

- All expenses are stored in Pakistani Rupees (Rs)
- Expenses persist between program executions
- To reset all expenses, simply delete the `expenses.json` file
- The application is case-insensitive for category searches

## Testing

The application has been tested with:
- Valid expense entries
- Invalid inputs (empty fields, non-numeric amounts)
- Invalid date formats
- File operations and corrupted files
- Multiple expense records
- Deletion and search operations

All features work as expected without errors.
