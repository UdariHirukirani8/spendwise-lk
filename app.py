from database import (
    create_tables,
    add_transaction,
    get_transactions,
    get_balance_summary
)


def show_menu():
    print("\n" + "=" * 40)
    print("          SPENDWISE LK")
    print("=" * 40)

    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Balance")
    print("5. Exit")


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

    category = input("Enter income category: ").strip()
    description = input("Enter description: ").strip()

    if category == "":
        print("Category cannot be empty.")
        return

    add_transaction(
        "income",
        amount,
        category,
        description
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

    category = input("Enter expense category: ").strip()
    description = input("Enter description: ").strip()

    if category == "":
        print("Category cannot be empty.")
        return

    add_transaction(
        "expense",
        amount,
        category,
        description
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
        created_at = transaction[5]

        print(
            f"#{transaction_id} | "
            f"{transaction_type.title()} | "
            f"Rs. {amount:.2f} | "
            f"{category} | "
            f"{description} | "
            f"{created_at}"
        )


def view_balance():
    total_income, total_expense, balance = get_balance_summary()

    print("\n--- Account Summary ---")
    print(f"Total Income   : Rs. {total_income:.2f}")
    print(f"Total Expenses : Rs. {total_expense:.2f}")
    print(f"Balance        : Rs. {balance:.2f}")


def main():
    create_tables()

    while True:
        show_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_income()

        elif choice == "2":
            add_expense()

        elif choice == "3":
            view_transactions()

        elif choice == "4":
            view_balance()

        elif choice == "5":
            print("\nThank you for using SpendWise LK!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid option. Please choose between 1 and 5.")


if __name__ == "__main__":
    main()