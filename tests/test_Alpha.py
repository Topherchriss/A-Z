import unittest
#from Alpha import BankAccount

class TestTrapeza(unittest.TestCase):

    def setUp(self):
        # Call this method before each test
        self.account = BankAccount(account_number="1000101", account_holder="Jean Maswa", customer_id="1456", default_balance=1000)


    def test_default_balance(self):
        self.assertEqual(self.account.account_balance, 1000, "Default balance should be $1000")


    def test_deposit(self):
        self.account.deposit(5000)
        self.assertEqual(self.account.account_balance, 6000, "Deposit of $5000 should result in a balance of $6000")


    def test_invalid_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(-300)


    def test_withdrawal(self):
        self.account.withdraw(500)
        self.assertEqual(self.account.account_balance, 500, "Withdrawal of $500 should result in a balance of $500")


    def test_less_funds(self):
        with self.assertRaises(ValueError):
            self.account.withdraw(2000)


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
