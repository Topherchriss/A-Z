import unittest
from Alpha import BankAccount
from unittest import mock

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

    def test_send_notification(self):
        with mock.patch('builtins.print') as mock_print:
            self.account.deposit(60000)
            self.account.send_notification()

        # Assert that the expected message is in the captured print calls
        expected_message = "Notification: A large deposit was made to your account."
        self.assertIn(mock.call(expected_message), mock_print.call_args_list)
