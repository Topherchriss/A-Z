import json
from Alpha import BankAccount

def save_bank_account_data(account, filename):
    try:
        with open(filename, "w") as file:
            json.dump(account.to_json(), file, indent=2)
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

def load_bank_account_data(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            if data:
                return BankAccount.from_json(data)
    except FileNotFoundError:
        # If the file doesn't exist, return None or handle accordingly
        print(f"File {filename} not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None
