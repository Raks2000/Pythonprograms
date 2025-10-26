# Simple Banking System

balance = 1000  # initial balance

while True:
    print("\n1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Exit")

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        print("Your balance is:", balance)
    elif choice == '2':
        amount = float(input("Enter deposit amount: "))
        balance += amount
        print("Deposited! New balance:", balance)
    elif choice == '3':
        amount = float(input("Enter withdrawal amount: "))
        if amount <= balance:
            balance -= amount
            print("Withdrawn! New balance:", balance)
        else:
            print("Insufficient balance!")
    elif choice == '4':
        print("Thank you! Goodbye.")
        break
    else:
        print("Invalid option. Try again.")
