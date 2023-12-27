import unittest
import yaml
import Alpha
from unittest import TestCase
from unittest.mock import patch, Mock, create_autospec, PropertyMock
from Gui_Trapeza import CreateAccount, DataOps, BudgetActions
from Alpha import BankCustomer, BankAccount
from exceptions import InvalidBudgetLimitError, BudgetCategoryAlreadyExistsError, InvalidCustomerIDError, InvalidThresholdAmountError, WrongCustomerIdError, BudgetCategoryNotFoundError, InvalidThresholdAmountError, InsufficientFundsError

class TestBudgetActions(unittest.TestCase):
    """
    Test cases for the 'set_budget_category' method in the 'BudgetActions' class.
    """

    def setUp(self):

        # Create an instance of BudgetActions for testing
        mock_data_ops = Mock(spec=["selected_customer"], autospec=True)
        mock_bank_account = Mock(spec=["budget_categories", "set_budget"], autospec=True)
        mock_budget_actions = Mock(spec=["set_budget_category"], autospec=True)
        self.data_ops = mock_data_ops
        self.bank_account = mock_bank_account
        self.budget_actions = mock_budget_actions
        self.budget_actions = BudgetActions(data_ops=self.data_ops, bank_account=self.bank_account)


    def test_set_budget_category_success(self):
        with patch('Gui_Trapeza.messagebox.showinfo') as mock_showinfo:

            account_data = {
            "account_number": "11111",
            "account_holder": "Nyoso",
            "customer_id": "345",
            "default_balance": 1000.0,
            }

            # Set up mock data for testing
            category = "Groceries"
            limit = 500.0
            customer_id = "345"

            self.data_ops.selected_customer.customer_id = customer_id
            self.data_ops.selected_customer.account_balance = 1000.0  # Set a valid account balance for the test


            # Set up mock return values for bank_account
            self.bank_account.budget_categories = {}

            # Test set_budget_category with valid input
            result = self.budget_actions.set_budget_category(category, limit, customer_id)
            # Assertions
            self.assertTrue(result)
            self.assertIsNotNone(self.bank_account.budget_categories)
            mock_showinfo.assert_called_once_with("Success", f"Dear customer a budget category of {category} with a limit of ${limit} was successfully added to your budget categories")


    def test_set_budget_category_invalid_limit(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            account_data = {
                "account_number": "34590",
                "account_holder": "Mwana",
                "customer_id": "2",
                "default_balance": 1000.0,
                }

            # Set up mock data for testing
            category = "Groceries"
            limit = -3990.0
            customer_id = "2"


            # Set up mock return values for bank_account
            self.bank_account.budget_categories = {}

            # Test set_budget_category with invalid customeer ID
            with self.assertRaises(InvalidBudgetLimitError) as context:
                self.budget_actions.set_budget_category(category, limit, customer_id)

            self.assertEqual(str(context.exception), f"Budget limit cannot be a negative value.")

            mock_showerror.assert_called_once_with('Error', 'Budget limit cannot be a negative value.')


    def test_set_budget_category_budget_already_exists(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            account_data = {
                "account_number": "377uyyt7",
                "account_holder": "nzibi",
                "customer_id": "98770",
                "default_balance": 1000.0,
                }

            # Set up mock data for testing
            category = "Books"
            limit = 100.0
            customer_id = account_data["customer_id"]

            self.data_ops.selected_customer.account_balance = 1000.0  # Set a valid account balance for the test

            # Set up mock return values for bank_account
            self.bank_account.budget_categories = {category: limit}

            # Test set_budget_category with existing category
            with self.assertRaises(BudgetCategoryAlreadyExistsError) as context:
                self.budget_actions.set_budget_category(category=category, limit=limit, customer_id=customer_id)

            # Assertions
            self.assertIsNotNone(self.bank_account.budget_categories)

            self.assertEqual(str(context.exception), f"Budget category 'Books' already has a limit set.")

            mock_showerror.assert_called_once_with('Error', "Budget category 'Books' already has a limit set.")

    def test_set_budget_category_invalid_customer_id(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            account_data = {
                "account_number": "678uy7",
                "account_holder": "Yale",
                "customer_id": "990",
                "default_balance": 10000.0,
                }

            # Set up mock data for testing
            category = "Bills"
            limit = 900.0
            customer_id = 990

            self.data_ops.selected_customer.customer_id = customer_id

            # Set up mock return values for bank_account
            self.bank_account.budget_categories = {}

            # Test set_budget_category with invalid customeer ID
            with self.assertRaises(TypeError) as context:
                self.budget_actions.set_budget_category(category, limit, customer_id)

            # Assertions
            self.assertEqual(str(context.exception), f"Customer ID must be a string.")
            mock_showerror.assert_called_once_with('Error', 'Customer ID must be a string.')

    def test_set_budget_category_limit_exceeding_account_balance(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            account_data = {
                "account_number": "678uy7",
                "account_holder": "Yale",
                "customer_id": "990",
                "default_balance": 1000.0,
                }

            # Set up mock data for testing
            category = "Bills"
            limit = 1900.0
            customer_id = "990"

            self.data_ops.selected_customer.customer_id = customer_id
            self.data_ops.selected_customer.account_balance = 1000.0  # Set a valid account balance for the test


            # Set up mock return values for bank_account
            self.bank_account.budget_categories = {}

            # Test set_budget_category with invalid customeer ID
            with self.assertRaises(InsufficientFundsError) as context:
                self.budget_actions.set_budget_category(category, limit, customer_id)

            # Assertions
            self.assertEqual(str(context.exception), f"Insufficient funds to proceed, budget limit cannot exceed current account balance.")
            mock_showerror.assert_called_once_with('Error', 'Insufficient funds to proceed, budget limit cannot exceed current account balance.')

class TestBudgetActionsGetBudgetCategories(unittest.TestCase):
    """
    Test cases for the 'get_budget_categories' method in the 'BudgetActions' class.
    """

    def setUp(self):
        # Create an instance of BudgetActions for testing
        mock_data_ops = Mock(spec=["selected_customer"], autospec=True)
        mock_bank_account = Mock(spec=["budget_categories", "set_budget"], autospec=True)
        mock_budget_actions = Mock(spec=["set_budget_category"], autospec=True)
        self.data_ops = mock_data_ops
        self.bank_account = mock_bank_account
        self.budget_actions = mock_budget_actions
        self.budget_actions = BudgetActions(data_ops=self.data_ops, bank_account=self.bank_account)


    def test_get_budget_categories_success(self):

        # Set up mock data for testing
        customer_id = "1234"
        expected_budget_categories = {"Groceries": 500, "Entertainment": 200}

        # Set the selected customer ID in data_ops
        self.data_ops.selected_customer.customer_id = customer_id

        # Set up mock return values for bank_account
        self.bank_account.budget_categories = expected_budget_categories

        # Test get_budget_categories with valid customer ID
        result = self.budget_actions.get_budget_categories(customer_id)

        # Assertions
        self.assertTrue(result)
        self.assertEqual(result, expected_budget_categories)


    def test_get_budget_categories_invalid_customer_id(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            customer_id = 1234
            self.data_ops.selected_customer.customer_id = customer_id

            with self.assertRaises(TypeError) as context:
                # Test get_budget_categories with invalid customer ID
                self.budget_actions.get_budget_categories(customer_id)

            # Assertions
            self.assertEqual(str(context.exception), "Customer ID must be a string.")
            mock_showerror.assert_called_once_with("Error", "Customer ID must be a string.")

    def test_get_budget_categories_wrong_customer_id(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            account_data = {
                "account_number": "678uy7",
                "account_holder": "Yale",
                "customer_id": "990",
                "default_balance": 1000.0,
                }

            customer_id = account_data["customer_id"]

            self.data_ops.selected_customer.customer_id = customer_id

            with self.assertRaises(WrongCustomerIdError) as context:
                # Test get_budget_categories with wrong customer ID
                self.budget_actions.get_budget_categories(customer_id="99")

            # Assertions
            self.assertEqual(str(context.exception), "You entered the wrong Customer ID(PIN)")
            mock_showerror.assert_called_once_with("Error", "You entered the wrong Customer ID(PIN)")


class TestBudgetActionsGetBudgetCategoryLimit(unittest.TestCase):
    """
    Test cases for the 'get_category_limit' method in the 'BudgetActions' class.
    """

    def setUp(self):
        # Create an instance of BudgetActions for testing
        mock_data_ops = Mock(spec=["selected_customer"], autospec=True)
        mock_bank_account = Mock(spec=["budget_categories", "set_budget"], autospec=True)
        mock_budget_actions = Mock(spec=["set_budget_category"], autospec=True)
        self.data_ops = mock_data_ops
        self.bank_account = mock_bank_account
        self.budget_actions = mock_budget_actions
        self.budget_actions = BudgetActions(data_ops=self.data_ops, bank_account=self.bank_account)

    def test_get_budget_category_limit_success(self):

        # Set up mock data for testing
        customer_id = "670"
        category = "Groceries"
        expected_budget_limit = 500.0

        # Set the selected customer ID in data_ops
        self.data_ops.selected_customer.customer_id = customer_id

        # Set up mock return values for bank_account
        self.bank_account.budget_categories = {category: expected_budget_limit}

        # Test get_budget_category_limit with valid customer ID and category
        result = self.budget_actions.get_budget_category_limit(category, customer_id)

        # Assertions
        self.assertEqual(result, expected_budget_limit)


    def test_get_budget_category_limit_invalid_customer_id(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            with self.assertRaises(TypeError) as context:
                # Test get_budget_category_limit with invalid customer ID
                self.budget_actions.get_budget_category_limit("Groceries", 1234)

            # Assertions
            self.assertEqual(str(context.exception), f"Invalid customer ID")
            mock_showerror.assert_called_once_with('Error', 'Invalid customer ID')


    def test_get_budget_category_limit_wrong_customer_id(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            account_data = {
                "account_number": "678uy7",
                "account_holder": "Lolwe",
                "customer_id": "670",
                "default_balance": 1000.0,
                }

            customer_id = account_data["customer_id"]
            category =  "Groceries"

            # Set the selected customer ID in data_ops
            self.data_ops.selected_customer.customer_id = customer_id

            with self.assertRaises(WrongCustomerIdError) as context:
                # Test get_budget_category_limit with invalid customer ID
                self.budget_actions.get_budget_category_limit(category, customer_id="1234")

            # Assertions
            self.assertEqual(str(context.exception), f"You entered the wrong Customer ID(PIN)")
            mock_showerror.assert_called_once_with("Error", f"You entered the wrong Customer ID(PIN)")


    def test_get_budget_category_limit_nonexistent_category(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            # Set up mock data for testing
            customer_id = "1987"
            existing_category = "Groceries"
            predefined_categories = {"Groceries": 500, "Entertainment": 200, "Utilities": 300}

            # Set the selected customer ID in data_ops
            self.data_ops.selected_customer.customer_id = customer_id

            # Set up mock return values for bank_account
            self.bank_account.budget_categories = predefined_categories

            # Test get_budget_category_limit with a non-existent category
            non_existent_category = "NuhImNotInThere"
            with self.assertRaises(BudgetCategoryNotFoundError) as context:
                self.budget_actions.get_budget_category_limit(non_existent_category, customer_id)

            #Try it out with the existing category
            result = self.budget_actions.get_budget_category_limit(existing_category, customer_id)

            # Assertions
            self.assertEqual(str(context.exception), f"Budget category '{non_existent_category}' not found.")
            mock_showerror.assert_called_once_with("Error", f"Budget category '{non_existent_category}' not found.")
            self.assertTrue(result)


class TestBudgetActionsUpdateBudgetCategoryLimit(unittest.TestCase):
    """
    Test cases for the 'update_budget_category_limit' method in the 'BudgetActions' class.
    """

    def setUp(self):

        # Create an instance of BudgetActions for testing
        self.mock_data_ops = Mock(spec=["selected_customer"], autospec=True)
        self.mock_bank_account = Mock(spec=["budget_categories", "set_budget", "get_budget_categories"], autospec=True)
        self.mock_showerror = Mock()
        self.data_ops = self.mock_data_ops
        self.bank_account = self.mock_bank_account
        self.budget_actions = BudgetActions(data_ops=self.data_ops, bank_account=self.bank_account)


    def test_update_budget_category_limit_invalid_customer_id(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            # Set up mock data for testingS
            category = "Groceries"
            new_limit = 600
            customer_id = 5678

            # Test update_budget_category_limit with invalid customer ID
            with self.assertRaises(TypeError) as context:
                self.budget_actions.update_budget_category_limit(category, new_limit, customer_id)

            # Assertions
            self.assertEqual(str(context.exception), 'Customer ID must be a string.')
            mock_showerror.assert_called_once_with("Error","Customer ID must be a string.")


    def test_update_budget_category_limit_negative_limit(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            # Set up mock data for testing
            category = "Groceries"
            new_limit = -100
            customer_id = "1234"

            # Test update_budget_category_limit with negative limit
            with self.assertRaises(InvalidBudgetLimitError) as context:
                self.budget_actions.update_budget_category_limit(category, new_limit, customer_id)

            # Assertions
            self.assertEqual(str(context.exception), 'limit must be more than a $1')
            mock_showerror.assert_called_once_with('Error', 'limit must be more than a $1')
"""
 **Test Suite: `test_BudgetActionsUpdateBudgetCategoryLimit`**

This test suite specifically uses inheritance to address an encountered `AttributeError` related to accessing attributes on a mock `BankAccount` instance. Normally, separate test classes are preferred for each method. However, inheritance proved necessary in this case due to the following reasons:

1. **Previously, using a direct instance of `BankAccount` caused the instance to be empty (without attributes) within the test cases.** This resulted in an `AttributeError` when attempting to access attributes like `budget_categories` on the empty instance.
2. **To solve this, the `MockBankAccount` class inherits from `BankAccount` and initializes essential attributes in its `__init__` method.** This ensures that the mock `BankAccount` instance is fully populated with the required attributes before each test, preventing the `AttributeError`.

* **Inheritance succesfully Eliminates `AttributeError`:** By inheriting from `BankAccount` and initializing missing attributes, we avoid accessing undefined attributes on an empty instance.

**Note:**
This inheritance is a one time approach specific to addressing the encountered `AttributeError`.
"""

class MockBankAccount(BankAccount):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set needed attributes
        self.budget_categories = {}
        self.get_budget_categories = {"Groceries": 500, "Home": 700}


class TestBudgetActionsUpdateBudgetCategoryLimitSuccessNonExisting(unittest.TestCase):

    def setUp(self):
        # Create an instance of BudgetActions for testing
        mock_data_ops = Mock(spec=["selected_customer"], autospec=True)
        mock_bank_account = MockBankAccount(BankAccount)
        self.data_ops = mock_data_ops
        self.bank_account = mock_bank_account
        self.budget_actions = BudgetActions(data_ops=self.data_ops, bank_account=self.bank_account)

    def test_update_budget_category_limit_success(self):

        # Set up mock data for testing
        category = "Home"
        new_limit = 600
        customer_id = "1423"

        self.budget_categories = {"Groceries": 500, "Home": 700}

        # Set the selected customer ID in data_ops
        self.data_ops.selected_customer.customer_id = customer_id

        # Set a valid account balance for the test
        self.data_ops.selected_customer.account_balance = 10000.0

        # Test update_budget_category_limit with valid input
        self.budget_actions.update_budget_category_limit(category="Home", new_limit=600, customer_id=customer_id)

        # Assertions
        self.assertEqual(self.bank_account.budget_categories[category], new_limit)


    def test_update_budget_category_limit_nonexistent_category(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            # Set up mock data for testing
            category = "NonExistentCategory"
            new_limit = 600
            customer_id = "1234"


            # Set the selected customer ID in data_ops
            self.data_ops.selected_customer.customer_id = customer_id

            # Set a valid account balance for the test
            self.data_ops.selected_customer.account_balance = 1000.0


            # Test update_budget_category_limit with non-existent category
            with self.assertRaises(BudgetCategoryNotFoundError) as context:
                self.budget_actions.update_budget_category_limit(category, new_limit, customer_id)

            # Assertions
            self.assertEqual(str(context.exception), f"Budget category '{category}' not found.")
            mock_showerror.assert_called_once_with('Error', "Budget category 'NonExistentCategory' not found.")

class TestBudgetActionsThreshold(unittest.TestCase):
    """
    Test cases for the 'threshold' method in the 'BudgetActions' class.
    """

    def setUp(self):
        """
        Set up common attributes and create an instance of BudgetActions for testing.
        """
        # Create an instance of BudgetActions for testing
        self.mock_data_ops = Mock(spec=["selected_customer"], autospec=True)
        self.mock_bank_account = Mock(spec=["set_threshold"], autospec=True)
        self.mock_showerror = Mock()
        self.data_ops = self.mock_data_ops
        self.bank_account = self.mock_bank_account
        self.budget_actions = BudgetActions(data_ops=self.data_ops, bank_account=self.bank_account)

    def test_threshold_valid_input(self):

        # Set up mock data for testing
        threshold = 100
        customer_id = "5678"

        # Set the selected customer ID in data_ops
        self.data_ops.selected_customer.customer_id = customer_id

        # Set a valid account balance for the test
        self.data_ops.selected_customer.account_balance = 1000.0

        # Test threshold with valid input
        self.budget_actions.threshold(threshold, customer_id)

        # Assertions
        self.bank_account.set_threshold.assert_called_once_with(threshold, customer_id)

    def test_threshold_invalid_customer_id(self):

        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:
            # Set up mock data for testing
            threshold = 100
            customer_id = 5678

            # Test threshold with invalid customer ID
            with self.assertRaises(TypeError) as context:
                self.budget_actions.threshold(threshold, customer_id)

            # Assertions
            self.assertEqual(str(context.exception), 'Customer ID must be a string.')
            mock_showerror.assert_called_once_with("Error", "Customer ID must be a string.")

    def test_threshold_invalid_threshold_value(self):

        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:
            # Set up mock data for testing
            threshold = -50
            customer_id = "1234"

            # Test threshold with invalid threshold value
            with self.assertRaises(InvalidThresholdAmountError) as context:
                self.budget_actions.threshold(threshold, customer_id)

            # Assertions
            self.assertEqual(str(context.exception), 'Threshold must be more than a $1')
            mock_showerror.assert_called_once_with('Error', 'Threshold must be more than a $1')

    def test_threshold_exceeds_account_balance(self):

        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:
            # Set up mock data for testing
            threshold = 2000
            customer_id = "5678"

            # Set the selected customer ID in data_ops
            self.data_ops.selected_customer.customer_id = customer_id

            # Set a valid account balance for the test
            self.data_ops.selected_customer.account_balance = 1000.0

            # Test threshold that exceeds account balance
            with self.assertRaises(InsufficientFundsError) as context:
                self.budget_actions.threshold(threshold, customer_id)

            # Assertions
            self.assertEqual(str(context.exception), 'Threshold cannot be more than current account balance')
            mock_showerror.assert_called_once_with('Error', 'Threshold cannot be more than current account balance')

    def test_threshold_wrong_customer_id_error(self):
        with patch("Gui_Trapeza.messagebox.showerror") as mock_showerror:

            # Set up mock data for testing
            threshold = 100
            customer_id = "5678"

            # Set the selected customer ID in data_ops
            self.data_ops.selected_customer.customer_id = customer_id

            # Set a valid account balance for the test
            self.data_ops.selected_customer.account_balance = 1000.0

            # Test threshold with invalid customer ID
            with self.assertRaises(WrongCustomerIdError) as context:
                self.budget_actions.threshold(threshold, customer_id="9876")

            # Assertions
            self.assertEqual(str(context.exception), 'Wrong Customer ID(PIN)')
            mock_showerror.assert_called_once_with('Error', 'Wrong Customer ID(PIN)')













