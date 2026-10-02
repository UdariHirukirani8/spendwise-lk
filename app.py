from datetime import datetime

from database import (
    create_tables,
    add_transaction,
    get_transactions,
    get_balance_summary,
    delete_transaction

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
    print("\n" + "=" * 40)
    print("          SPENDWISE LK")
    print("=" * 40)

    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Balance")
    print("5. Delete Transaction")
    print("6. Exit")


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


def add_income():
    print("\n--- Add Income ---")

    try:
        amount = float(input("Enter income amount: Rs. "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    category = select_category(INCOME_CATEGORIES)

    description = input("Enter description: ").strip()

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

    try:
        amount = float(input("Enter expense amount: Rs. "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    category = select_category(EXPENSE_CATEGORIES)

    description = input("Enter description: ").strip()

    transaction_date = get_valid_date()

    add_transaction(
        "expense",
        amount,
        category,
        description,
        transaction_date
    )

    print("\nExpense added successfully!")


def view_transactions():
    print("\n--- Transaction History ---")

    transactions = get_transactions()

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for transaction in transactions:
        transaction_id = transaction[0]
        transaction_type = transaction[1]
        amount = transaction[2]
        category = transaction[3]
        description = transaction[4]
        transaction_date = transaction[5]
        created_at = transaction[6]

        print(
            f"#{transaction_id} | "
            f"{transaction_type.title()} | "
            f"Rs. {amount:.2f} | "
            f"{category} | "
            f"{description} | "
            f"Date: {transaction_date} | "
            f"Created: {created_at}"
        )


def view_balance():
    total_income, total_expense, balance = get_balance_summary()

    print("\n--- Account Summary ---")
    print(f"Total Income   : Rs. {total_income:.2f}")
    print(f"Total Expenses : Rs. {total_expense:.2f}")
    print(f"Balance        : Rs. {balance:.2f}")


def delete_transaction_menu():
    print("\n--- Delete Transaction ---")

    transactions = get_transactions()

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for transaction in transactions:
        print(
            f"#{transaction[0]} | "
            f"{transaction[1].title()} | "
            f"Rs. {transaction[2]:.2f} | "
            f"{transaction[3]} | "
            f"{transaction[5]}"
        )

    try:
        transaction_id = int(
            input("\nEnter transaction ID to delete: ")
        )
    except ValueError:
        print("Invalid ID. Please enter a number.")
        return

    confirm = input(
        f"Are you sure you want to delete transaction #{transaction_id}? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Delete cancelled.")
        return

    if delete_transaction(transaction_id):
        print("Transaction deleted successfully!")
    else:
        print("Transaction ID not found.")


def main():
    create_tables()

    while True:
        show_menu()

        choice = input("\nChoose an option: ").strip()

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
            print("\nThank you for using SpendWise LK!")
            print("Goodbye!")
            break


        else:
            print("\nInvalid option. Please choose between 1 and 6.")


if __name__ == "__main__":
    main()