
import unittest
import json
import os
from json_utils import save_bank_account_data, load_bank_account_data
from Alpha import BankAccount

class TestJSONFile(unittest.TestCase):

    def test_save_bank_account_data(self):
        bank_account = BankAccount(account_number="1000102", account_holder="Chachu Mulumba", customer_id="2567",  default_balance=1500)
        save_bank_account_data(bank_account, 'account_data.json')

        with open('account_data.json', 'r') as file:
            data = json.load(file)

        self.assertEqual(data['account_holder'], 'Chachu Mulumba')
        self.assertEqual(data['account_balance'], 1500)

    """
    def test_load_bank_account_data(self):
        with open('account_data.json', 'w') as file:
            json.dump({'account_holder': 'Chachu Mulumba', 'account_balance': 1500}, file, indent=2)

        bank_account = load_bank_account_data('account_data.json')

        #self.assertEqual(bank_account.customer_id, '2567')
        #self.assertEqual(bank_account.account_balance, 1500)
        """

    def test_load_bank_account_data_invalid_json(self):
        with open('account_data.json', 'w') as file:
            file.write('This is not a valid JSON')

        bank_account = load_bank_account_data('account_data.json')

        self.assertIsNotNone(bank_account)

    def test_load_bank_account_data_file_not_found(self):
        bank_account = load_bank_account_data('does_not_exist.json')

        self.assertIsNotNone(bank_account)



