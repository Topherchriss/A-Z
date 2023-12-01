import json
from Alpha import BankAccount

def save_bank_account_data(account, filename):
    with open(filename, "w") as file:
        json.dump(account.to_json(), file, indent=2)

def load_bank_account_data(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    # Create a new BankAccount object
    account = BankAccount(
        account_number=data["account_number"],
        account_holder=data["account_holder"],
        customer_id=data["customer_id"],
        default_balance=data["account_balance"],
    )

    # Populate other attributes from the loaded data
    account.transaction_history = data["transaction_history"]
    account.budget_categories = data["budget_categories"]
    account.cumulative_expenses = data["cumulative_expenses"]
    account.threshold = data["threshold"]

    return account
