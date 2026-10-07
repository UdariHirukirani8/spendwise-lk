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


# =========================================================
# CATEGORIES
# =========================================================

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


# =========================================================
# MENU
# =========================================================

def show_menu():
    print("\n" + "=" * 50)
    print("                 SPENDWISE LK")
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
    print("10. Category Spending Analytics")
    print("11. Smart Spending Insights")
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

    transaction_date = get_valid_date()

    add_transaction(
        "income",
        amount,
        category,
        description,
        transaction_date
    )

    print("\nIncome added successfully!")


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

    transaction_date = get_valid_date()

    add_transaction(
        "expense",
        amount,
        category,
        description,
        transaction_date
    )

    print("\nExpense added successfully!")


# =========================================================
# VIEW TRANSACTIONS
# =========================================================

def view_transactions():
    print("\n--- Transaction History ---")

    transactions = get_transactions()

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for transaction in transactions:
        display_transaction(transaction)


# =========================================================
# VIEW BALANCE
# =========================================================

def view_balance():
    total_income, total_expense, balance = (
        get_balance_summary()
    )

    print("\n--- Account Summary ---")
    print(f"Total Income   : Rs. {total_income:.2f}")
    print(f"Total Expenses : Rs. {total_expense:.2f}")
    print(f"Balance        : Rs. {balance:.2f}")


# =========================================================
# MONTHLY ANALYTICS
# =========================================================

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

    transactions = get_transactions_by_month(
        year,
        month
    )

    total_income, total_expense, balance = (
        get_monthly_summary(year, month)
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


# =========================================================
# CATEGORY SPENDING ANALYTICS
# =========================================================

def category_spending_analytics():
    print("\n--- Category Spending Analytics ---")

    try:
        year = int(input("Enter year: "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("Invalid month. Please enter a value between 1 and 12.")
            return

    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    category_spending = get_category_spending(
        year,
        month
    )

    if len(category_spending) == 0:
        print("No expense transactions found for this month.")
        return

    total_expense = sum(
        amount
        for category, amount in category_spending
    )

    print(f"\n--- Spending for {year}-{month:02d} ---")

    for category, amount in category_spending:
        percentage = (
            amount / total_expense
        ) * 100

        print(
            f"{category:<15} "
            f"Rs. {amount:>10.2f} "
            f"({percentage:.1f}%)"
        )

    highest_category = category_spending[0][0]
    highest_amount = category_spending[0][1]

    highest_percentage = (
        highest_amount / total_expense
    ) * 100

    print("\n--- Smart Insights ---")

    print(
        f"Highest spending category: "
        f"{highest_category} "
        f"(Rs. {highest_amount:.2f})"
    )

    print(
        f"{highest_category} represents "
        f"{highest_percentage:.1f}% "
        f"of total monthly expenses."
    )

    if highest_percentage >= 50:
        print(
            "Insight: More than half of your monthly "
            "expenses are concentrated in one category."
        )

    elif highest_percentage >= 30:
        print(
            "Insight: A significant portion of your "
            "monthly spending is concentrated in this category."
        )

    else:
        print(
            "Insight: Your spending is relatively "
            "distributed across categories."
        )


# =========================================================
# SMART SPENDING INSIGHTS
# =========================================================

def smart_spending_insights():
    print("\n--- Smart Spending Insights ---")

    try:
        year = int(input("Enter year: "))
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print(
                "Invalid month. "
                "Please enter a value between 1 and 12."
            )
            return

    except ValueError:
        print("Invalid input. Please enter numbers only.")
        return

    current_spending = get_category_spending(
        year,
        month
    )

    if len(current_spending) == 0:
        print("No expense data found for this month.")
        return

    # Previous month calculation
    if month == 1:
        previous_month = 12
        previous_year = year - 1

    else:
        previous_month = month - 1
        previous_year = year

    previous_spending = get_category_spending(
        previous_year,
        previous_month
    )

    current_dict = dict(current_spending)
    previous_dict = dict(previous_spending)

    current_total = sum(
        current_dict.values()
    )

    previous_total = sum(
        previous_dict.values()
    )

    print(
        f"\nCurrent month total expenses : "
        f"Rs. {current_total:.2f}"
    )

    print(
        f"Previous month total expenses: "
        f"Rs. {previous_total:.2f}"
    )

    # -----------------------------------------
    # Overall monthly change
    # -----------------------------------------

    if previous_total > 0:
        change = current_total - previous_total

        change_percentage = (
            change / previous_total
        ) * 100

        if change > 0:
            print(
                f"Overall spending increased by "
                f"Rs. {change:.2f} "
                f"({change_percentage:.1f}%)."
            )

        elif change < 0:
            print(
                f"Overall spending decreased by "
                f"Rs. {abs(change):.2f} "
                f"({abs(change_percentage):.1f}%)."
            )

        else:
            print(
                "Overall spending did not change."
            )

    else:
        print(
            "No previous-month expense data "
            "available for comparison."
        )

    # -----------------------------------------
    # Category comparison
    # -----------------------------------------

    print("\n--- Category Changes ---")

    all_categories = (
        set(current_dict)
        | set(previous_dict)
    )

    changes = []

    for category in sorted(all_categories):
        current_amount = current_dict.get(
            category,
            0
        )

        previous_amount = previous_dict.get(
            category,
            0
        )

        difference = (
            current_amount - previous_amount
        )

        changes.append(
            (
                category,
                difference,
                current_amount,
                previous_amount
            )
        )

        if previous_amount > 0:
            percentage_change = (
                difference / previous_amount
            ) * 100

            if difference > 0:
                print(
                    f"{category}: increased by "
                    f"Rs. {difference:.2f} "
                    f"({percentage_change:.1f}%)"
                )

            elif difference < 0:
                print(
                    f"{category}: decreased by "
                    f"Rs. {abs(difference):.2f} "
                    f"({abs(percentage_change):.1f}%)"
                )

            else:
                print(
                    f"{category}: no change"
                )

        elif current_amount > 0:
            print(
                f"{category}: new spending "
                f"this month "
                f"(Rs. {current_amount:.2f})"
            )

    # -----------------------------------------
    # Biggest increase
    # -----------------------------------------

    highest_increase = max(
        changes,
        key=lambda item: item[1]
    )

    category = highest_increase[0]
    increase = highest_increase[1]

    print("\n--- Key Insights ---")

    if increase > 0:
        print(
            f"Biggest spending increase: "
            f"{category} "
            f"(+Rs. {increase:.2f})"
        )

    else:
        print(
            "No category showed a spending increase."
        )

    # -----------------------------------------
    # Spending concentration
    # -----------------------------------------

    highest_category = max(
        current_dict,
        key=current_dict.get
    )

    highest_amount = (
        current_dict[highest_category]
    )

    concentration = (
        highest_amount / current_total
    ) * 100

    if concentration >= 50:
        print(
            f"Warning: {highest_category} "
            f"accounts for "
            f"{concentration:.1f}% "
            f"of this month's spending."
        )

    elif concentration >= 30:
        print(
            f"Notice: {highest_category} "
            f"is a major expense category "
            f"at {concentration:.1f}% "
            f"of total spending."
        )

    else:
        print(
            "Insight: Spending is relatively "
            "distributed across categories."
        )


# =========================================================
# SET MONTHLY BUDGET
# =========================================================

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

    category = select_category(
        EXPENSE_CATEGORIES
    )

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


# =========================================================
# VIEW BUDGET STATUS
# =========================================================

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

    budgets = get_budgets(
        year,
        month
    )

    if len(budgets) == 0:
        print(
            "No budgets found for this month."
        )
        return

    print(
        f"\n--- Budget Status for "
        f"{year}-{month:02d} ---"
    )

    for category, budget_amount in budgets:
        spent = get_category_expense(
            year,
            month,
            category
        )

        remaining = (
            budget_amount - spent
        )

        if budget_amount > 0:
            percentage = (
                spent / budget_amount
            ) * 100
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
            print(
                "WARNING: You have used over "
                "80% of this budget."
            )


# =========================================================
# DELETE TRANSACTION
# =========================================================

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
            input(
                "\nEnter transaction ID to delete: "
            )
        )

    except ValueError:
        print(
            "Invalid ID. Please enter a number."
        )
        return

    confirm = input(
        f"Are you sure you want to delete "
        f"transaction #{transaction_id}? "
        f"(y/n): "
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
    print("\n--- Edit Transaction ---")

    transactions = get_transactions()

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for transaction in transactions:
        display_transaction(transaction)

    try:
        transaction_id = int(
            input(
                "\nEnter transaction ID to edit: "
            )
        )

    except ValueError:
        print(
            "Invalid ID. Please enter a number."
        )
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
    display_transaction(
        selected_transaction
    )

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
        print(
            "Invalid transaction type."
        )
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


# =========================================================
# MAIN APPLICATION
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
                "\nThank you for using "
                "SpendWise LK!"
            )
            print("Goodbye!")
            break

        else:
            print(
                "\nInvalid option. "
                "Please choose between "
                "1 and 12."
            )


# =========================================================
# PROGRAM ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()