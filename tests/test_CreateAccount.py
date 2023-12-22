import unittest
import yaml
from unittest import TestCase
from unittest.mock import patch, Mock
from Gui_Trapeza import CreateAccount, DataOps
from Alpha import BankCustomer, BankAccount
import Alpha


#Helper functions
def load_data(filename):
    with open(filename, "r") as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

def save_data(filename, data):
    with open(filename, "w") as file:
        yaml.dump(data, file, default_flow_style=False)

class TestCreateAccount(unittest.TestCase):

    def setUp(self):
        # Mock DataOps and BankCustomer for testing
        mock_data_ops = Mock(spec=DataOps, autospec=True)
        mock_data_ops.bank_customers = [] # Initialize with an empty list
        self.data_ops = mock_data_ops
        self.customer = Mock(spec=BankCustomer, existing_customer=Mock(spec=BankCustomer))
        self.create_account = CreateAccount(self.data_ops, self.customer)

    def test_has_matching_information_matching_id(self):
        account_data = {"customer_id": "123"}
        self.customer.customer_id = "123"
        result = self.create_account.has_matching_information(account_data)
        self.assertTrue(result)

    def test_has_matching_information_matching_attributes(self):
        account_data = {"customer_id": "123", "other_attr": "value"}
        self.customer.customer_id = "123"
        self.customer.other_attr = "value"
        result = self.create_account.has_matching_information(account_data)
        self.assertTrue(result)


class CreateAccountTest(unittest.TestCase):

    def setUp(self):
        # Mock DataOps and BankCustomer for testing
        mock_data_ops = Mock(spec=DataOps, autospec=True)
        mock_data_ops.bank_customers = [] # Initialize with an empty list
        self.data_ops = mock_data_ops
        self.customer = Mock(spec=BankCustomer, existing_customer=Mock(spec=BankCustomer))
        self.filename = "customer_tests.yaml"
        self.initial_data = load_data(self.filename) # Load initial data
        self.create_account_service = CreateAccount(self.data_ops, self.customer)
        self.created_customer = None

    def load_data(filename):
        with open(filename, "r") as file:
            yaml_data = yaml.safe_load(file)
        return yaml_data

    def save_data(filename, data):
        with open(filename, "w") as file:
            yaml.dump(data, file, default_flow_style=False)

    def test_create_customer_valid_data(self):
        """Test creating a new customer with valid data."""
        account_data = {
            "customer_name": "Mwalimu Daktari",
            "account_number": "12345",
            "account_holder": "Teacher Doctor",
            "customer_id": "1",
            "default_balance": 0.0,
        }

        customer = self.create_account_service.create_customer(account_data)

        # Verify data saved
        #saved_data = load_data(self.filename)

        self.assertEqual(customer.customer_name, "Mwalimu Daktari")
        self.assertEqual(customer.account_number, "12345")
        self.assertEqual(customer.account_holder, "Teacher Doctor")
        self.assertEqual(customer.customer_id, "1")
        self.assertEqual(customer.default_balance, 0.0)
        self.assertGreaterEqual(len(self.filename), len(self.initial_data))

        #self.assertDictEqual(self.loaded, customer.to_yaml())

    def test_create_customer_missing_data(self):
        """Test creating a new customer with missing data."""
        account_data = {
            "account_number": "11111",
            "account_holder": "Police",
            "customer_id": "2",
            "default_balance": 100.0,
        }

        # Test missing required data
        with self.assertRaises(KeyError):
            self.create_account_service.create_customer(account_data)

        # Add customer name and test default balance
        account_data["customer_name"] = "Polisi"
        customer = self.create_account_service.create_customer(account_data)
        self.assertEqual(customer.default_balance, 100.0)


    def test_create_account_existing_customer_unchanged_data(self):
        """Test that existing customer data remains unchanged."""

        existing_customer_data = {
            "customer_name": "Jane",
            "account_number": "11111",
            "account_holder": "Kamala",
            "customer_id": "2",
            "default_balance": 100.0,
        }

        # Create existing customer data
        self.create_account_service.create_customer(account_data=existing_customer_data)

        # Account data with same customer ID
        account_data = {
            "customer_name": "Jane",
            "account_number": "11111",
            "account_holder": "Kamala",
            "customer_id": "2",
            "default_balance": 100.0
        }

        # Attempt to create account (should NOT create)
        account = self.create_account_service.create_account(account_data)
        save_data(self.filename, account_data)

        # Verify that saved_data is not None
        saved_data = load_data(self.filename)
        self.assertIsNotNone(saved_data)

        saved_data = load_data(self.filename)
        if saved_data:
            self.assertTrue(all(key in saved_data and saved_data[key] == value for key, value in existing_customer_data.items()))
        else:
            self.fail("No saved data found")

        """
        customer_data = saved_data.items()
        for key, value in saved_data.items():
            if key in existing_customer_data:
                self.assertEqual(value, existing_customer_data[key])
            else:
                self.fail("Failed")

        if customer_data:
            self.assertEqual(customer_data, existing_customer_data)
        #else:
         #   self.fail("Customer data with ID 2 not found")

        if customer_data:
            for key, value in existing_customer_data.items():
                self.assertEqual(customer_data[key], value)
        """

