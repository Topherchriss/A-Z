import unittest
from Alpha import BankAccount, BankCustomer
import Gui_Trapeza
from exceptions import InsufficientFundsError, InvalidDepositAmountError, InvalidCustomerIDError, InvalidAccountNumberError, InvalidBudgetLimitError, BudgetCategoryNotFoundError, BudgetCategoryAlreadyExistsError, InvalidThresholdAmountError, AccountCreationError, InvalidWithrawalAmountError, WrongCustomerIdError


class TestTrapeza(unittest.TestCase):

    """
    Test cases for the BankAccount class in the Alpha module.


    Methods:
        setUp(self) -> None:
            Set up a BankAccount instance for testing.

        test_default_balance(self) -> None:
            Test the default balance of a BankAccount.

        test_deposit(self) -> None:
            Test the deposit method of a BankAccount.

        test_invalid_deposit(self) -> None:
            Test handling invalid deposit amounts in a BankAccount.

        test_withdrawal(self) -> None:
            Test the withdrawal method of a BankAccount.

        test_less_funds(self) -> None:
            Test handling withdrawal with insufficient funds in a BankAccount.

        test_invalid_withdrawal(self) -> None:
            Test handling invalid withdrawal amounts in a BankAccount.

        test_trans_history(self) -> None:
            Test the transaction history of a BankAccount.
"""

    def setUp(self):
        # Set up a BankAccount instance for testing
        self.account = BankAccount(account_number="1000101", account_holder="Jean Maswa", customer_id="1456", default_balance=10000)

    def test_default_balance(self):
        self.assertEqual(self.account.account_balance, 10000, "Default balance should be $1000.0")


    def test_deposit(self):
        self.account.deposit_money(5000, customer_id="1456")
        self.assertEqual(self.account.account_balance, 15000, "Deposit of $5000 should result in a balance of $6000.0")


    def test_invalid_deposit(self):
        with self.assertRaises(InvalidDepositAmountError) as context:
            self.account.deposit_money(-300, customer_id="1456")
        self.assertEqual(str(context.exception), "Invalid deposit amount. Please enter a valid number.")

    def test_withdrawal(self):
        self.account.withdraw_money(5000, customer_id="1456")
        self.assertEqual(self.account.account_balance, 5000, "Withdrawal of $5000 should result in a balance of $500.0")


    def test_less_funds(self):
        with self.assertRaises(InsufficientFundsError) as context:
            self.account.withdraw_money(200000, customer_id="1456")
        self.assertEqual(str(context.exception), "Insufficient funds to proceed with withdrawal.")


    def test_invalid_withdrawal(self):
        with self.assertRaises(InvalidWithrawalAmountError) as context:
            self.account.withdraw_money(-390, customer_id="1456")
        self.assertEqual(str(context.exception), "Invalid withdrawal amount. Please enter a valid number.")


    def test_trans_history(self):
        self.account.deposit_money(5000, customer_id="1456")
        self.account.withdraw_money(1000, customer_id="1456")
        self.account.withdraw_money(500, customer_id="1456")
        self.account.deposit_money(1500, customer_id="1456")
        trans = self.account.account_transactions(customer_id="1456", account_number="1000101")
        self.assertIsNotNone(trans)
        self.assertEqual(len(trans), 4, "Transaction history should have four entities")


from unittest.mock import patch
class TestSendNotification(unittest.TestCase):

    """
    Test cases for the send_notification method in the BankAccount class.

    Methods:
        setUp(self) -> None:
            Set up a BankAccount instance for testing notifications.

        test_large_deposit_notification(self, mock_print) -> None:
            Test sending a notification for a large deposit.

        test_large_withdrawal_notification(self, mock_print) -> None:
            Test sending a notification for a large withdrawal.

        test_no_notification(self, mock_print) -> None:
            Test sending no notification for a regular transaction.

        test_below_threshold_notification(self, mock_print) -> None:
            Test sending a notification for an account below a threshold.

    """

    def setUp(self):
        # Set up a BankAccount instance for testing
        self.account = BankAccount(account_number="1000101", account_holder="Jean Maswa", customer_id="1456", default_balance=10000)

    @patch('builtins.print')
    def test_large_deposit_notification(self, mock_print):
        # Arrange
        self.account.deposit_money(60000, customer_id="1456")

        # Act
        self.account.send_notification()

        # Assert
        expected_message = "Notification: A large deposit was made to your account."
        mock_print.assert_called_with(expected_message)

    @patch('builtins.print')
    def test_large_withdrawal_notification(self, mock_print):
        # Arrange
        self.account.withdraw_money(7000, customer_id="1456")

        # Act
        self.account.send_notification()

        # Assert
        expected_message = "Notification: A large withdrawal was made from your account."
        mock_print.assert_called_with(expected_message)

    @patch('builtins.print')
    def test_no_notification(self, mock_print):
        # Arrange - No significant events
        self.account.deposit_money(2000, customer_id="1456")

        # Act
        result = self.account.send_notification()

        # Assert
        self.assertFalse(result) #Notificaion method should not be called

    @patch('builtins.print')
    def test_below_threshold_notification(self, mock_print):
        #Arrange
        self.account.set_account_threshold(9000, customer_id="1456")
        self.account.withdraw_money(1500, customer_id="1456")

        #Act
        self.account.send_notification()

        #Assert
        expected_message = f"Notification: Your account balance is below $9000.0."

        mock_print.assert_called_with(expected_message)


class TestBudgetCategory(unittest.TestCase):

    """
    Test cases for budget-related methods in the BankAccount class.

    Methods:
        setUp(self) -> None:
            Set up a BankAccount instance for testing budgets.

        test_no_set_category(self, mock_print) -> None:
            Test handling budget spending for an unset category.

        test_budget_exceed(self, mock_print) -> None:
            Test handling budget exceedance.

        test_normal_budget_spending(self, mock_print) -> None:
            Test normal budget spending.

        test_invalid_amount(self, mock_print) -> None:
            Test handling invalid budget spending amounts.

        test_excess_than_limit(self, mock_print) -> None:
            Test exceeding the budget limit.

        test_normal_expense(self, mock_print) -> None:
            Test normal expense within budget.

        test_expense_but_no_category(self, mock_print) -> None:
            Test handling expense with an undefined category.

        test_limit_after_spending(self, mock_print) -> None:
            Test remaining budget limit after spending.

        test_set_threshold(self, mock_print) -> None:
            Test setting a threshold for the account balance.

        test_set_threshold_invalid_amount(self, mock_print) -> None:
            Test handling invalid threshold amounts.

        test_set_threshold_above_balance(self, mock_print) -> None:
            Test setting a threshold above the account balance.
    """

    def setUp(self):
        # Set up a BankAccount instance for testing
        self.account = BankAccount(account_number="1000101", account_holder="Jean Maswa", customer_id="1456", default_balance=10000)

    @patch('builtins.print')
    def test_no_set_category(self, mock_print):
        #Arrange
        self.account.set_budget_category(category="Shoping", limit=700, customer_id="1456")

        #Act
        self.account.budget_spending(category="School", amount=300)

        #Assert
        expected_message = f"Dear Jean Maswa category: School not set!"

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_budget_exceed(self, mock_print):
        #Arrange
        self.account.set_budget_category(category="Enta", limit=100, customer_id="1456")

        #Act
        self.account.budget_spending(category="Enta", amount=5000)

        #Assert
        self.account.send_notification()
        expected_message = f"Expense of 5000.0 from Enta was successful. Your new balance is 5000.0"

        mock_print.assert_called_with(expected_message)


    @patch("builtins.print")
    def test_normal_budget_spending(self, mock_print):

        self.account.set_budget_category(category="sports", limit=2000, customer_id="1456")

        self.account.budget_spending(category="sports", amount=1000)

        expected_message = f"Expense of 1000.0 from sports was successful. Your new balance is 9000.0"

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_invalid_amount(self, mock_print):
        self.account.set_budget_category(category="vip", limit=4000, customer_id="1456")

        self.account.budget_spending(category="vip", amount=-3000)

        expected_message = "Invalid expense amount -3000.0. Please insert a positive value"

        mock_print.assert_called_with(expected_message)



    @patch('builtins.print')
    def test_excess_than_limit(self, mock_print):
        self.account.set_budget_category(category="BILLS", limit=300, customer_id="1456")

        self.account.get_expense(category="BILLS", amount=700)

        expected_message = "Exceeding budget limit"

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_normal_expense(self, mock_print):

        self.account.set_budget_category(category="BILLS", limit=1000, customer_id="1456")

        self.account.get_expense(category="BILLS", amount=500)

        self.account.send_notification()
        expected_message = "You have succesfully spent 500.0 form category BILLS remainig $500.0"

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_expense_but_no_category(self, mock_print):

        self.account.set_budget_category(category="A", limit=300, customer_id="1456")

        self.account.get_expense(category="a", amount=200)

        expected_message = "Category 'a' not found in budget."

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_limit_after_spending(self, mock_print):

        self.account.set_budget_category(category="A", limit=500, customer_id="1456")

        self.account.get_expense(category='A', amount=300)

        expected_message = "You have succesfully spent 300.0 form category A remainig $200.0"

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_set_threshold(self, mock_print):
        with patch("Gui_Trapeza.messagebox.showinfo") as mock_showinfo:

            self.account.set_account_threshold(288, customer_id="1456")

            mock_showinfo.assert_called_once_with('Success', 'Dear Jean Maswa a threshold of $288.0 was succesfully added for account number 1000101')

    @patch('builtins.print')
    def test_set_threshold_invalid_amount(self, mock_print):

        with self.assertRaises(InvalidThresholdAmountError) as context:
            self.account.set_account_threshold(-600, customer_id="1456")

        self.assertEqual(str(context.exception), "Threshold must be more than a $1")


    @patch('builtins.print')
    def test_set_threshold_above_balance(self, mock_print):

        with self.assertRaises(InsufficientFundsError) as context:
            self.account.set_account_threshold(15000, customer_id="1456")

        self.assertEqual(str(context.exception), "Threshold cannot be more than current account balance.")


class TestBankCustomer(unittest.TestCase):

    def setUp(self):
        # Set up a BankCustomer instance for testing
        self.customer = BankCustomer(customer_name="John Doe", account_number="1000101", account_holder="John Doe", customer_id="1456", default_balance=10000)

    def test_add_account(self):
        # Arrange
        account = BankAccount(account_number="2000202", account_holder="John Doe", customer_id="1456", default_balance=5000)

        # Act
        self.customer.addAccount(account)

        # Assert
        self.assertIn(account, self.customer.get_all_accounts(), "Account should be added to the customer's profile")

    def test_total_balance(self):
        # Arrange
        account1 = BankAccount(account_number="2000202", account_holder="John Doe", customer_id="1456", default_balance=5000)
        account2 = BankAccount(account_number="3000303", account_holder="John Doe", customer_id="1456", default_balance=7000)
        self.customer.addAccount(account1)
        self.customer.addAccount(account2)

        # Act
        total = self.customer.total_balance()

        # Assert
        expected_total = account1.account_balance + account2.account_balance
        self.assertEqual(total, expected_total, "Total balance should match the sum of individual account balances")

    def test_has_matching_information(self):
        # Arrange
        account_data = {"customer_id": "1456", "customer_name": "John Doe"}

        # Act & Assert
        self.assertTrue(self.customer.has_matching_information(account_data), "Customer information should match")

    def test_does_not_have_matching_information(self):
        # Arrange
        account_data = {"customer_id": "9999", "customer_name": "Unknown"}

        # Act & Assert
        self.assertFalse(self.customer.has_matching_information(account_data), "Customer information should not match")

