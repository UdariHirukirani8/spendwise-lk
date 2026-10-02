transactions = []

while True:
    print("\n" + "=" * 40)
    print("          SPENDWISE LK")
    print("=" * 40)

    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Transactions")
    print("4. View Balance")
    print("5. Exit")

    choice = input("\nChoose an option: ")

    # -----------------------------
    # 1. ADD INCOME
    # -----------------------------
    if choice == "1":
        print("\n--- Add Income ---")

        try:
            amount = float(input("Enter income amount: Rs. "))
        except ValueError:
            print("Invalid amount. Please enter a number.")
            continue

        category = input("Enter income category: ")
        description = input("Enter description: ")

        transaction = {
            "type": "income",
            "amount": amount,
            "category": category,
            "description": description
        }

        transactions.append(transaction)

        print("\nIncome added successfully!")


    # -----------------------------
    # 2. ADD EXPENSE
    # -----------------------------
    elif choice == "2":
        print("\n--- Add Expense ---")

        try:
            amount = float(input("Enter expense amount: Rs. "))
        except ValueError:
            print("Invalid amount. Please enter a number.")
            continue

        category = input("Enter expense category: ")
        description = input("Enter description: ")

        transaction = {
            "type": "expense",
            "amount": amount,
            "category": category,
            "description": description
        }

        transactions.append(transaction)

        print("\nExpense added successfully!")


    # -----------------------------
    # 3. VIEW TRANSACTIONS
    # -----------------------------
    elif choice == "3":
        print("\n--- Transaction History ---")

        if len(transactions) == 0:
            print("No transactions found.")

        else:
            for index, transaction in enumerate(transactions, start=1):
                print(
                    f"{index}. "
                    f"{transaction['type'].title()} | "
                    f"Rs. {transaction['amount']:.2f} | "
                    f"{transaction['category']} | "
                    f"{transaction['description']}"
                )


    # -----------------------------
    # 4. VIEW BALANCE
    # -----------------------------
    elif choice == "4":
        total_income = 0
        total_expense = 0

        for transaction in transactions:

            if transaction["type"] == "income":
                total_income += transaction["amount"]

            elif transaction["type"] == "expense":
                total_expense += transaction["amount"]

        balance = total_income - total_expense

        print("\n--- Account Summary ---")
        print(f"Total Income   : Rs. {total_income:.2f}")
        print(f"Total Expenses : Rs. {total_expense:.2f}")
        print(f"Balance        : Rs. {balance:.2f}")


    # -----------------------------
    # 5. EXIT
    # -----------------------------
    elif choice == "5":
        print("\nThank you for using SpendWise LK!")
        print("Goodbye!")
        break


    # -----------------------------
    # INVALID MENU OPTION
    # -----------------------------
    else:
        print("\nInvalid option. Please choose between 1 and 5.")