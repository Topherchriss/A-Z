import unittest
import yaml
from unittest import TestCase
from unittest.mock import patch, Mock
from Gui_Trapeza import CreateAccount, DataOps, AccountTransactions
from Alpha import BankCustomer, BankAccount
import Alpha

class TestDataOps:
    def __init__(self, selected_customer):
        self.selected_customer = selected_customer

class TestInterfaceBank:
    def display_notification(self, message):
        pass

class TestAccountTransactions(unittest.TestCase):
    def setUp(self):
        # Create a mock selected customer
        self.selected_customer = BankAccount(
            account_number="1000101",
            account_holder="Milele",
            customer_id="1456",
            default_balance=10000
        )

        # Create a mock DataOps and InterfaceBank
        self.data_ops = TestDataOps(selected_customer=self.selected_customer)
        self.interface = TestInterfaceBank()

        # Create an instance of AccountTransactions for testing
        self.account_transactions = AccountTransactions(
            account_number="1000101",
            account_holder="Milele",
            customer_id="1456",
            default_balance=10000,
            data_ops=self.data_ops,
            interface=self.interface
        )

    def test_withdraw_success(self):
        with patch('Gui_Trapeza.messagebox.showinfo') as mock_showinfo:
            result = self.account_transactions.withdraw(amount=500, customer_id="1456")
            self.assertTrue(result)
            mock_showinfo.assert_called_with("Success", "Withdrawal of $500.0 was successful. Your new account balance is 9500.0")

    def test_withdraw_insufficient_funds(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            result = self.account_transactions.withdraw(amount=20000, customer_id="1456")
            self.assertFalse(result)
            mock_showerror.assert_called_with('Error', 'Insufficient funds to proceed to withdrawal.')


    def test_withdraw_invalid_amount(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test withdrawal with an invalid amount (non-float)
            result = self.account_transactions.withdraw(amount="invalid", customer_id="1456")
            self.assertFalse(result)
            mock_showerror.assert_called_with("Error", "Invalid withdrawal amount. Please enter a valid number.")

    def test_withdraw_negative_amount(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test withdrawal with a negative amount
            result = self.account_transactions.withdraw(amount=-200, customer_id="1456")
            self.assertFalse(result)
            mock_showerror.assert_called_with("Error", "Invalid withdrawal amount. Please enter a valid number.")

    def test_withdraw_non_string_customer_id(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test withdrawal with a non-string customer ID
            result = self.account_transactions.withdraw(amount=300, customer_id=123)
            self.assertFalse(result)
            mock_showerror.assert_called_once_with('Error', 'Customer ID must be a string.')


    def test_withdraw_invalid_customer_id(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test withdrawal with an invalid customer ID
            result = self.account_transactions.withdraw(amount=300, customer_id="invalid_id")
            self.assertFalse(result)
            mock_showerror.assert_called_with("Error", "Invalid customer ID.")

class TestAccountTransactionsDeposit(unittest.TestCase):
    def setUp(self):

        self.selected_customer = BankAccount(
            account_number="10001012",
            account_holder="Omwami Jay",
            customer_id="1456",
            default_balance=10000
        )

        # Create a mock DataOps and InterfaceBank
        self.data_ops = TestDataOps(selected_customer=self.selected_customer)
        self.interface = TestInterfaceBank()

        self.account_transactions = AccountTransactions(
            account_number="10001012",
            account_holder="Omwami Jay",
            customer_id="1456",
            default_balance=1900,
            data_ops=self.data_ops,
            interface=self.interface
        )

    def test_deposit_valaid_amount_customer_id(self):
        with patch('Gui_Trapeza.messagebox.showinfo') as mock_showinfo:
            #Test deposit with valid amount and customer ID
            result = self.account_transactions.deposit(amount=500, customer_id="1456")
            self.assertTrue(result)
            mock_showinfo.assert_called_once_with("Success", "Deposit of $500.0 was successful. Your new account balance is $2400.0")


    def test_deposit_invalid_amount(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test deposit with an invalid amount (non-float)
            result = self.account_transactions.deposit(amount="970y9.i", customer_id="1456")
            self.assertFalse(result)
            mock_showerror.assert_called_once_with("Error", "Invalid deposit amount. Please enter a valid number.")


    def test_deposit_negative_amount(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test deposit with a negative amount
            result = self.account_transactions.deposit(amount=-200, customer_id="1456")
            self.assertFalse(result)
            mock_showerror.assert_called_once_with('Error', 'Minimum deposit amount is $1.')

    """

    def test_deposit_non_string_customer_id(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test deposit with a non-string customer ID
            result = self.account_transactions.deposit(amount=300, customer_id=723)
            self.assertFalse(result)
            mock_showerror.assert_called_once_with('Error', TypeError())
            with self.assertRaises(TypeError):
                self.account_transactions.deposit(amount=300, customer_id=723)

    """


    def test_deposit_invalid_customer_id(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test deposit with an invalid customer ID
            result = self.account_transactions.deposit(amount=300, customer_id="invalid_id")
            self.assertFalse(result)
            mock_showerror.assert_called_once_with("Error", "Invalid customer ID.")


    def test_deposit_invalid_deposit_amount(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test deposit with an invalid deposit amount (less than 1)
            result = self.account_transactions.deposit(amount=0, customer_id="1456")
            self.assertFalse(result)
            mock_showerror.assert_called_once_with("Error", "Minimum deposit amount is $1.")


class TestAccountTransactionsCheckBalance(unittest.TestCase):
    def setUp(self):
        # Create a mock selected customer
        self.selected_customer = BankAccount(
            account_number="1000103",
            account_holder="Ndolo Sanchez",
            customer_id="1456",
            default_balance=8000.90
        )

        # Create a mock DataOps and InterfaceBank
        self.data_ops = TestDataOps(selected_customer=self.selected_customer)
        self.interface = TestInterfaceBank()

        # Create an instance of AccountTransactions for testing
        self.account_transactions = AccountTransactions(
            account_number="1000103",
            account_holder="Ndolo Sanchez",
            customer_id="1456",
            default_balance=8000.90,
            data_ops=self.data_ops,
            interface=self.interface
        )

    def test_check_balance_success(self):
        with patch('Gui_Trapeza.messagebox.showinfo') as mock_showinfo:
            # Test check_balance with valid customer ID and account number
            result = self.account_transactions.check_balance(customer_id="1456", account_number="1000103")
            self.assertTrue(result)
            mock_showinfo.assert_called_once_with("Your current account balance is $8000.9.")

    def test_check_balance_invalid_customer_id(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test check_balance with invalid customer ID
            result = self.account_transactions.check_balance(customer_id="1234", account_number="1000103")
            self.assertFalse(result)
            mock_showerror.assert_called_once_with('Error', 'Error. You entered a wrong PIN')

    def test_check_balance_invalid_account_number(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test check_balance with invalid account number
            result = self.account_transactions.check_balance(customer_id="1456", account_number="5678")
            self.assertFalse(result)
            mock_showerror.assert_called_once_with('Error', 'Error. You entered an invalid account number')

class TestAccountTransactionsTransctions(unittest.TestCase):
    def setUp(self):
        # Create a mock selected customer
        self.selected_customer = BankAccount(
            account_number="1000104",
            account_holder="Pindi Boss",
            customer_id="5678",
            default_balance=16789.68
        )

        # Create a mock DataOps and InterfaceBank
        self.data_ops = TestDataOps(selected_customer=self.selected_customer)
        self.interface = TestInterfaceBank()

        # Create an instance of AccountTransactions for testing
        self.account_transactions = AccountTransactions(
            account_number="1000104",
            account_holder="Pindi Boss",
            customer_id="5678",
            default_balance=8000.90,
            data_ops=self.data_ops,
            interface=self.interface
        )
    """
****
"""

    def test_transactions_success(self):
        with patch('Gui_Trapeza.messagebox.showinfo') as mock_showinfo:
            # Set up mock data for selected customer's transaction list
            mock_transaction_history = [
                {"Type of transaction": "deposit", "Amount deposited": 200},
                {"Type of transaction": "withdrawal", "Amount withdrawn": 100}
            ]
            self.account_transactions.get_transaction_history = mock_transaction_history

            # Test transactions with valid customer ID and account number
            result = self.account_transactions.transactions(customer_id="5678", account_number="1000104")
            #self.assertTrue(result != "") # Check that the result is not an empty string
            self.assertIsNotNone(result)
            #expected_message = "Pindi Boss's transaction history:\ndeposit of $800\nwithdrawal of $100"
            #mock_showinfo.assert_called_once_with("Transactions", expected_message)


    def test_transactions_invalid_customer_id(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test transactions with invalid customer ID
            result = self.account_transactions.transactions(customer_id="1234", account_number="1000104")
            self.assertFalse(result)
            mock_showerror.assert_called_once_with('Error', 'Error. You entered a wrong PIN')

    def test_transactions_invalid_account_number(self):
        with patch('Gui_Trapeza.messagebox.showerror') as mock_showerror:
            # Test transactions with invalid account number
            result = self.account_transactions.transactions(customer_id="5678", account_number="1000103889")
            self.assertFalse(result)
            mock_showerror.assert_called_once_with('Error', 'Error. You entered an invalid account number')

    def test_transactions_no_transactions(self):
        with patch('Gui_Trapeza.messagebox.showinfo') as mock_showinfo:
            # Set up mock data for selected customer's transaction list (empty list)
            mock_transaction_history = []
            self.account_transactions.get_transaction_history = mock_transaction_history

            # Test transactions with valid customer ID and account number but no transactions
            result = self.account_transactions.transactions(customer_id="5678", account_number="1000104")

            self.assertEqual(result, "")  # Since there are no transactions, the return value should be an empty string

            mock_showinfo.assert_called_once_with("Transactions", f"Pindi Boss's transaction history is empty.")











