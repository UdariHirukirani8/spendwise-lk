print("=" * 40)
print("          SPENDWISE LK")
print("=" * 40)

print("1. Add Income")
print("2. Add Expense")
print("3. View Transactions")
print("4. View Balance")
print("5. Exit")

choice = input("\nChoose an option: ")

if choice == "1":
    print("\nAdd Income selected")

elif choice == "2":
    print("\nAdd Expense selected")

elif choice == "3":
    print("\nView Transactions selected")

elif choice == "4":
    print("\nView Balance selected")

elif choice == "5":
    print("\nGoodbye!")

else:
    print("\nInvalid option. Please choose between 1 and 5.")