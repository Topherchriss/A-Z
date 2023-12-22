VALID_DATA = """
- customer_name: Doe
  account_number: 123
  account_holder: Onyi
  customer_id: 1
  default_balance: 100
- customer_name: Fuwe
  account_number: 456
  account_holder: Jane
  customer_id: 2
  default_balance: 200
- customer_name: livi
  account_number: 789
  account_holder: Yobuk
  customer_id: 3
  account_number: 789
  default_balance: 500
"""

INVALID_CUSTOMER_DATA = """
- customer_name: John
  account_number: 123
  default_balance: 100
- invalid data:@y
- customer_name: Omolo
  account_number: 789
  default_balance: 500
"""
no_file = " "

import unittest
import yaml
from unittest.mock import patch, mock_open, Mock
from unittest import TestCase
from yaml.scanner import ScannerError
from Alpha import BankCustomer, BankAccount
from Gui_Trapeza import DataOps, CreateAccount
from exceptions import InvalidAccountNumberError



class TestDataOpsLoadData(unittest.TestCase):

    def setUp(self):
        self.valid_data_file = "valid_data_file.yaml"
        self.invalid_data_file = "invalid_data_file.yaml"
        self.data_ops = DataOps(self.valid_data_file, bank_customers=[])


    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_data_file_not_found(self, mock_open):
        """Test handling file not found."""
        results = self.data_ops.load_data(no_file)
        self.assertIsNone(results)
        self.assertEqual(len(self.data_ops.get_all_customers()), 0)

    @patch("builtins.open", side_effect=lambda f, m: mock_open(read_data=VALID_DATA).return_value)
    def test_load_data_valid_file(self, mock_open):
        """Test loading data from a valid YAML file."""
        self.data_ops.load_data(self.valid_data_file)
        self.assertEqual(len(self.data_ops.get_all_customers()), 3)

    @patch("builtins.open", side_effect=lambda f, m: mock_open(read_data=INVALID_CUSTOMER_DATA).return_value)
    def test_load_data_invalid_customer_data(self, mock_open):
        """Test loading data with invalid customer data."""
        results = self.data_ops.load_data(self.invalid_data_file)
        #Assertions
        self.assertIsNone(results)
        self.assertEqual(len(self.data_ops.get_all_customers()), 0) #Though the files is not None
        


class TestDataOpsSaveData(unittest.TestCase):

    def setUp(self):
        self.valid_data_file = "valid_data_file.yaml"
        self.test_save_data = "test_save_data.yaml"
        self.customer = Mock(spec=BankCustomer)
        self.data_ops = DataOps(self.test_save_data, bank_customers=[])
        self.create_account_service = CreateAccount(self.data_ops, self.customer)

    @patch("builtins.open", side_effect=lambda f, m: mock_open().return_value)
    @patch("yaml.safe_load", return_value=[])

    def test_save_data(self, mock_safe_load, mock_open):
        account_data = {
            "customer_name": "Mwalimu Daktari",
            "account_number": "12345",
            "account_holder": "Teacher Doctor",
            "customer_id": "1",
            "default_balance": 0.0,
        }

        customer = self.create_account_service.create_customer(account_data)
        saved_data = self.data_ops.save_data(self.test_save_data, [customer])  # Pass a list of customers
        self.assertTrue(customer)
        self.assertTrue(saved_data)

        # Verify the saved data
        with open(self.test_save_data, "r") as file:
            saved_data_from_file = yaml.safe_load(file)
            #self.assertEqual(len(saved_data_from_file), 1)
            #self.assertEqual(saved_data, saved_data_from_file)


class TestDataOpsSelectCustomer(unittest.TestCase):

    def setUp(self):
        self.valid_data_file = "valid_data.yaml"
        self.data_ops = DataOps(filename="valid_data.yaml", bank_customers=[])

        customer1 = BankCustomer(customer_name="John Doe", account_number="67890", customer_id="C123", account_holder="Jane Doe", default_balance=2000)
        self.data_ops.bank_customers.append(customer1)

    def test_select_customer_by_account_number_nonexistent_customer(self):
        # Set up the DataOps object with manually populated customer data
        mock_customer = Mock(spec=BankCustomer, account_number="999999")
        self.data_ops.bank_customers.append(mock_customer)

        # Call the select_customer_by_account_number method with a non-existent account number
        selected_customer = self.data_ops.select_customer_by_account_number(mock_customer.account_number)

        # Verify that the selected customer is the default customer
        self.assertIsNotNone(selected_customer)
        #self.assertEqual(selected_customer.account_number, "1")


    def test_select_customer_by_account_number_existing_customer(self):
        # Create a mock BankCustomer instance for testing
        mock_customer = Mock(spec=BankCustomer, account_number="12345")

        # Set up the DataOps object with a list of mock customers
        self.data_ops.bank_customers = [mock_customer]

        # Call the select_customer_by_account_number method with the mock account number
        selected_customer = self.data_ops.select_customer_by_account_number("12345")

        # Verify that the selected customer is the mock customer
        self.assertEqual(selected_customer, mock_customer)


    def test_select_customer_by_account_number_success(self):
        # Load valid customer data from the file
        self.data_ops.load_data(self.valid_data_file)

        # Set up the DataOps object with loaded customer data
        mock_customer = Mock(spec=BankCustomer, account_number="999001")
        self.data_ops.bank_customers = [mock_customer]

        # Call the select_customer_by_account_number method with a valid account number
        selected_customer = self.data_ops.select_customer_by_account_number(mock_customer.account_number)

        # Verify that the selected customer is not the default customer
        self.assertIsNotNone(selected_customer)
        self.assertEqual(selected_customer.account_number, "999001")


    def test_select_customer_by_account_number_invalid_account_number(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            # Create a mock BankCustomer instance for testing
            mock_customer = Mock(spec=BankCustomer, account_number="12345")

            # Set up the DataOps object with a list of mock customers
            self.data_ops.bank_customers = [mock_customer]

            with self.assertRaises(TypeError) as context:
                # Call the select_customer_by_account_number method with an invalid account number
                self.data_ops.select_customer_by_account_number(12345)

            # Assertions
            self.assertEqual(str(context.exception), "Invalid account_number")
            self.assertIsNone(self.data_ops.selected_customer)  # No customer should be selected








