import csv
import os
from datetime import datetime

# File to store expenses
EXPENSES_FILE = 'expenses.csv'

# Define categories
CATEGORIES = ['Food', 'Transport', 'Entertainment', 'Bills', 'Other']

def initialize_file():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Description', 'Amount'])
        print(f"Created new expense file: {EXPENSES_FILE}")

def add_expense():
    """Add a new expense entry."""
    date_str = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
    if not date_str:
        date_str = datetime.today().strftime('%Y-%m-%d')
    else:
        # Validate date
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            print("Invalid date format! Use YYYY-MM-DD.")
            return
    
    print("Choose a category:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")
    try:
        cat_choice = int(input("Enter category number: "))
        if not 1 <= cat_choice <= len(CATEGORIES):
            raise ValueError
    except ValueError:
        print("Invalid category choice.")
        return
    category = CATEGORIES[cat_choice - 1]

    description = input("Enter description: ").strip()
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Amount must be a number.")
        return

    # Append expense to file
    with open(EXPENSES_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date_str, category, description, f"{amount:.2f}"])

    print("Expense added successfully!")

def view_summary():
    """Generate and display monthly summary by category."""
    if not os.path.exists(EXPENSES_FILE):
        print("No expenses recorded yet.")
        return

    month_year = input("Enter month and year to view summary (MM-YYYY), or press Enter for current month: ").strip()
    if not month_year:
        month_year = datetime.today().strftime('%m-%Y')
    try:
        datetime.strptime(month_year, '%m-%Y')
    except ValueError:
        print("Invalid format! Use MM-YYYY.")
        return

    summary = {cat: 0.0 for cat in CATEGORIES}
    total = 0.0

    with open(EXPENSES_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date_obj = datetime.strptime(row['Date'], '%Y-%m-%d')
            if date_obj.strftime('%m-%Y') == month_year:
                amount = float(row['Amount'])
                summary[row['Category']] += amount
                total += amount

    print(f"\nExpense Summary for {month_year}:")
    for cat, amt in summary.items():
        print(f"{cat}: ${amt:.2f}")
    print(f"Total: ${total:.2f}\n")

def main():
    initialize_file()
    while True:
        print("\n--- PyExpenseTracker ---")
        print("1. Add Expense")
        print("2. View Monthly Summary")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == '__main__':
    main()
