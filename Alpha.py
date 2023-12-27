import yaml
from tkinter import messagebox
from exceptions import InsufficientFundsError, InvalidDepositAmountError, InvalidCustomerIDError, InvalidAccountNumberError, InvalidBudgetLimitError, BudgetCategoryNotFoundError, BudgetCategoryAlreadyExistsError, InvalidThresholdAmountError, AccountCreationError, InvalidWithrawalAmountError, WrongCustomerIdError, ExceedingBudgetLimitError, InvalidExpenseAmountError

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

    def __init__(self, account_number="", account_holder="", customer_id="", default_balance=0):
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
        self.transaction_history = []
        self.budget_categories = {}
        self.cumulative_expenses = {}
        self.threshold = 0.0

    def to_yaml(self):
        data = {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "customer_id": self.customer_id,
            "account_balance": self.account_balance,
            "transaction_history": self.transaction_history,
            "budget_categories": self.budget_categories,
            "cumulative_expenses": self.cumulative_expenses,
            "threshold": self.threshold
        }
        return yaml.dump(data, default_flow_style=False)

    @classmethod
    def from_yaml(cls, yaml_str):
        data = yaml.safe_load(yaml_str)
        return cls(
            account_number=data["account_number"],
            account_holder=data["account_holder"],
            customer_id=data["customer_id"],
            default_balance=data["account_balance"],
            transaction_history=data["transaction_history"],
            budget_categories=data["budget_categories"],
            cumulative_expenses=data["cumulative_expenses"],
            threshold=data["threshold"]
        )


    def deposit_money(self, amount, customer_id):
        """
        Deposits funds to the current account.

        Args:
            amount (float): The amount to deposit.
            customer_id (str): The customer ID associated with the account.

        Returns:
            boolean: True if the deposit is successful, False otherwise.
        """
        try:
            amount = float(amount)

            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if amount < 1:
                raise InvalidDepositAmountError("Invalid deposit amount. Please enter a valid number.")


            self.account_balance += amount
            self.transaction_history.append({"Type of transaction": "deposit", "Amount deposited": amount})
            messagebox.showinfo("Success", f"Deposit of ${amount} was successful. Your new account balance is ${self.account_balance}")
            return True

        except ValueError:
            messagebox.showerror("Error", "Invalid deposit amount. Please enter a valid number.")
            return False
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            return False
        except InvalidDepositAmountError as e:
            messagebox.showerror("Error", e.message)
            raise
            return False
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            raise
            return False


    def withdraw_money(self, amount, customer_id):
        """
        Performs a withdrawal from the current account.

        Args:
            amount (float): The amount to withdraw.
            customer_id (str): The customer ID associated with the account.

        Returns:
            boolean: True if the withdrawal is successful, False otherwise.
        """
        try:
            amount = float(amount)

            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if amount > self.account_balance:
                raise InsufficientFundsError("Insufficient funds to proceed with withdrawal.")

            if amount < 1:
                raise InvalidWithrawalAmountError("Invalid withdrawal amount. Please enter a valid number.")

            #Inform the user when the account balance goes below set threshold
            if self.account_balance - amount < self.threshold:
                confirmation_message = (
                    f"Proceeding with the withdrawal of ${amount} will result in a new account balance below "
                    f"the set threshold of ${self.threshold}. Are you sure you want to continue?"
                )

                # Prompt user for confirmation
                confirmation = messagebox.askokcancel("Withdrawal Confirmation", confirmation_message)

                if not confirmation:
                    return False


            self.account_balance -= amount
            self.transaction_history.append({"Type of transaction": "withdrawal", "Amount withdrawn": amount})
            messagebox.showinfo("Success", f"Withdrawal of ${amount} was successful. Your new account balance is {self.account_balance}")
            return True

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return False
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            return False
        except InsufficientFundsError as e:
            messagebox.showerror("Error", e.message)
            print("Insufficient funds to proceed with withdrawal")
            raise
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
        except InvalidWithrawalAmountError as e:
            messagebox.showerror("Error", e.message)
            raise
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return False



    def check_account_balance(self, customer_id, account_number):
        """
        Verifies the account number and customer ID before retrieving the current account balance.

        Args:
            customer_id (str): The customer ID associated with the account.
            account_number (str): The account number to verify.

        Returns:
            boolean: True if the balance retrieval is successful, False otherwise.
        """
        try:

            if not isinstance(account_number, str):
                raise TypeError("Customer account number must be a string.")

            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            return self.account_balance

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please try again.")
            return False
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Error", str(e))



    def account_transactions(self, customer_id, account_number):
        """
        Retrieves and displays the transaction history for the specified customer account.

        Args:
            customer_id (str): The customer ID associated with the account.
            account_number (str): The account number to verify.

        Returns:
            formatted_transactions: A string containing formatted transaction history.

        Raises:
            ValueError: If any input is invalid.
            TypeError: If the customer ID or account number is not a string.
            InvalidCustomerIDError: If the provided customer ID does not match the current customer.
            InvalidAccountNumberError: If the provided account number does not match the current account.
            Exception: Any other unexpected exception encountered.
        """
        try:
            if not isinstance(account_number, str):
                raise TypeError("Customer account number must be a string.")

            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            return self.transaction_history
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input for transaction history: {e}")
        except TypeError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))



    def set_budget_category(self, category, limit, customer_id):
        """
        Sets a budget limit for a specific spending category.

        Args:
            category (str): The name of the spending category.
            limit (float): The maximum amount allowed to be spent in the category.
            customer_id(str): Customer's secret identifier(PIN)

        Raises:
            TypeError: If the customer ID is not a string.
            InsufficientFundsError: if the budget limit exceeds the current account balance.
            InvalidBudgetLimitError: If the budget limit is not a valid number or negative.
            BudgetCategoryAlreadyExistsError: If the category already exists.
        """
        try:
            limit = float(limit)

            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if limit < 0:
                raise InvalidBudgetLimitError("Budget limit cannot be a negative value.")

            if limit > self.account_balance:
                raise InsufficientFundsError("Insufficient funds to proceed, budget limit cannot exceed current account balance.")

            if category in self.budget_categories:
                raise BudgetCategoryAlreadyExistsError(f"Budget category '{category}' already has a limit set.")

            self.budget_categories[category] = limit
            return True

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            raise
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            raise
        except InvalidBudgetLimitError as e:
            messagebox.showerror("Error", e.message)
            raise
        except InsufficientFundsError as e:
            messagebox.showerror("Error", e.message)
            raise
        except Exception as e:
            messagebox.showerror("Error", e.message)


    def get_budget_categories(self, customer_id,):
        """
        Returns a dictionary of all budget categories and their limits.

        Args:
            customer_id (str): Customer secret identifier(PIN)

        Returns:
            dict: A dictionary where keys are category names and values are budget limits.

        Raises:
            TypeError: If the provided customer ID is not a string.
            ValueError: If there's an issue with the customer ID or budget categories.
            Exception: For any other unexpected exceptions.
        """
        try:
            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            return self.budget_categories

        except TypeError as e:
            messagebox.showerror("Error", str(e))
            raise
        except ValueError as e:
            messagebox.showerror("Error", e.message)
            raise
        except Exception as e:
            messagebox.showerror("Error",e.message)
            return False


    def get_budget_category_limit(self, category, customer_id):
        """
        Returns the budget limit for a specific spending category.

        Args:
            category (str): The name of the spending category.
            customer_id(str): Customer secret identifier(PIN)

        Returns:
            float: The budget limit for the specified category.
        """
        try:
            if not isinstance(customer_id, str):
                raise TypeError("Invalid customer ID")

            return self.budget_categories[category]

        except TypeError as e:
            messagebox.showerror("Error", str(e))
            raise
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))



    def set_account_threshold(self, threshold, customer_id):
        """
        Sets the threshold amount for a customer's account.

        Args:
            threshold (float): The minimum account balance that triggers a notification.
            customer_id (str): The customer's unique identifier.

        Raises:
            TypeError: If the customer ID is not a string.
            InsufficientFundsError: if the Threshold exceeds the current account balance.
            InvalidThresholdError: If the threshold is invalid (less than 1).
        """
        try:
            threshold = float(threshold)

            if not isinstance(customer_id, str):
                raise TypeError ("Customer ID must be a string.")

            if threshold < 1:
                raise InvalidThresholdAmountError (f"Threshold must be more than a ${1}")

            if threshold > self.account_balance:
                raise InsufficientFundsError(f"Threshold cannot be more than current account balance.")

            self.threshold = threshold
            messagebox.showinfo("Success", f"Dear {self.account_holder} a threshold of ${self.threshold} was succesfully added for account number {self.account_number}")
            return True

        except ValueError as e:
            messagebox.showerror("Error", e)
            raise
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            raise
        except InvalidThresholdAmountError as e:
            messagebox.showerror("Error", e.message)
            raise
        except InsufficientFundsError as e:
            messagebox.showerror("Error", e.message)
            raise


    def spend_from_budget(self, category, amount, customer_id):
        """
        Spend an amount from a specific budget category.

        Args:
            category (str): The name of the budget category.
            amount (float): The amount to spend.

        Raises:
               TypeError: If the customer ID is not a string.
                InsufficientFundsError: if the amout to spend exceeds the current account balance.
                InvalidExpenseAmountError: If the amount to spend is invalid (less than 1).
                BudgetCategoryNotFoundError: If the budget category to spend from does.
                ExceedingBudgetLimitError: If the amount to spend exceeds the limit set.
        Returns:
            boolean: True if the spending is successful, False otherwise.
        """
        try:
            amount = float(amount)

            if not isinstance(customer_id, str):
                raise TypeError ("Customer ID must be a string.")

            if amount < 1:
                raise InvalidExpenseAmountError(f"Invalid expense amount {amount}. Please enter a positive value.")

            if amount > self.account_balance:
                raise InsufficientFundsError("Insufficient funds to proceed")

            if category not in self.budget_categories:
                raise BudgetCategoryNotFoundError(f"Dear {self.account_holder}, category: {category} not set!")

            if category not in self.cumulative_expenses:
                self.cumulative_expenses[category] = 0

            # Retrieve the budget limit for the category
            budget_limit = self.budget_categories[category]
            cumulative_expense = self.cumulative_expenses[category]
            total_expenses = amount + cumulative_expense

            if amount > budget_limit:
                raise ExceedingBudgetLimitError(f"Dear {self.account_holder}, you have exceeded your budget for {category}.")

            if budget_limit < total_expenses:
                raise ExceedingBudgetLimitError(f"Exceeding budget limit for {category}. Transaction cancelled.")

            self.account_balance -= amount
            cumulative_expense += amount
            budget_limit -= amount

            limit_after_spending = budget_limit - amount  # Update the limit

            messagebox.showinfo("Success", f"Expense of ${amount} from category {category} was successful. Your new balance is ${self.account_balance}. Remaining budget limit for {category}: ${limit_after_spending}.")

            self.transaction_history.append({"Type of transaction": "Expense", "Category": category, "Amount spent": amount})

            return True

        except ValueError as e:
            messagebox.showerror("Error", e)
            return False
        except TypeError:
            messagebox.showerror("Error", "something unexpected happended, Please try again later!")
            return False
        except InsufficientFundsError as e:
            messagebox.showerror("Error", e.message)
            raise
        except InvalidExpenseAmountError as e:
            messagebox.showerror("Error", e.message)
            raise
        except ExceedingBudgetLimitError as e:
            messagebox.showerror("Error", e.message)
            raise
        except Exception as e:
            messagebox.showerror("Error", e.message)
            return False


    def clear_data(self, customer_id):

        try:
            if not isinstance(customer_id, str):
                raise TypeError ("Customer ID must be a string.")

             # Open the file in write mode and write an empty YAML object
            with open("data_file.yaml", "w") as file:
                yaml.dump({}, file)

        except TypeError as e:
            messagebox.showerror("Error", e)
            raise
        except Exception as e:
            messagebox.showerror("Error", e)

    """
    The below 3 methods are here because there are test cases (in the test_Alpha.py) file that depend on these methods. wrote those tests earlier in development and getting rid of these methods would result to a re-structure of the tests which would somehow be time consuming
    """

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


    def budget_spending(self, category, amount):

        try:
            amount = float(amount)
        except ValueError as e:
            print(f"Error amount value has to be a float {e}")

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


    def get_expense(self, category, amount):

        try:
            amount = float(amount)
        except ValueError as e:
            print(f"Error invalid amount {e}")

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


class BankCustomer(BankAccount):

    """
    A class representing a bank customer.

    Attributes:
        customer_name (str): The name of the customer.
        accounts (list): List of associated bank accounts.

    Methods:
        addAccount(account: BankAccount) -> None:
            Add a bank account to the customer's profile.

    """

    def __init__(self, customer_name, account_number, account_holder, customer_id, default_balance):
        super().__init__(account_number, account_holder, customer_id)
        self.customer_name = customer_name
        self.default_balance = default_balance
        self.accounts = []


    def to_yaml(self):
        accounts_yaml = [yaml.dump(account, default_flow_style=False) for account in self.accounts]
        return yaml.dump({
            'customer_name': self.customer_name,
            'accounts': accounts_yaml,
            'account_number': self.account_number,
            'account_holder': self.account_holder,
            'customer_id': self.customer_id,
            'default_balance': self.default_balance,
        }, default_flow_style=False)


    @classmethod
    def from_yaml(cls, yaml_str):
        data = yaml.safe_load(yaml_str)
        accounts_data = data.get('accounts', [])
        accounts = []

        for account_data in accounts_data:
            accounts.append(BankAccount.from_yaml(account_data))

        customer = cls(data['customer_name'], data['account_number'], data['account_holder'], data['customer_id'], data['default_balance'])
        customer.accounts = accounts

        return data

    def _update_yaml_string(self):
        """
        Update the internal YAML string representation of the customer object.
        """
        account_yaml_strings = []
        for account in self.accounts:
            account_yaml_strings.append(yaml.dump(account, default_flow_style=False))

        self._yaml_string = yaml.dump({
            'customer_name': self.customer_name,
            'accounts': account_yaml_strings,
            'account_number': self.account_number,
            'account_holder': self.account_holder,
            'customer_id': self.customer_id,
            'default_balance': self.default_balance,
        }, default_flow_style=False)

    def addAccount(self, account):

        """
        Add a bank account to the customer's profile.

        Parameters:
            account (BankAccount): The bank account to be added.

        """
        self.accounts.append(account)

        # Update the customer object's YAML string representation
        self._update_yaml_string()

        print(f"Account added for {self.customer_name}. Thank you for choosing our bank.")

    def has_matching_information(self, account_data: dict):
        """
        Checks if the customer information matches the provided data.

        Parameters:
            account_data (dict): Dictionary containing customer information.

        Returns:
            boolean: True if information matches, False otherwise.
        """

        # Check for a matching customer ID first
        try:
            if self.customer_id == account_data["customer_id"]:
                return True
        except KeyError as e:
            print(f"Error: {e}")

        # If no ID match, compare other relevant information
        for key, value in account_data.items():
            try:
                if hasattr(self, key) and getattr(self, key) == value:
                    return True
            except KeyError as e:
                print(f"Error: {e}")
        return False



    def total_balance(self):
        total = sum(account.account_balance for account in self.accounts)
        print(f"The total amount in {self.customer_name} accounts is: {total}")
        return total

    def get_all_accounts(self):
        return self.accounts

    def __str__(self):
        return str(self.accounts)

import unittest

if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*.py')
    unittest.TextTestRunner().run(test_suite)





