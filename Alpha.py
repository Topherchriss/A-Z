class BankAccount:
    """
    A class representing a bank account.

    Attributes:
        account_number (str): The account number associated with the account.
        account_holder (str): The name of the account holder.
        customer_id (str): The unique identifier of the customer.
        default_balance (float): The initial balance of the account.

    Methods:
        deposit(amount: float) -> None:
            Deposit a specified amount into the account.

        withdraw(amount: float) -> None:
            Withdraw a specified amount from the account.

        check_balance() -> float:
            Get the current balance of the account.

        get_transaction_history() -> list:
            Retrieve the transaction history of the account.

        send_notification() -> None:
            Send a notification to the account holder based on account activity.

        set_threshold(threshold: float) -> None:
            Set a threshold amount for the account.

        set_budget(category: str, limit: float) -> None:
            Set a budget limit for a specific spending category.

        budget_spending(category: str, amount: float) -> None:
            Record an expense for a specific spending category.

        get_expense(category: str, amount: float) -> None:
            Record an expense for a specific spending category and update the balance.
    """

    def __init__(self, account_number="", account_holder="", customer_id="", default_balance=0, **kwargs):
        """
        Initialize a new BankAccount instance.

        Parameters:
            account_number (str): The account number associated with the account.
            account_holder (str): The name of the account holder.
            customer_id (str): The unique identifier of the customer.
            default_balance (float): The initial balance of the account.
            **kwargs: Additional keyword arguments.
        """

        self.account_number = account_number
        self.account_holder = account_holder
        self.customer_id = customer_id
        self.account_balance = default_balance
        self.transaction_history = kwargs.get("transaction_history", [])
        self.budget_categories = kwargs.get("budget_categories", {})
        self.cumulative_expenses = kwargs.get("cumulative_expenses", {})
        self.threshold = kwargs.get("threshold", 0.0)

    def to_json(self):
        # Convert transaction_history list to a dictionary
        transaction_history_dict = [
            {"Type of transaction": entry.get("Type of transaction", ""),
             "Amount": entry.get("Amount deposited", 0.0)}
            for entry in self.transaction_history
        ]

        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "customer_id": self.customer_id,
            "account_balance": self.account_balance,
            "transaction_history": transaction_history_dict,
            "budget_categories": self.budget_categories,
            "cumulative_expenses": self.cumulative_expenses,
            "threshold": self.threshold
        }

    @classmethod
    def from_json(cls, data):
        print("Data before creating instance:", data)

        # Initialize instance with default values
        instance = cls()

         # Check if instance is successfully initialized
        if instance:
            print("succesfully initialized")

        # Check if data is a dictionary
            if isinstance(data, dict):
                print("Data is a dictionary. Processing...")

                # Retrieve the transaction history and convert it back to a list
                transaction_history_list = [
                    {"Type of transaction": entry.get("Type of transaction", ""),
                    "Amount deposited": entry.get("Amount", 0.0)}
                    for entry in data.get("transaction_history", [])
                ]

                    # Update instance with data
                instance.account_number = data.get("account_number", "")
                instance.account_holder = data.get("account_holder", "")
                instance.customer_id = data.get("customer_id", "")
                instance.default_balance = data.get("account_balance", 0)
                instance.transaction_history = transaction_history_list
                instance.budget_categories = data.get("budget_categories", {})
                instance.cumulative_expenses = data.get("cumulative_expenses", {})
                instance.threshold = data.get("threshold", 0)

                print("Created instance:", instance)
            else:
                print("Invalid data format. Expected dictionary.")
        return instance



    def set_budget(self, category, limit):
        self.budget_categories[category] = limit

    def budget_spending(self, category, amount):

        if category not in self.budget_categories:
            print(f"Dear {self.account_holder} category: {category} not set!")
            return

        if amount > 0:
            self.account_balance -= amount

            #check aganist budget limit
            if amount > self.budget_categories[category]:
                print(f"Dear {self.account_holder} you have exceded your budget for {category}")

            self.transaction_history.append({"Type of transaction": "Expense", "Category": category, "Amount spent": amount})

            self.send_notification()
            print(f"Expense of {amount} from {category} was successful. Your new balance is {
                self.account_balance}")
        else:
            print(f"Invalid expense amount {amount}. Please insert a positive value")
            return


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
        if self.account_balance <= self.threshold:
            print(f"Notification: Your account balance is below ${self.threshold}.")

    def get_expense(self, category, amount):

        if category not in self.budget_categories:
            print(f"Category '{category}' not found in budget.")
            return

        if category not in self.cumulative_expenses:
            self.cumulative_expenses[category] = 0

        limit = self.budget_categories[category]

        if amount + self.cumulative_expenses[category] > limit:
            print("Exceeding budget limit")
            return


        else:
            self.account_balance -= amount

            self.cumulative_expenses[category] += amount  # Increment cumulative expenses

            limit_after_spending = self.budget_categories[category] - amount
            self.budget_categories[category] -= amount

            print(f"You have succesfully spent {amount} form category {category} remainig ${limit_after_spending}")

            self.transaction_history.append({"Type of transaction": "Expense", "Category": category, "Amount spent": amount})
            self.send_notification()

            return limit_after_spending


    def set_threshold(self, threshold):
        if threshold <= 0 or threshold == '':
            print("Invalid threshold value provided")

        elif threshold > self.account_balance:
            print("Threshold amount cannot exceded current account balance")

        else:
            self.threshold = threshold
            print(f"Dear {self.account_holder} a threshold of ${self.threshold} was succesfully added for account {self.account_number}")

class BankCustomer:

    """
    A class representing a bank customer.

    Attributes:
        customer_name (str): The name of the customer.
        accounts (list): List of associated bank accounts.

    Methods:
        addAccount(account: BankAccount) -> None:
            Add a bank account to the customer's profile.

    """

    def __init__(self, customer_name):

        self.customer_name = customer_name
        self.accounts = []

    def addAccount(self, account):

        """
        Add a bank account to the customer's profile.

        Parameters:
            account (BankAccount): The bank account to be added.

        """
        self.accounts.append(account)

        print(f"Account {account.account_number} added for {self.customer_name}. Thank you for choosing our bank.")


    def total_balance(self):
        total = sum(account.account_balance for account in self.accounts)

        print(f"The total amount in {self.customer_name} accounts is: {total}")


    def __str__(self):
        return str(self.accounts)

"""
To effectivley deal with module dependancies and avoid potential errors i decided to import a module when and only when it's needed during execution

"""

import unittest

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*.py')
    unittest.TextTestRunner().run(test_suite)



import tkinter as tk
from Trapeza_gui import BankInterface

root = tk.Tk()

app = BankInterface(root)

root.protocol("WM_DELETE_WINDOW", app.on_closing)# Set up an event handler for when the application is closed

root.mainloop()
