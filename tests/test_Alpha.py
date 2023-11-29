import unittest
from unittest.mock import patch
from Alpha import BankAccount


class TestTrapeza(unittest.TestCase):


    def setUp(self):
        # Call this method before each test
        self.account = BankAccount(account_number="1000101", account_holder="Jean Maswa", customer_id="1456", default_balance=10000)


    def test_default_balance(self):
        self.assertEqual(self.account.account_balance, 10000, "Default balance should be $1000")


    def test_deposit(self):
        self.account.deposit(5000)
        self.assertEqual(self.account.account_balance, 15000, "Deposit of $5000 should result in a balance of $6000")


    def test_invalid_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-300)


    def test_withdrawal(self):
        self.account.withdraw(5000)
        self.assertEqual(self.account.account_balance, 5000, "Withdrawal of $5000 should result in a balance of $500")


    def test_less_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(20000)


    def test_invalid_withdrawal(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(-390)


    def test_trans_history(self):
        self.account.deposit(5000)
        self.account.withdraw(1000)
        self.account.withdraw(500)
        self.account.deposit(1500)
        trans = self.account.get_transaction_history()
        self.assertEqual(len(trans), 4, "Transaction history should have four entities")

    """
    testing notifications proved to be tricky challenge so i decided to use this approach and separate the tests in a diffrent class to enhance the ability to test the send_notification method in diffrent scenarios.

    """

class TestSendNotification(unittest.TestCase):

    def setUp(self):
        # Call this method before each test
        self.account = BankAccount(account_number="1000101", account_holder="Jean Maswa", customer_id="1456", default_balance=10000)

    @patch('builtins.print')
    def test_large_deposit_notification(self, mock_print):
        # Arrange
        self.account.deposit(60000)

        # Act
        self.account.send_notification()

        # Assert
        expected_message = "Notification: A large deposit was made to your account."
        mock_print.assert_called_with(expected_message)

    @patch('builtins.print')
    def test_large_withdrawal_notification(self, mock_print):
        # Arrange
        self.account.withdraw(7000)

        # Act
        self.account.send_notification()

        # Assert
        expected_message = "Notification: A large withdrawal was made from your account."
        mock_print.assert_called_with(expected_message)

    @patch('builtins.print')
    def test_no_notification(self, mock_print):
        # Arrange - No significant events
        self.account.deposit(2000)

        # Act
        self.account.send_notification()

        # Assert
        expected_message = "Dear customer your deposit of 2000 was succesful. Your new balance is: 12000"

        mock_print.assert_called_with(expected_message)


