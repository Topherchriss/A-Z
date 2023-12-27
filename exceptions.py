class InsufficientFundsError(Exception):
    """
    Raised when an attempt is made to perform a financial operation (e.g., withdrawal) that would exceed the available balance of the account.

    This exception is typically triggered when:

    * The requested withdrawal amount is greater than the current account balance.
    * An attempt is made to debit the account for an amount exceeding the available funds.
    * An attempt is made to set a budget category with a limit exceeding the current account balance.
    * The provided threshold value is higher than the current account balance.


    This exception helps ensure that financial operations respect the current account balance and prevent situations where the account goes into negative balance.
    """
    def __init__(self, message="Insufficient funds to proceed."):
        self.message = message
        super().__init__(self.message)

class InvalidDepositAmountError(Exception):
    """
    Raised when an attempt is made to deposit a non-numerical value or a negative amount.

    This exception is typically triggered when:

    * The provided deposit amount is not a valid number (a string or a symbol).
    * The provided deposit amount is negative.

    This exception ensures that only valid deposits are recorded in the account and prevents accidental or invalid entries from being processed.

    """
    def __init__(self, message="Invalid deposit amount. Please enter a valid number."):
        self.message = message
        super().__init__(self.message)

class InvalidWithrawalAmountError(Exception):
    """
    Raised when an attempt is made to withdraw an invalid amount from an account.

    This exception is typically triggered when:

    * The requested withdrawal amount is negative or zero.

    This exception helps prevent erroneous withdrawals that could potentially affect the account balance and ensures that only valid withdrawals are processed.
    """
    def __init__(self, message="Withrawal amount cannot be a negative value or $0"):
        self.message = message
        super().__init__(self.message)

class InvalidCustomerIDError(Exception):
    """
    Raised when an attempt is made to perform an operation requiring a valid customer ID that is either missing or not recognized.

    This exception is typically triggered when:

    * The provided customer ID is not a valid string value. (Customer ID in some parts of the code will be reffered to as PIN )
    * The provided customer ID does not match any existing customer record in the system's data.

    This exception helps maintain data integrity and ensures that operations are performed on the correct account holder.
    """

    def __init__(self, message="Invalid customer ID."):
        self.message = message
        super().__init__(self.message)

class InvalidAccountNumberError(Exception):
    """
    Raised when an attempt is made to perform an operation requiring a valid account number that is either missing or not recognized.

    This exception is typically triggered when:

    * The provided account number is not a valid string value.
    * The provided account number does not match any existing account record in the system's data.

    This exception helps maintain data integrity and ensures that operations are performed on the correct account.
    """

    def __init__(self, message="Invalid account number."):
        self.message = message
        super().__init__(self.message)

class InvalidBudgetLimitError(Exception):
    """
    Raised when an attempt is made to set a budget limit with an invalid value.

    This exception is typically triggered when:

    * The provided budget limit is not a valid numerical value.(a string or a symbol)
    * The provided budget limit is negative.

    This exception ensures that budget limits are set with meaningful values and prevents potential errors in budget calculations and tracking.
    """

    def __init__(self, message="Invalid limit amount."):
        self.message =  message
        super().__init__(self.message)

class BudgetCategoryNotFoundError(Exception):
    """
    Raised when an attempt is made to perform a budget-related operation on a category that does not exist within the account's budget configuration.

    This exception is typically triggered when:

    * The provided budget category name is not found in the account's existing budget categories.
    * An attempt is made to spend or track expenses for a non-existent category.

    This exception helps maintain budget integrity and ensures that operations are performed on valid categories within the account's budget structure.
    """
    def __init__(self, message="Budget Category not found"):
        self.message = message
        super().__init__(self.message)

class BudgetCategoryAlreadyExistsError(Exception):
    """
    Raised when an attempt is made to set a budget for a category that is already defined and configured within the account.

    This exception is typically triggered when:

    * The provided budget category name already exists in the account's budget configuration.
    * An attempt is made to duplicate an existing budget category.

    This exception helps prevent redundant budget setups and ensures that categories are configured uniquely and only once within an account.
    """
    def __init__(self, message="Budget Category already set"):
        self.message = message
        super().__init__(self.message)

class InvalidThresholdAmountError(Exception):
    """
    Raised when an attempt is made to set a threshold for the account balance with an invalid value.

    This exception is typically triggered when:

    * The provided threshold value is not a valid numerical value.(A string or a symbol)
    * The provided threshold value is negative.
    * The provided threshold value is higher than the current account balance.

    This exception ensures that thresholds are set with meaningful and valid values and prevents situations where the threshold set is higher than the current account balance and cannot be effectively monitored.
    """
    def __init__(self, message="Invalid Threshold amount"):
        self.message = message
        super().__init__(self.message)

class AccountCreationError(Exception):
    """
    Raised when an error occurs during the process of creating a new account for a customer.

    This exception is a generic error handler for unexpected issues that may arise during account creation, such as data related errors, data validation failures, or system limitations.

    The specific message attached to this exception can provide more details about the nature of the error encountered.

    This exception helps inform users about unsuccessful account creation attempts and allows to diagnose and address potential issues with the account creation process.
    """
    def __init__(self, message="An error occure while creating your account.Please try again later"):
        self.message = message
        super().__init__(self.message)

class WrongCustomerIdError(Exception):
    """
    Raised when an attempt is made to perform an operation requiring a Customer ID(PIN) that is not recognized

    This exception is error handler for wrong customer IDs .The specific message attached to this exception provides more details

    This exception ensures data integrity and avoids performing actions on unauthoritized accounts. Helps inform users about unsuccessful operation attempts due to wrong Customer ID(PIN);diffrent ones from the one used to create the account in.
    """
    def __init__(self, message="You entered the wrong Customer ID(PIN)"):
        self.message = message
        super().__init__(self.message)


class NoCustomerSelectedError(Exception):
    """
    Raised when an operation requires a selected customer, but none is currently selected.

    This exception is typically triggered when attempting to perform an action that requires an active customer selection, such as setting a budget or performing a transaction.
    It ensures that the application user selects a customer before proceeding with certain operations and prevent users from performing operations on unauthoritized accounts
    """
    def __init__(self, message="Please select a customer first"):
        self.message = message
        super().__init__(self.message)


class ExceedingBudgetLimitError(Exception):
    """
    Raised when an expense exceeds the budget limit set for a specific category.

    This exception is typically triggered when attempting to spend an amount from a budget category, and the proposed expense surpasses the predefined budget limit.
    It helps in maintaining financial discipline by preventing expenditures beyond the set limits.
    """
    def __inti__(self, message="Exceeding budget limit"):
        self.message = message
        super().__init__(self.message)


class InvalidExpenseAmountError(Exception):
    """
    Raised when an attempt is made to spend an invalid or non-positive amount.

    This exception is typically triggered when trying to perform an expense, and the provided amount is either not a valid numerical value or is less than $1.
    It ensures that expenses are made with meaningful and positive values.
    """
    def __init__(self, message=("Invalid expense amount. Please enter a positive value.")):
        self.message = message
        super().__init__(self.message)