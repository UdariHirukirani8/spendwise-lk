from datetime import datetime

from database import (
    create_tables,
    add_transaction,
    get_transactions,
    get_balance_summary,
    delete_transaction,
    update_transaction,
    get_transactions_by_month,
    get_monthly_summary,
    set_budget,
    get_budgets,
    get_category_expense
)


INCOME_CATEGORIES = [
    "Salary",
    "Freelance",
    "Business",
    "Allowance",
    "Investment",
    "Other"
]

EXPENSE_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Education",
    "Health",
    "Entertainment",
    "Rent",
    "Other"
]


def select_category(categories):
    print("\nSelect a category:")

    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

    while True:
        try:
            choice = int(input("Choose category number: "))

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

            print("Invalid choice. Please select a valid number.")

        except ValueError:
            print("Please enter a number.")


def show_menu():
    print("\n" + "=" * 45)
    print("              SPENDWISE LK")
    print("=" * 45)

    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Balance")
    print("5. Delete Transaction")
    print("6. Edit Transaction")
    print("7. Monthly Analytics")
    print("8. Set Monthly Budget")
    print("9. View Budget Status")
    print("10 Exit")


def get_valid_date():
    while True:
        transaction_date = input(
            "Enter transaction date (YYYY-MM-DD): "
        ).strip()

        try:
            datetime.strptime(transaction_date, "%Y-%m-%d")
            return transaction_date

        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD format.")


def get_valid_amount(message):
    while True:
        try:
            amount = float(input(message))

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Invalid amount. Please enter a number.")


def add_income():
    print("\n--- Add Income ---")

    amount = get_valid_amount(
        "Enter income amount: Rs. "
    )

    category = select_category(
        INCOME_CATEGORIES
    )

    description = input(
        "Enter description: "
    ).strip()

    transaction_date = get_valid_date()

    add_transaction(
        "income",
        amount,
        category,
        description,
        transaction_date
    )

    print("\nIncome added successfully!")


def add_expense():
    print("\n--- Add Expense ---")

    amount = get_valid_amount(
        "Enter expense amount: Rs. "
    )

    category = select_category(
        EXPENSE_CATEGORIES
    )

    description = input(
        "Enter description: "
    ).strip()

    transaction_date = get_valid_date()

    add_transaction(
        "expense",
        amount,
        category,
        description,
        transaction_date
    )

    print("\nExpense added successfully!")


def display_transaction(transaction):
    transaction_id = transaction[0]
    transaction_type = transaction[1]
    amount = transaction[2]
    category = transaction[3]
    description = transaction[4]
    transaction_date = transaction[5]

    print(
        f"#{transaction_id} | "
        f"{transaction_type.title()} | "
        f"Rs. {amount:.2f} | "
        f"{category} | "
        f"{description} | "
        f"Date: {transaction_date}"
    )


def view_transactions():
    print("\n--- Transaction History ---")

    transactions = get_transactions()

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for transaction in transactions:
        display_transaction(transaction)


def view_balance():
    total_income, total_expense, balance = (
        get_balance_summary()
    )

    print("\n--- Account Summary ---")
    print(
        f"Total Income   : Rs. {total_income:.2f}"
    )
    print(
        f"Total Expenses : Rs. {total_expense:.2f}"
    )
    print(
        f"Balance        : Rs. {balance:.2f}"
    )


def monthly_analytics():
    print("\n--- Monthly Analytics ---")

    try:
        year = int(input("Enter year (e.g. 2026): "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("Invalid month. Please enter a value between 1 and 12.")
            return

    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    transactions = get_transactions_by_month(year, month)

    total_income, total_expense, balance = get_monthly_summary(
        year,
        month
    )

    print(f"\n--- Summary for {year}-{month:02d} ---")
    print(f"Total Income   : Rs. {total_income:.2f}")
    print(f"Total Expenses : Rs. {total_expense:.2f}")
    print(f"Balance        : Rs. {balance:.2f}")

    print("\n--- Transactions ---")

    if len(transactions) == 0:
        print("No transactions found for this month.")
        return

    for transaction in transactions:
        display_transaction(transaction)    

def set_budget_menu():
    print("\n--- Set Monthly Budget ---")

    try:
        year = int(input("Enter year: "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("Invalid month.")
            return

    except ValueError:
        print("Please enter valid numbers.")
        return

    category = select_category(EXPENSE_CATEGORIES)

    amount = get_valid_amount(
        "Enter budget amount: Rs. "
    )

    set_budget(
        year,
        month,
        category,
        amount
    )

    print("\nBudget saved successfully!")


def view_budget_status():
    print("\n--- Budget Status ---")

    try:
        year = int(input("Enter year: "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("Invalid month.")
            return

    except ValueError:
        print("Please enter valid numbers.")
        return

    budgets = get_budgets(year, month)

    if len(budgets) == 0:
        print("No budgets found for this month.")
        return

    print(f"\n--- Budget Status for {year}-{month:02d} ---")

    for category, budget_amount in budgets:
        spent = get_category_expense(
            year,
            month,
            category
        )

        remaining = budget_amount - spent

        if budget_amount > 0:
            percentage = (spent / budget_amount) * 100
        else:
            percentage = 0

        print(
            f"\n{category}"
            f"\nBudget    : Rs. {budget_amount:.2f}"
            f"\nSpent     : Rs. {spent:.2f}"
            f"\nRemaining : Rs. {remaining:.2f}"
            f"\nUsed      : {percentage:.1f}%"
        )

        if spent > budget_amount:
            print(
                f"WARNING: Budget exceeded by "
                f"Rs. {abs(remaining):.2f}"
            )

        elif percentage >= 80:
            print("WARNING: You have used over 80% of this budget.")        


def delete_transaction_menu():
    print("\n--- Delete Transaction ---")

    transactions = get_transactions()

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for transaction in transactions:
        display_transaction(transaction)

    try:
        transaction_id = int(
            input("\nEnter transaction ID to delete: ")
        )

    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    confirm = input(
        f"Are you sure you want to delete "
        f"transaction #{transaction_id}? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Delete cancelled.")
        return

    if delete_transaction(transaction_id):
        print("Transaction deleted successfully!")

    else:
        print("Transaction ID not found.")


def edit_transaction_menu():
    print("\n--- Edit Transaction ---")

    transactions = get_transactions()

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for transaction in transactions:
        display_transaction(transaction)

    try:
        transaction_id = int(
            input("\nEnter transaction ID to edit: ")
        )

    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    selected_transaction = None

    for transaction in transactions:
        if transaction[0] == transaction_id:
            selected_transaction = transaction
            break

    if selected_transaction is None:
        print("Transaction ID not found.")
        return

    print("\nCurrent transaction:")
    display_transaction(selected_transaction)

    print("\nSelect new transaction type:")
    print("1. Income")
    print("2. Expense")

    type_choice = input(
        "Choose transaction type: "
    ).strip()

    if type_choice == "1":
        transaction_type = "income"

        category = select_category(
            INCOME_CATEGORIES
        )

    elif type_choice == "2":
        transaction_type = "expense"

        category = select_category(
            EXPENSE_CATEGORIES
        )

    else:
        print("Invalid transaction type.")
        return

    amount = get_valid_amount(
        "Enter new amount: Rs. "
    )

    description = input(
        "Enter new description: "
    ).strip()

    transaction_date = get_valid_date()

    updated = update_transaction(
        transaction_id,
        transaction_type,
        amount,
        category,
        description,
        transaction_date
    )

    if updated:
        print(
            "\nTransaction updated successfully!"
        )

    else:
        print(
            "\nTransaction could not be updated."
        )


def main():
    create_tables()

    while True:
        show_menu()

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            add_income()

        elif choice == "2":
            add_expense()

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            view_balance()

        elif choice == "5":
            delete_transaction_menu()

        elif choice == "6":
            edit_transaction_menu()

        elif choice == "7":
             monthly_analytics()    

        elif choice == "8":
            set_budget_menu()

        elif choice == "9":
            view_budget_status()
     

        elif choice == "10":
            print(
                "\nThank you for using SpendWise LK!"
            )
            print("Goodbye!")
            break

        else:
            print(
                "\nInvalid option. "
                "Please choose between 1 and 7."
            )


if __name__ == "__main__":
    main()