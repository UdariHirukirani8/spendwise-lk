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
    get_category_expense,
    get_category_spending
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


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def select_category(categories):
    print("\nSelect a category:")

    for index, category in enumerate(
        categories,
        start=1
    ):
        print(
            f"{index}. {category}"
        )

    while True:
        try:
            choice = int(
                input(
                    "Choose category number: "
                )
            )

            if 1 <= choice <= len(categories):
                return categories[
                    choice - 1
                ]

            print(
                "Invalid category."
            )

        except ValueError:
            print(
                "Please enter a number."
            )


def get_valid_amount(message):
    while True:
        try:
            amount = float(
                input(message)
            )

            if amount <= 0:
                print(
                    "Amount must be greater than zero."
                )
                continue

            return amount

        except ValueError:
            print(
                "Invalid amount."
            )


def get_valid_date():
    while True:
        transaction_date = input(
            "Enter transaction date "
            "(YYYY-MM-DD): "
        ).strip()

        try:
            datetime.strptime(
                transaction_date,
                "%Y-%m-%d"
            )

            return transaction_date

        except ValueError:
            print(
                "Invalid date. "
                "Use YYYY-MM-DD."
            )


def display_transaction(
    transaction
):
    print(
        f"#{transaction[0]} | "
        f"{transaction[1].title()} | "
        f"Rs. {transaction[2]:.2f} | "
        f"{transaction[3]} | "
        f"{transaction[4]} | "
        f"Date: {transaction[5]}"
    )


# =========================================================
# MENU
# =========================================================

def show_menu():
    print("\n" + "=" * 50)
    print(
        "                 SPENDWISE LK"
    )
    print("=" * 50)

    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Balance")
    print("5. Delete Transaction")
    print("6. Edit Transaction")
    print("7. Monthly Analytics")
    print("8. Set Monthly Budget")
    print("9. View Budget Status")
    print(
        "10. Category Spending Analytics"
    )
    print(
        "11. Smart Spending Insights"
    )
    print("12. Exit")


# =========================================================
# ADD INCOME
# =========================================================

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

    transaction_date = (
        get_valid_date()
    )

    add_transaction(
        "income",
        amount,
        category,
        description,
        transaction_date
    )

    print(
        "\nIncome added successfully!"
    )


# =========================================================
# ADD EXPENSE
# =========================================================

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

    transaction_date = (
        get_valid_date()
    )

    add_transaction(
        "expense",
        amount,
        category,
        description,
        transaction_date
    )

    print(
        "\nExpense added successfully!"
    )


# =========================================================
# VIEW TRANSACTIONS
# =========================================================

def view_transactions():
    print(
        "\n--- Transaction History ---"
    )

    transactions = get_transactions()

    if not transactions:
        print(
            "No transactions found."
        )
        return

    for transaction in transactions:
        display_transaction(
            transaction
        )


# =========================================================
# VIEW BALANCE
# =========================================================

def view_balance():
    income, expense, balance = (
        get_balance_summary()
    )

    print("\n--- Account Summary ---")

    print(
        f"Total Income   : "
        f"Rs. {income:.2f}"
    )

    print(
        f"Total Expenses : "
        f"Rs. {expense:.2f}"
    )

    print(
        f"Balance        : "
        f"Rs. {balance:.2f}"
    )


# =========================================================
# DELETE TRANSACTION
# =========================================================

def delete_transaction_menu():
    transactions = get_transactions()

    if not transactions:
        print(
            "No transactions found."
        )
        return

    for transaction in transactions:
        display_transaction(
            transaction
        )

    try:
        transaction_id = int(
            input(
                "\nEnter transaction ID "
                "to delete: "
            )
        )

    except ValueError:
        print("Invalid ID.")
        return

    confirm = input(
        "Are you sure? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Delete cancelled.")
        return

    if delete_transaction(
        transaction_id
    ):
        print(
            "Transaction deleted successfully!"
        )

    else:
        print(
            "Transaction ID not found."
        )


# =========================================================
# EDIT TRANSACTION
# =========================================================

def edit_transaction_menu():
    transactions = get_transactions()

    if not transactions:
        print(
            "No transactions found."
        )
        return

    for transaction in transactions:
        display_transaction(
            transaction
        )

    try:
        transaction_id = int(
            input(
                "\nEnter transaction ID "
                "to edit: "
            )
        )

    except ValueError:
        print("Invalid ID.")
        return

    selected = None

    for transaction in transactions:

        if (
            transaction[0]
            == transaction_id
        ):
            selected = transaction
            break

    if selected is None:
        print(
            "Transaction not found."
        )
        return

    print("\n1. Income")
    print("2. Expense")

    type_choice = input(
        "Choose type: "
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
        print("Invalid type.")
        return

    amount = get_valid_amount(
        "Enter new amount: Rs. "
    )

    description = input(
        "Enter description: "
    ).strip()

    transaction_date = (
        get_valid_date()
    )

    success = update_transaction(
        transaction_id,
        transaction_type,
        amount,
        category,
        description,
        transaction_date
    )

    if success:
        print(
            "Transaction updated successfully!"
        )

    else:
        print(
            "Could not update transaction."
        )


# =========================================================
# MONTHLY ANALYTICS
# =========================================================

def monthly_analytics():
    try:
        year = int(
            input("Enter year: ")
        )

        month = int(
            input(
                "Enter month (1-12): "
            )
        )

    except ValueError:
        print("Invalid input.")
        return

    if month < 1 or month > 12:
        print("Invalid month.")
        return

    transactions = (
        get_transactions_by_month(
            year,
            month
        )
    )

    income, expense, balance = (
        get_monthly_summary(
            year,
            month
        )
    )

    print(
        f"\n--- {year}-{month:02d} ---"
    )

    print(
        f"Income  : Rs. {income:.2f}"
    )

    print(
        f"Expense : Rs. {expense:.2f}"
    )

    print(
        f"Balance : Rs. {balance:.2f}"
    )

    print("\nTransactions:")

    if not transactions:
        print(
            "No transactions found."
        )
        return

    for transaction in transactions:
        display_transaction(
            transaction
        )


# =========================================================
# SET BUDGET
# =========================================================

def set_budget_menu():
    try:
        year = int(
            input("Enter year: ")
        )

        month = int(
            input(
                "Enter month (1-12): "
            )
        )

    except ValueError:
        print("Invalid input.")
        return

    if not 1 <= month <= 12:
        print("Invalid month.")
        return

    category = select_category(
        EXPENSE_CATEGORIES
    )

    amount = get_valid_amount(
        "Enter budget: Rs. "
    )

    set_budget(
        year,
        month,
        category,
        amount
    )

    print(
        "Budget saved successfully!"
    )


# =========================================================
# BUDGET STATUS
# =========================================================

def view_budget_status():
    try:
        year = int(
            input("Enter year: ")
        )

        month = int(
            input(
                "Enter month (1-12): "
            )
        )

    except ValueError:
        print("Invalid input.")
        return

    budgets = get_budgets(
        year,
        month
    )

    if not budgets:
        print(
            "No budgets found."
        )
        return

    for category, budget in budgets:

        spent = get_category_expense(
            year,
            month,
            category
        )

        remaining = (
            budget - spent
        )

        percentage = (
            spent / budget
        ) * 100

        print(
            f"\n{category}"
        )

        print(
            f"Budget    : Rs. {budget:.2f}"
        )

        print(
            f"Spent     : Rs. {spent:.2f}"
        )

        print(
            f"Remaining : Rs. {remaining:.2f}"
        )

        print(
            f"Used      : {percentage:.1f}%"
        )

        if spent > budget:
            print(
                "WARNING: Budget exceeded!"
            )

        elif percentage >= 80:
            print(
                "WARNING: More than "
                "80% budget used."
            )


# =========================================================
# CATEGORY ANALYTICS
# =========================================================

def category_spending_analytics():
    try:
        year = int(
            input("Enter year: ")
        )

        month = int(
            input(
                "Enter month (1-12): "
            )
        )

    except ValueError:
        print("Invalid input.")
        return

    spending = get_category_spending(
        year,
        month
    )

    if not spending:
        print(
            "No expense data found."
        )
        return

    total = sum(
        amount
        for category, amount
        in spending
    )

    print(
        f"\n--- Spending "
        f"{year}-{month:02d} ---"
    )

    for category, amount in spending:

        percentage = (
            amount / total
        ) * 100

        print(
            f"{category:<15} "
            f"Rs. {amount:>10.2f} "
            f"({percentage:.1f}%)"
        )


# =========================================================
# SMART SPENDING INSIGHTS
# =========================================================

def smart_spending_insights():
    try:
        year = int(
            input("Enter year: ")
        )

        month = int(
            input(
                "Enter month (1-12): "
            )
        )

    except ValueError:
        print("Invalid input.")
        return

    if not 1 <= month <= 12:
        print("Invalid month.")
        return

    current = dict(
        get_category_spending(
            year,
            month
        )
    )

    if not current:
        print(
            "No expense data found."
        )
        return

    if month == 1:
        previous_year = year - 1
        previous_month = 12

    else:
        previous_year = year
        previous_month = month - 1

    previous = dict(
        get_category_spending(
            previous_year,
            previous_month
        )
    )

    current_total = sum(
        current.values()
    )

    previous_total = sum(
        previous.values()
    )

    print(
        f"\nCurrent expenses : "
        f"Rs. {current_total:.2f}"
    )

    print(
        f"Previous expenses: "
        f"Rs. {previous_total:.2f}"
    )

    if previous_total > 0:

        difference = (
            current_total
            - previous_total
        )

        percentage = (
            difference
            / previous_total
        ) * 100

        if difference > 0:

            print(
                f"Spending increased by "
                f"Rs. {difference:.2f} "
                f"({percentage:.1f}%)."
            )

        elif difference < 0:

            print(
                f"Spending decreased by "
                f"Rs. {abs(difference):.2f} "
                f"({abs(percentage):.1f}%)."
            )

        else:
            print(
                "Spending did not change."
            )

    else:
        print(
            "No previous-month "
            "data available."
        )

    highest_category = max(
        current,
        key=current.get
    )

    highest_amount = (
        current[highest_category]
    )

    percentage = (
        highest_amount
        / current_total
    ) * 100

    print(
        f"\nHighest category: "
        f"{highest_category}"
    )

    print(
        f"Amount: Rs. "
        f"{highest_amount:.2f}"
    )

    print(
        f"Share: "
        f"{percentage:.1f}%"
    )


# =========================================================
# MAIN
# =========================================================

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
            category_spending_analytics()

        elif choice == "11":
            smart_spending_insights()

        elif choice == "12":
            print(
                "\nThank you for using SpendWise LK!"
            )
            print("Goodbye!")
            break

        else:
            print(
                "Invalid option. "
                "Choose between 1 and 12."
            )


if __name__ == "__main__":
    main()