class Bankaccount:
    def __init__(self, account_number, account_holder, balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited: {amount}. New balance: {self.balance}")
        else:
            print("Deposit amount must be positive.")
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew: {amount}. New balance: {self.balance}")
        else:
            print("Insufficient funds or invalid withdrawal amount.")
    def get_balance(self):
        return self.balance
# Example usage:
account = Bankaccount("123456789", "John Doe", 1000)
account.deposit(500)
account.withdraw(200)   
print("Current balance:", account.get_balance())
account.withdraw(2000)  # Attempt to withdraw more than the balance
