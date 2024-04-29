class BankAccount:
    account_number_counter = 101

    def __init__(self, name, email, address, account_type):
        self.account_number = BankAccount.account_number_counter
        BankAccount.account_number_counter += 1
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.history = []
        self.balance = 0
        self.loan_count = 0
        self.loan_amount = 0

    def deposit(self, amount):
        self.balance += amount
        self.history.append(("Deposit", amount, self.balance))
        print(f"{amount} deposited. New balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("not possible")
        else:
            self.balance -= amount
            self.history.append(("withdrow", amount, self.balance))
            print(f"{amount} withdrawn. Remaining balance: {self.balance}")

    def check_balance(self):
        print(f"Available balance: {self.balance}")
        return self.balance

    def show_transactions(self):
        if not self.history:
            print("No transactions found.")
        else:
            for transaction in self.history:
                print(f"Transaction: {transaction[0]}, Amount: {transaction[1]}, Balance: {transaction[2]}")

    def take_loan(self, amount,bank):
        if bank.loan_feature_enabled:
            if self.loan_count >= 2:
                print("Loan limit reached")
            else:
                self.loan_count += 1
                self.loan_amount += amount
                self.balance += amount
                self.history.append(("Loan", amount, self.balance))
                print(f"Loan of {amount} approved. Total loans taken: {self.loan_count}. New balance: {self.balance}")
        else:
            print('Loan system is disabled now')
    def transfer(self, amount, from_account):
        if amount > self.balance:
            print("not possible")
        else:
            self.withdraw(amount)
            from_account.deposit(amount)
            print(f"Transferred {amount} to {from_account.name}")

class Bank:
    def __init__(self):
        self.accounts = {}
        self.loan_feature_enabled = True

    def create_account(self, name, email, address, account_type):
        new_account = BankAccount(name, email, address, account_type)
        self.accounts[new_account.account_number] = new_account
        print(f"Account created for {name}. Account Number: {new_account.account_number}")
        return new_account

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            print(f"Account {account_number} has been deleted.")
        else:
            print("Account not found")

    def list_accounts(self):
        if not self.accounts:
            print("No accounts found.")
        else:
            for account in self.accounts.values():
                print(f"Account Number: {account.account_number}, Name: {account.name}, Balance: {account.balance}")

    def total_balance(self):
        total = sum(account.balance for account in self.accounts.values())
        print(f"Total bank balance: {total}")
        return total

    def total_loans(self):
        total = sum(account.loan_amount for account in self.accounts.values())
        print(f"Total loans: {total}")
        return total

class Admin:
    def __init__(self, bank):
        self.bank = bank

    def create_account(self, name, email, address, account_type):
        return self.bank.create_account(name, email, address, account_type)

    def delete_user_account(self, account_number):
        self.bank.delete_account(account_number)

    def view_all_accounts(self):
        self.bank.list_accounts()

    def check_total_balance(self):
        self.bank.total_balance()

    def check_total_loans(self):
        self.bank.total_loans()

    def loan_setting(self,tmps,bank):
        if tmps == 'on':
            bank.loan_feature_enabled = True
            print('Loan system enabled')
 
        elif tmps == 'off':
            bank.loan_feature_enabled = False
            print('Loan system disabled')

bank = Bank()
admin = Admin(bank)

while True:
    print("-------------Menu--------------")
    print("1. User Menu")
    print("2. Admin Menu")
    print("3. Exit Menu")
    op1 = int(input("Select option: "))
    print(" ")

    if op1 == 1:
        while True:
            print("1. Create a new account")
            print("2. Deposit money")
            print("3. Check balance")
            print("4. Withdraw balance")
            print("5. Transfer money")
            print("6. Take loan")
            print("7. Exit...")
            op2 = int(input("Select option: "))

            if op2 == 1:
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                address = input("Enter your address: ")
                account_type = input("Enter your account type: ")
                account = bank.create_account(name, email, address, account_type)
            elif op2 in [2, 3, 4, 5, 6]:
                tmp = int(input("Enter your account number: "))
                account = bank.get_account(tmp)
                if account:
                    if op2 == 2:
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)
                    elif op2 == 3:
                        account.check_balance()
                    elif op2 == 4:
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)
                    elif op2 == 5:
                        rec_acc_num = int(input("Enter from_account's account number: "))
                        from_account = bank.get_account(rec_acc_num)
                        if from_account:
                            amount = float(input("Enter amount to transfer: "))
                            account.transfer(amount, from_account)
                    elif op2 == 6:
                        amount = float(input("Enter loan amount: "))
                        account.take_loan(amount,bank)
                else:
                    print("invalid account Number")
            elif op2 == 7:
                break 
    elif op1 == 2:
        while True:
            print('Options')
            print(' 1 : Create account')
            print(' 2 : Delete account')
            print(' 3 : Show user list')
            print(' 4 : Total available balance')
            print(' 5 : Total loan amount')
            print(' 6 : Loan feature of the bank')
            print(' 7 : Exit')
            op3 = int(input("Enter the option : "))
            if op3 == 1:
                name = input("Enter your name: ")
                email = input("Enter your email: ")
                address = input("Enter your address: ")
                account_type = input("Enter account type: ")
                admin.create_account(name, email, address, account_type)
            elif op3 == 2:
                account_number = int(input("Enter account number: "))
                admin.delete_user_account(account_number)
            elif op3 == 3:
                admin.view_all_accounts()
            elif op3 == 4:
                admin.check_total_balance()
            elif op3 == 5:
                admin.check_total_loans()
            elif op3 == 6:
                tmps = input("enter only on/off : ")
                admin.loan_setting(tmps,bank)
            elif op3 == 7:
                break
    elif op1 == 3:
        break
    else:
        print("Invalid option")
