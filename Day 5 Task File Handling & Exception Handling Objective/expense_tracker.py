import json
import os
from datetime import datetime

EXPENSES_FILE = "expenses.json"


def load_expenses():
    try:
        if os.path.exists(EXPENSES_FILE):
            with open(EXPENSES_FILE, "r") as file:
                expenses = json.load(file)
            return expenses
        else:
            return []
    except json.JSONDecodeError:
        print("Error: Corrupted expense file. Starting fresh.")
        return []
    except IOError as e:
        print(f"Error reading file: {e}")
        return []


def save_expenses(expenses):
    try:
        with open(EXPENSES_FILE, "w") as file:
            json.dump(expenses, file, indent=4)
        print("Expenses saved successfully.")
    except IOError as e:
        print(f"Error saving file: {e}")
    except Exception as e:
        print(f"Unexpected error while saving: {e}")


def add_expense(expenses):
    try:
        title = input("Enter expense title: ").strip()
        if not title:
            print("Error: Title cannot be empty.")
            return
        
        category = input("Enter expense category (e.g., Food, Transport, Entertainment): ").strip()
        if not category:
            print("Error: Category cannot be empty.")
            return
        
        amount_input = input("Enter expense amount: ").strip()
        try:
            amount = float(amount_input)
            if amount <= 0:
                print("Error: Amount must be greater than 0.")
                return
        except ValueError:
            print("Error: Invalid amount. Please enter a number.")
            return
        
        date = input("Enter expense date (YYYY-MM-DD) or press Enter for today: ").strip()
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                print("Error: Invalid date format. Use YYYY-MM-DD.")
                return
        
        expense = {
            "title": title,
            "category": category,
            "amount": amount,
            "date": date
        }
        
        expenses.append(expense)
        save_expenses(expenses)
        print(f"Expense added: {title} - Rs {amount}")
        
    except Exception as e:
        print(f"Error adding expense: {e}")


def view_all_expenses(expenses):
    try:
        if not expenses:
            print("No expenses found.")
            return
        
        print("\n" + "="*70)
        print(f"{'Date':<12} {'Title':<20} {'Category':<15} {'Amount':<10}")
        print("="*70)
        
        for expense in expenses:
            print(f"{expense['date']:<12} {expense['title']:<20} {expense['category']:<15} Rs {expense['amount']:<9}")
        
        print("="*70)
        total = sum(expense['amount'] for expense in expenses)
        print(f"Total Expenses: Rs {total}")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"Error viewing expenses: {e}")


def search_by_category(expenses):
    try:
        if not expenses:
            print("No expenses to search.")
            return
        
        category = input("Enter category to search: ").strip()
        if not category:
            print("Error: Category cannot be empty.")
            return
        
        matching_expenses = [e for e in expenses if e['category'].lower() == category.lower()]
        
        if not matching_expenses:
            print(f"No expenses found in category: {category}")
            return
        
        print("\n" + "="*70)
        print(f"Expenses in category: {category}")
        print("="*70)
        print(f"{'Date':<12} {'Title':<20} {'Category':<15} {'Amount':<10}")
        print("="*70)
        
        for expense in matching_expenses:
            print(f"{expense['date']:<12} {expense['title']:<20} {expense['category']:<15} Rs {expense['amount']:<9}")
        
        total = sum(e['amount'] for e in matching_expenses)
        print("="*70)
        print(f"Total in {category}: Rs {total}")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"Error searching expenses: {e}")


def delete_expense(expenses):
    try:
        if not expenses:
            print("No expenses to delete.")
            return
        
        view_all_expenses(expenses)
        
        index_input = input("Enter the index number of the expense to delete (starting from 0): ").strip()
        try:
            index = int(index_input)
            if 0 <= index < len(expenses):
                deleted = expenses.pop(index)
                save_expenses(expenses)
                print(f"Deleted: {deleted['title']} - Rs {deleted['amount']}")
            else:
                print("Error: Invalid index. Please enter a valid number.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")
        
    except Exception as e:
        print(f"Error deleting expense: {e}")


def view_summary(expenses):
    try:
        if not expenses:
            print("No expenses to summarize.")
            return
        
        print("\n" + "="*50)
        print("EXPENSE SUMMARY")
        print("="*50)
        
        categories = {}
        for expense in expenses:
            category = expense['category']
            amount = expense['amount']
            if category in categories:
                categories[category] += amount
            else:
                categories[category] = amount
        
        for category, total in sorted(categories.items()):
            print(f"{category:<20} Rs {total}")
        
        overall_total = sum(expense['amount'] for expense in expenses)
        print("="*50)
        print(f"{'Total':<20} Rs {overall_total}")
        print("="*50 + "\n")
        
    except Exception as e:
        print(f"Error generating summary: {e}")


def main():
    print("\n" + "="*50)
    print("PERSONAL EXPENSE TRACKER")
    print("="*50 + "\n")
    
    expenses = load_expenses()
    
    while True:
        try:
            print("Options:")
            print("1. Add New Expense")
            print("2. View All Expenses")
            print("3. Search Expense by Category")
            print("4. Delete Expense Record")
            print("5. View Expense Summary")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == "1":
                add_expense(expenses)
            elif choice == "2":
                view_all_expenses(expenses)
            elif choice == "3":
                search_by_category(expenses)
            elif choice == "4":
                delete_expense(expenses)
            elif choice == "5":
                view_summary(expenses)
            elif choice == "6":
                print("Thank you for using Personal Expense Tracker!")
                break
            else:
                print("Error: Invalid choice. Please enter a number between 1 and 6.\n")
        
        except KeyboardInterrupt:
            print("\nApplication interrupted by user.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
