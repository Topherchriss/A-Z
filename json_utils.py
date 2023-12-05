import json
from Alpha import BankAccount


cached_data = None  # Global variable to store cached data and avoid data being loaded multiple times

def save_bank_account_data(bank_account, filename):

    """"
    This function saves the data of a BankAccount object to a JSON file.

    Parameters:

    bank_account: The BankAccount object to save.
    filename: The filename to save the data to.
    Returns:
    None

    Exceptions:

    Exception: An error occurred while saving the account data.
    """
    try:
        data = bank_account.to_json()
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        print(f"An error occurred while saving account data: {e}")

def load_bank_account_data(filename):

    """
    This function loads the data of a BankAccount object from a JSON file.

    Parameters:
    filename: The filename to load the data from.

    Returns:
    The data of a BankAccount object loaded from the file, or None if there was an error.

    Exceptions:
    FileNotFoundError: The file does not exist.
    json.JSONDecodeError: The file contains invalid JSON.
    Exception: An error occurred while loading the account data.

    """
    print("Loading account data from file:", filename)

    global cached_data
    # Check if data is already cached
    if cached_data is not None:
        return cached_data
        print("Cached data found, returning cached data")

    try:
        with open(filename, 'r') as file:
            data = json.load(file)

            # Fix the data types
            data['account_balance'] = float(data['account_balance'])

            for transaction in data['transaction_history']:
                try:
                    transaction['amount'] = float(transaction['amount'])
                except ValueError as ve:
                    print(f"Error converting 'amount' to float: {ve}")
                    return None
            print("Data conversion complete")

            #Store the loaded data in the cache
            cached_data = data
            print("Cached data updated")

            return data

    except FileNotFoundError:
        # Handle the case where the file doesn't exist
        print(f"File {filename} not found.")
        return None

    except json.JSONDecodeError:
        # Handle the case where the file contains invalid JSON
        print(f"Invalid JSON format in file {filename}.")
        return None

    except Exception as e:
        print(f"An error occurred while loading account data: {e}")
        return None


