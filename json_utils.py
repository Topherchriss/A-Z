import json
from Alpha import BankAccount

def save_bank_account_data(account, filename):
     """
    Save the data of a BankAccount instance to a JSON file.

    Parameters:
    - account (BankAccount): The BankAccount instance to save.
    - filename (str): The name of the file to save the data to.

    Returns:
    None
    """
    try:
        with open(filename, "w") as file:
            json.dump(account.to_json(), file, indent=2)
    except Exception as e:
        print(f"An error occurred while saving data: {e}")

def load_bank_account_data(filename):

    """
    Load data from a JSON file and create a BankAccount instance.

    Parameters:
    - filename (str): The name of the file to load data from.

    Returns:
    BankAccount or None: The loaded BankAccount instance, or None if an error occurred.
    """

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
