from tkinter import messagebox
from Gui_Trapeza import DataOps
from exceptions import InsufficientFundsError, InvalidDepositAmountError, InvalidCustomerIDError, InvalidAccountNumberError, InvalidBudgetLimitError, BudgetCategoryNotFoundError, BudgetCategoryAlreadyExistsError, InvalidThresholdAmountError, AccountCreationError, InvalidWithrawalAmountError, WrongCustomerIdError


class AccountTransactions:
    """
    Responsible for encapsulating the logic for account transactions.

    Attributes:
        data_ops (DataOps): Object providing data access operations.
        interface (InterfaceBank): Object responsible for interface updates.
        account_balance (float): The current account balance.
        transaction_history (list): List to store transaction history.

    Methods:
        withdraw(amount, customer_id): Allows a withdrawal from the current account.
        deposit(amount, customer_id): Allows a deposit to the current account.
        check_balance(customer_id, account_number): Verifies the account number and customer ID before retrieving and displaying the current account balance.
        transactions(customer_id, account_number): Retrieves and displays the transaction history for the specified customer account.
    """

    def __init__(self, account_number, account_holder, customer_id, default_balance, data_ops: DataOps):
        self.account_number = account_number
        self.customer_id = customer_id
        self.account_balance = default_balance
        self.transaction_history = []
        self.data_ops = data_ops


    def withdraw(self, amount, customer_id):
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


            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Invalid customer ID.")

            self.account_balance -= amount
            self.transaction_history.append({"Type of transaction": "withdrawal", "Amount withdrawn": amount})
            messagebox.showinfo("Success", f"Withdrawal of ${amount} was successful. Your new account balance is {self.account_balance}")
            return True

        except ValueError:
            messagebox.showerror("Error", "Invalid withdrawal amount. Please enter a valid number.")
            return False
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            return False
        except InsufficientFundsError as e:
            messagebox.showerror("Error", e.message)
            print("Insufficient funds to proceed with withdrawal")
            return False
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            return False
        except InvalidWithrawalAmountError as e:
            messagebox.showerror("Error", e.message)
            return False


    def deposit(self, amount, customer_id):
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


            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Invalid customer ID.")

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
            return False
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            return False


    def check_balance(self, customer_id, account_number):
        """
        Verifies the account number and customer ID before retrieving and displaying the current account balance.

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

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Error. You entered a wrong PIN")

            if account_number != self.data_ops.selected_customer.account_number:
                raise InvalidAccountNumberError("Error. You entered an invalid account number")

            # Retrieve and display balance
            current_balance = self.data_ops.selected_customer.account_balance
            messagebox.showinfo("Account Balance", f"Your current account balance is ${current_balance}.")
            return True

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please try again.")
            return False
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            return False
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            return False
        except InvalidAccountNumberError as e:
            messagebox.showerror("Error", e.message)
            return False


    def transactions(self, customer_id, account_number):
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

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Error. You entered a wrong PIN")

            if account_number != self.data_ops.selected_customer.account_number:
                raise InvalidAccountNumberError("Error. You entered an invalid account number")

            transactions =  self.data_ops.selected_customer.account_transactions(customer_id, account_number)
            if transactions:
                formatted_transactions = "\n".join(str(transaction) for transaction in transactions)
                messagebox.showinfo("Transactions", f"{self.data_ops.selected_customer.account_holder}'s transaction history:\n{formatted_transactions}")
                return formatted_transactions
            else:
                # Handle the case where there are no transactions
                messagebox.showinfo("Transactions", f"{self.data_ops.selected_customer.account_holder}'s transaction history is empty.")
                return ""

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input for transaction history: {e}")
        except TypeError as e:
            messagebox.showerror("Error", str(e))
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
        except InvalidAccountNumberError as e:
            messagebox.showerror("Error", e.message)
        except Exception as e:
            messagebox.showerror("Error", str(e))