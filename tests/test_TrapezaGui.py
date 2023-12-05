import unittest
import os
from Alpha import BankAccount
from Trapeza_gui import BankInterface
from json_utils import save_bank_account_data, load_bank_account_data


class TestBankAccountMethods(unittest.TestCase):

    def setUp(self):
        self.customer1 = BankAccount(account_number="1000102", account_holder="Chachu Mulumba", customer_id="2567",  default_balance=1500)

    def test_save_account_data(self):
        # Save account data to JSON file
        self.customer1.deposit(1000)
        BankInterface.save_account_data(self.customer1, "account_data.json")

        # Check if JSON file exists
        self.assertTrue(os.path.exists("account_data.json"))

        # Load account data from JSON file
        loaded_account_data = load_bank_account_data("account_data.json")

        # Check if loaded account data is the same as saved account data
        #self.assertEqual(loaded_account_data, self.customer1)