import unittest
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



from unittest.mock import patch

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

    @patch('builtins.print')
    def test_below_threshold_notification(self, mock_print):
        #Arrange
        self.account.set_threshold(9000)
        self.account.withdraw(1500)

        #Act
        self.account.send_notification()

        #Assert
        expected_message = f"Notification: Your account balance is below $9000."

        mock_print.assert_called_with(expected_message)


class TestBudgetCategory(unittest.TestCase):

    def setUp(self):
        # Call this method before each test
        self.account = BankAccount(account_number="1000101", account_holder="Jean Maswa", customer_id="1456", default_balance=10000)

    @patch('builtins.print')
    def test_no_set_category(self, mock_print):
        #Arrange
        self.account.set_budget(category="Shoping", limit=700)

        #Act
        self.account.budget_spending(category="School", amount=300)

        #Assert
        expected_message = f"Dear Jean Maswa category: School not set!"

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_budget_exceed(self, mock_print):
        #Arrange
        self.account.set_budget(category="Enta", limit=100)

        #Act
        self.account.budget_spending(category="Enta", amount=5000)

        #Assert
        self.account.send_notification()
        expected_message = f"Expense of 5000 from Enta was successful. Your new balance is 5000"

        mock_print.assert_called_with(expected_message)


    @patch("builtins.print")
    def test_normal_budget_spending(self, mock_print):

        self.account.set_budget(category="sports", limit=2000)

        self.account.budget_spending(category="sports", amount=1000)

        expected_message = f"Expense of 1000 from sports was successful. Your new balance is 9000"

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_invalid_amount(self, mock_print):
        self.account.set_budget(category="vip", limit=4000)

        self.account.budget_spending(category="vip", amount=-3000)

        expected_message = "Invalid expense amount -3000. Please insert a positive value"

        mock_print.assert_called_with(expected_message)



    @patch('builtins.print')
    def test_excess_than_limit(self, mock_print):
        self.account.set_budget(category="BILLS", limit=300)

        self.account.get_expense(category="BILLS", amount=700)

        expected_message = "Exceeding budget limit"

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_normal_expense(self, mock_print):

        self.account.set_budget(category="BILLS", limit=1000)

        self.account.get_expense(category="BILLS", amount=500)

        self.account.send_notification()
        expected_message = "You have succesfully spent 500 form category BILLS remainig $500"

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_expense_but_no_category(self, mock_print):

        self.account.set_budget(category="A", limit=300)

        self.account.get_expense(category="a", amount=200)

        expected_message = "Category 'a' not found in budget."

        mock_print.assert_called_with(expected_message)


    @patch('builtins.print')
    def test_limit_after_spending(self, mock_print):

        self.account.set_budget(category="A", limit=500)

        self.account.get_expense(category='A', amount=300)

        expected_message = "You have succesfully spent 300 form category A remainig $200"

        mock_print.assert_called_with(expected_message)

    @patch('builtins.print')
    def test_set_threshold(self, mock_print):

        self.account.set_threshold(288)

        expected_message = "Dear Jean Maswa a threshold of $288 was succesfully added for account 1000101"

        mock_print.assert_called_with(expected_message)

    @patch('builtins.print')
    def test_set_threshold(self, mock_print):

        self.account.set_threshold(-600)

        expected_message = "Invalid threshold value provided"

        mock_print.assert_called_with(expected_message)

    @patch('builtins.print')
    def test_set_threshold_above_balance(self, mock_print):

        self.account.set_threshold(15000)

        expected_message = "Threshold amount cannot exceded current account balance"

        mock_print.assert_called_with(expected_message)

