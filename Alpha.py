#import unittest
#import tkinter as tk
#from tkinter import messagebox
#from Trapeza_gui import BankInterface

class BankAccount:
    def __init__(self, account_number, account_holder, customer_id, default_balance = 0):

        self.account_number = account_number
        self.account_holder = account_holder
        self.customer_id = customer_id
        self.account_balance = default_balance
        self.transaction_history = []


    def deposit(self, amount):
        if amount > 10:
            self.account_balance += amount

            self.transaction_history.append({"Type of transaction": "Deposit", "Amount deposited": amount})
            self.send_notification()

            print(f"Dear customer your deposit of {amount} was succesful. Your new balance is: {self.account_balance}")
        else:
            raise ValueError("Invalid deposit amount. Please enter a positive value.")


    def withdraw(self, amount):

        if amount >= 10 and amount <= self.account_balance:
            self.account_balance -= amount

            self.transaction_history.append({"Type of transaction": "withdrawal", "Amount withdrawn": amount})
            self.send_notification()

            print(f"Withdrawl of {amount} was succesful. Your new account balance is {self.account_balance}")
        else:
            raise ValueError(f"Invalid withdrawal amount or Insufficient funds to withdraw: {amount}")


    def checkBalance(self):
        print(f"Your Current account balance is: {self.account_balance}" )


    def get_transaction_history(self):
        return self.transaction_history


    def send_notification(self):

        # Check for significant events
        if self.transaction_history:
            last_transaction = self.transaction_history[-1]

            #check for large deposit
            if last_transaction["Type of transaction"].lower() == "deposit" and last_transaction["Amount deposited"] >= 50000:
                print("Notification: A large deposit was made to your account.")

            #check or large withdrawals
            elif last_transaction["Type of transaction"].lower() == "withdrawal" and last_transaction["Amount withdrawn"] >= 5000:
                print("Notification: A large withdrawal was made from your account.")

        # Check balance threshold
        threshold = 100
        if self.account_balance <= 100:
            print(f"Notification: Your account balance is below ${threshold}.")

class BankCustomer:

    def __init__(self, customer_name):

        self.customer_name = customer_name
        self.accounts = []

    def addAccount(self, account):


        self.accounts.append(account)

        print(f"Account {account.account_number} added for {self.customer_name}. Thank you for choosing our bank.")


    def total_balance(self):
        total = sum(account.account_balance for account in self.accounts)

        print(f"The total amount in {self.customer_name} accounts is: {total}")


    def __str__(self):
        return str(self.accounts)

import unittest

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests',pattern='test_Alpha.py')
    unittest.TextTestRunner().run(test_suite)


import tkinter as tk
from Trapeza_gui import BankInterface

root = tk.Tk()
app = BankInterface(root)
root.mainloop()
