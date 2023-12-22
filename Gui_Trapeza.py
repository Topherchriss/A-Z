import tkinter as tk
import yaml
import unittest
from tkinter import messagebox
from Alpha import BankAccount, BankCustomer
from exceptions import InsufficientFundsError, InvalidDepositAmountError, InvalidCustomerIDError, InvalidAccountNumberError, InvalidBudgetLimitError, BudgetCategoryNotFoundError, BudgetCategoryAlreadyExistsError, InvalidThresholdError, AccountCreationError, InvalidWithrawalAmountError, WrongCustomerIdError

class DataOps:
    def __init__(self, filename: str, bank_customers: BankCustomer):
        self.filename = filename
        self.bank_customers = bank_customers if bank_customers is not None else []
        self.selected_customer: BankCustomer | None = None

    def load_data(self, filename):
        try:
            with open(self.filename, "r") as file:
                data = yaml.safe_load(file)

            if isinstance(data, list):
                for customer_data in data:

                    try:
                        if isinstance(customer_data, dict):

                            # Create a BankCustomer instance from the dictionary
                            customer = BankCustomer(**customer_data)
                            self.bank_customers.append(customer)

                    except KeyError as e:
                        print(f"Missing key '{e.args[0]}' in customer data")
                    except ValueError as e:
                        print(f"Invalid data type for key '{e.args[0]}' in customer data")
                    except TypeError as e:
                        print(f"Unexpected data type for customer data: {e}")
                    except yaml.YAMLError as e:
                        raise yaml.YAMLError(f"YAML Error: {e}")
                    except Exception as e:
                        print(f"Error loading customer data: {e}")

            print(f"Loaded {len(self.bank_customers)} customers from {self.filename}")


        except FileNotFoundError:
            # Handle file not found case
            print(f"File {self.filename} not found.")
        except yaml.YAMLError as e:
            # Handle invalid YAML format case
            print(f"YAML Error: {e}")
        except Exception as e:
            # Handle other unexpected exceptions
            print(f"An error occurred while loading data from {self.filename}: {e}")


    def get_all_customers(self):
        return self.bank_customers


    def save_data(self, filename, account_data):
        saved_data = []  # Initialize an empty list to store saved data

        try:
            with open(self.filename, "w") as file:

                for customer in self.bank_customers:
                    yaml.dump(customer.to_yaml(), file, default_flow_style=False)
                    file.flush()  # Explicitly flush after each customer data
                    saved_data.append(customer.to_yaml())  # Append the saved data to the list

            print("Account data saved")
            return saved_data  # Return the list of saved data as YAML strings

        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {e.filename}")

        except PermissionError as e:
            raise PermissionError(f"Permission denied: {e.filename}")

        except OSError as e:
            raise OSError(f"IO Error: {e}")

        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"YAML Error: {e}")

        except Exception as e:
            # Handle any other unexpected exceptions
            print(f"Error saving data to {self.filename}: {e}")


    def select_customer(self, customer_index: int):
        try:
            self.selected_customer = self.bank_customers[customer_index]
        except IndexError:
            # Handle invalid customer index case
            print(f"Invalid customer index provided: {customer_index}")


    def select_customer_by_account_number(self, account_number: str):
        """
        Selects the customer with the given account number.
        """
        self.load_data("valid_data.yaml")

        defaultCustomer = BankAccount(account_number="1", account_holder="Default", customer_id="2", default_balance=1000 )

        self.load_data("valid_data.yaml")

        if not isinstance(account_number, str):
            raise TypeError("Invalid account_number")

        try:
            if self.bank_customers:
                for customer in self.bank_customers:
                    if customer.account_number == account_number:
                        self.selected_customer = customer
                        return self.selected_customer
            else:
                self.selected_customer = defaultCustomer
                return defaultCustomer
                print("Default account selected")

        except InvalidAccountNumberError as e:
            print(f"Error. Enter a valid account number", {e})
            messagebox.showerror("Error",  f"Enter a valid account number")
            raise
        except TypeError as e:
            messagebox.showerror("Error", f"Error: {e}")
            raise
        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")
            raise
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
            raise


class CreateAccount:

    def __init__(self, data_ops: DataOps, customer: BankCustomer):
        self.data_ops = data_ops
        self.customer = customer


    def has_matching_information(self, account_data: dict):
        """
        Checks if the customer information matches the provided data.

        Parameters:
            account_data (dict): Dictionary containing customer information.

        Returns:
            boolean: True if information matches, False otherwise.
        """

        # Check for a matching customer ID first
        try:
            if self.customer.customer_id == account_data["customer_id"]:
                return True
        except KeyError as e:
            print(f"Error: {e}")

        # If no ID match, compare other relevant information
        for key, value in account_data.items():
            try:
                if hasattr(self, key) and getattr(self, key) == value:
                    return True
            except KeyError as e:
                print(f"Error: {e}")
        return False



    def create_customer(self, account_data: dict):
        """
        Create a new BankCustomer instance and add it to the list.

        Parameters:
            #customer_name (str): The name of the new customer.
            account_number (str): The account number of the new customer
            account_holder (str): The name to associate the acoount that will be created later on
            customer_id (str): The unique customer identifier
            default_balance (float): The initial amount to create account with

        Returns:
            BankCustomer: The newly created customer instance.
        """
        # Extract individual values from account_data
        customer_name = account_data["customer_name"]
        account_number = account_data["account_number"]
        account_holder = account_data["account_holder"]
        customer_id = account_data["customer_id"]
        default_balance = account_data["default_balance"]

        try:
            # Create customer with extracted values
            self.customer = BankCustomer(customer_name, account_number, account_holder, customer_id, default_balance)
            self.data_ops.bank_customers.append(self.customer)
            return self.customer

        except KeyError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error creating customer: {e}")
            raise


    def create_account(self, account_data: dict):
        """
        Create a new BankAccount instance and add it to the specified customer.

        Parameters:
            customer (BankCustomer): The customer to associate the account with.
            account_data (dict): The data dictionary containing account information.

        Returns:
            BankAccount: The newly created account instance.
        """
        # Check for existing customer with matching information
        existing_customer = None
        try:
            for customer in self.data_ops.bank_customers:
                if customer.has_matching_information(account_data):
                    existing_customer = customer
                    break

        except Exception as e:
            print(f"Error finding existing customer: {e}")
            raise

        # Account creation and data saving for new customers
        if not existing_customer:
            try:
                created_customer = self.create_customer(account_data)

                account = BankAccount(**dict(zip([ "account_number", "account_holder", "customer_id", "default_balance"], account_data)))

                created_account = created_customer.addAccount(account)
                self.data_ops.save_data("data_file.yaml", created_account)

                return created_account

            except Exception as e:
                print(f"Error creating new customer: {e}")
                raise


class InterfaceBank:

    def __init__(self, master, data_ops: DataOps, bank_account: BankAccount, account_creation: CreateAccount):
        self.master = master
        self.master.title("A-Z TRAPEZA")
        self.data_ops = data_ops
        self.bank_account = bank_account
        self.account_creation = account_creation
        self.customer = None

        # Setting a consistent color scheme
        bg_color_window = "#4d3d08"
        bg_color = "#5d6134"
        accent_color = "#548ca8"
        highlight_color = "#D8BFD8"
        tt_color = "#4d3d08"
        ff_color = "#ebc81a"

        # Master window background
        master.configure(bg=bg_color_window)

        # Labels for Customer info:
        label_texts = ["Customer's Name:", "Account number:", "Amount:",
                       "Customer ID(PIN):","Budget Category:", "Budget Limit:"]
        self.label_widgets = [tk.Label(master, text=text) for text in label_texts]


        # Entry fields
        entry_widgets = [tk.Entry(master) for _ in range(len(label_texts))]
        self.entry_customer_name, self.entry_account_number, self.entry_amount, \
            self.entry_customer_id, self.entry_budget_category, \
            self.entry_budget_limit = entry_widgets

        # Buttons
        button_texts = ["Deposit", "Withdraw", "Set Budget", "Create Account",
                        "Transactions", "Spend Budget", "Set Threshold", "Select Customer", "Check Balance", "Calculate", "Clear Data", "Exit A-Z"]

        button_commands = [self.deposit_cash, self.withdraw_cash, self.set_budget,
                           self.create_account_window, self.show_transactions, self.spend_budget,
                           self.set_threshold, self.select_customer, self.check_balance, self.calculate, self.clear_data, self.on_closing]

        self.button_widgets = [tk.Button(master, text=text, command=cmd, bg=accent_color, fg=ff_color)
                               for text, cmd in zip(button_texts, button_commands)]


        # Grid layout
        for i, label_widget in enumerate(self.label_widgets):
            label_widget.grid(row=i, column=0, padx=10, pady=10, sticky="e")
        for i, entry_widget in enumerate(entry_widgets):
            entry_widget.grid(row=i, column=1, padx=10, pady=10, sticky="w")
        for i, button_widget in enumerate(self.button_widgets[:3]):  # First three buttons
            button_widget.grid(row=i, column=2, columnspan=2, pady=10)

        # Set button
        self.button_widgets[4].grid(row=2, column=4, columnspan=2, pady=10)
        for i, button_widget in enumerate(self.button_widgets[3:5]):  # Remaining budget-related buttons
            button_widget.grid(row=len(label_texts) + 1, column=i, padx=10, pady=10)
        for i, button_widget in enumerate(self.button_widgets[5:]):  # Remaining buttons
            button_widget.grid(row=i, column=4, columnspan=2, pady=10)


        # Notification panel
        self.notification_text = tk.Text(master, height=2, width=40)
        self.notification_text.grid(row=len(label_texts) + 2, column=0, columnspan=6, pady=20)

        # Apply the background color to widgets
        for widget in self.label_widgets + self.button_widgets + [self.notification_text]:
            widget.configure(bg=tt_color, fg=ff_color)

        #for widget in self.label_widgets + entry_widgets + self.button_widgets + [self.notification_text]:
            #widget.configure(bg=tt_color)



    def create_account_window(self):
        """
        Creates a window for adding accounts.
        """
        # Create a new window
        account_window = tk.Toplevel(self.master)
        account_window.title("Create Account")

        # Define labels and entries with a dictionary
        account_fields = {
            "customer_name": {"label": "Customer Name", "entry": tk.Entry(account_window)},
            "account_number": {"label": "Account Number:", "entry": tk.Entry(account_window)},
            "account_holder": {"label": "Account Holder:", "entry": tk.Entry(account_window)},
            "customer_id": {"label": "Customer ID:", "entry": tk.Entry(account_window)},
            "default_balance": {"label": "Default Balance:", "entry": tk.Entry(account_window)},
        }

        # Add labels and entries to the grid layout
        row = 0
        for field_name, field_data in account_fields.items():
            label = tk.Label(account_window, text=field_data["label"])
            label.grid(row=row, column=0, padx=10, pady=10)
            field_data["entry"].grid(row=row, column=1, padx=10, pady=10)
            row += 1

        # Add button to add the account
        button_add_account = tk.Button(
            account_window, text="Add Account", command=lambda: self.add_account(account_fields))
        button_add_account.grid(row=row, column=0, columnspan=2, pady=10)

    def calculate(self):
        #Creating a window for the calculator pop up

        calc_window = tk.Toplevel(self.master)
        calc_window.title("Calculator")

        #entry fields for the calculator input
        entry_calc = tk.Entry(calc_window)
        entry_calc.grid(row=0, column=0, columnspan=4)

        # Calculator buttons
        calc_buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('DEL', 5, 0),

        ]

         # Create calculator buttons
        for (text, row, column) in calc_buttons:

            if text == 'DEL':

                button = tk.Button(calc_window, text=text, command=lambda: entry_calc.delete(len(entry_calc.get()) - 1, tk.END))
            else:

                button = tk.Button(calc_window, text=text, command=lambda t=text: entry_calc.insert(tk.END, t))
            button.grid(row=row, column=column, sticky='nsew')


        # Equal button action
        def calculate():
            expression = entry_calc.get()
            try:
                result = eval(expression)
                entry_calc.delete(0, tk.END)
                entry_calc.insert(tk.END, str(result))
            except Exception as e:
                entry_calc.delete(0, tk.END)
                entry_calc.insert(tk.END, "Error")
                entry_calc.delete(0, tk.END)

        # Create equal button separately
        equal_button = tk.Button(calc_window, text='=', command=calculate)
        equal_button.grid(row=4, column=2, columnspan=1, sticky='nsew')

        # Configure grid layout
        for i in range(5):
            calc_window.grid_rowconfigure(i, weight=1)
            calc_window.grid_columnconfigure(i, weight=1)

        #Used the eval() function for simplicty but can as well as implement the Calculator class from Extras and express it using the logic below

    #method to perform evaluation logic
    def evaluate_expression(expression, calculator):

        # Split the expression into tokens (numbers and operators)
        tokens = expression.split()

        # Initialize the operand stack
        operand_stack = []

        for token in tokens:
            if token.isdigit():
                # Push the operand onto the stack
                operand_stack.append(int(token))

            else:
                # Perform the corresponding operation
                if token == '+':
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    result = calculator.addition(operand1, operand2)
                    operand_stack.append(result)

                elif token == '-':
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    result = calculator.subtraction(operand1, operand2)
                    operand_stack.append(result)

                elif token == '*':
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    result = calculator.multiplication(operand1, operand2)
                    operand_stack.append(result)

                elif token == '/':
                    operand2 = operand_stack.pop()
                    operand1 = operand_stack.pop()
                    result = calculator.division(operand1, operand2)
                    operand_stack.append(result)

                else:
                    raise ValueError(f"Unsupported operator: {token}")

        # Check if there's only one operand left
        if len(operand_stack) != 1:
            raise ValueError("Invalid expression")

        # Return the final result
        return operand_stack[0]


    def add_account(self, account_fields):
        """
        Creates and adds a new account to the selected customer.

        Parameters:
                - account_fields (dict): A dictionary containing account input fields.
        """
        customer_name = account_fields["customer_name"]["entry"].get()
        account_number = account_fields["account_number"]["entry"].get()
        account_holder = account_fields["account_holder"]["entry"].get()
        customer_id = account_fields["customer_id"]["entry"].get()

        try:
            # Convert default balance to float
            default_balance = float(account_fields["default_balance"]["entry"].get())
        except ValueError:
            return "Invalid default balance format"


        # Validate input data
        if not account_number or not account_holder or not customer_id or not default_balance:
            self.display_notification("Fill in all required fields to proceed.")
            messagebox.showerror("Error", f"Fill in all required fields to proceed.")
            return

        """
        # Check for existing account with same number
        for customer in self.data_ops.bank_customers:
            for account in self.data_ops.customer.accounts:
                if account.account_number == account_number:
                    self.display_notification("Account with same number already exists.")
                    messagebox.showinfo("Account with same number exists")
                    return
        """
        # Check for existing account with the same number
        if any(account.account_number == account_number for customer in self.data_ops.bank_customers for account in customer.accounts):
            self.display_notification("Account with the same number already exists.")
            messagebox.showinfo("Account with same number exists")
            return


        # Create new account data dictionary(excluding entry widgets at the same time)
        account_data = {
            "customer_name": customer_name,
            "account_number": account_number,
            "account_holder": account_holder,
            "customer_id": customer_id,
            "default_balance": default_balance,
        }

        try:
            # Create an instance of CreateAccount with the needed dependencies
            create_account_service = CreateAccount(self.data_ops, self.customer)

            #Call the create_account method to create the account
            account = create_account_service.create_account(account_data)
            self.data_ops.save_data("data_file.yaml", account)

            # Display success notification
            self.display_notification("Account created successfully.")
            messagebox.showinfo("Success", "Account created successfully.")

        except ValueError as e:
            # Handle validation error
            self.display_notification(f"Validation Error: {e}")
            messagebox.showerror("Error", f"Validation Error: {e}")
        except AttributeError as e:
            # Handle attribute error
            self.display_notification(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
        except AccountCreationError as e:
            self.display_notification(f"An error occurred preventing account creation: {e}")
            messagebox.showerror("Error", f"An error occurred preventing account creation: {e}")
        except Exception as e:
            # Handle other errors
            self.display_notification(f"Error creating account: {e}")
            messagebox.showerror("Error", f"Error creating account: {e}")


        # Method to display notifications
    def display_notification(self, message):
        self.notification_text.config(state=tk.NORMAL) #Enable the widget to be edited
        self.notification_text.insert(tk.END, f"{message}\n") #insert message
        self.notification_text.config(state=tk.DISABLED) #Disable the widget from modification after inserting the message
        self.notification_text.see(tk.END)


    def setup_data_ops(self, filename: str):
        data_ops = DataOps(filename, [])
        # Load data when the app opens
        data_ops.load_data(filename)
        return data_ops

    def load_customer_data(self, account_number: str | None = None):
        """
        Loads customer data from the YAML file.

        Args:
            account_number (str | None): Optional account number to filter loaded data.

        Raises:
            FileNotFoundError: If the data file is not found.
            YAMLError: If the YAML format is invalid.
            ValueError: If invalid account number is provided.
        """
        self.data_ops.load_data("data_file.yaml")

        if account_number is not None:
            # Filter customer data by account number
            filtered_customers = [
                customer for customer in self.data_ops.bank_customers
                if customer.account_number == account_number
            ]

            if not filtered_customers:
                raise InvalidAccountNumberError (
                    f"Customer with account number '{account_number}' not found."
                )

            self.data_ops.bank_customers = filtered_customers
            print(f"Loaded data for customer with account number '{account_number}'.")
            return filtered_customers[0]  # Return the first customer in the filtered list

        else:
            print(f"Loaded data for all customers.")
            return self.data_ops.bank_customers  # Return all customers if no account number is provided

    def select_customer(self):

        try:
            account_number = self.entry_account_number.get()

            if not account_number:
                raise InvalidAccountNumberError("Please enter a valid account number")

            if account_number:
                selection_succesful = self.data_ops.select_customer_by_account_number(account_number)

                if selection_succesful:
                    messagebox.showinfo("Success", f"Customer with account number {account_number} has been successfully selected")
                    self.display_notification(F"Success ,Customer with account number {account_number} has been successfully selected")
                else:
                    self.display_notification("Something went wrong while Selecting Account. Default Account selected")
                    messagebox.showerror("Error", f"Account selection failed. Default Account selected!")
                    self.entry_account_number.delete(0, tk.END)

        except TypeError as e:
            self.display_notification(f"Error: {e}")
        except InvalidAccountNumberError:
            self.display_notification("Error, Invalid account number entered")
        except Exception as e:
            self.display_notification(f"Error: account selection failed. {e}")


    def withdraw_cash(self):
        try:
            amount = float(self.entry_amount.get())
            customer_id = self.entry_customer_id.get()

            if not customer_id:
                raise ValueError("Please enter a valid customer ID.")
                messagebox.showerror("Error", f"Please enter a valid customer id(PIN) to proceed!")

            if not amount:
                raise ValueError("Please enter a valid amount.")
                messagebox.showerror("Error", f"Please enter a valid amount to proceed!" )

            if self.data_ops.selected_customer:
                withdraw_successful = self.data_ops.selected_customer.withdraw(amount, customer_id)

                if withdraw_successful:
                    self.display_notification(f"Success: Withdrawal of {amount} was successful")
                    messagebox.showinfo("Success", f"Withdrawal of {amount} was successful")
                    self.update_gui()

                else:
                    self.display_notification("Error: Withdrawal failed.")
                    messagebox.showerror("Error", f"Withdrawal of {amount} was unsuccessful!")
                    # Clear input fields
                    # self.entry_amount.delete(0, tk.END)
                    # self.entry_customer_id.delete(0, tk.END)
            else:
                self.display_notification("No customer selected.")
        except ValueError:
            self.display_notification("Error: Invalid amount entered.")
        except Exception as e:
            self.display_notification(f"Error: Withdrawal failed. {e}")


    def deposit_cash(self):
        try:
            amount = float(self.entry_amount.get())
            customer_id = self.entry_customer_id.get()

            if not customer_id:
                raise ValueError("Please enter a valid customer ID.")

            if not amount:
                raise ValueError("Please enter a valid amount.")

            if self.data_ops.selected_customer:
                deposit_succesful = self.data_ops.selected_customer.deposit(amount, customer_id)
                if deposit_succesful:
                    self.display_notification(f"Success: Deposit of {amount} was successful")
                    messagebox.showinfo("Success", f"Deposit of {amount} was successful")
                    self.update_gui()
                else:
                    self.display_notification("Error: Deposit failed")
                    messagebox.showerror("Error", f"Deposit of {amount} was unsuccessful")
                    # Clear input fields
                    self.entry_amount.delete(0, tk.END)
                    self.entry_customer_id.delete(0, tk.END)
            else:
                self.display_notification("No customer found")

        except ValueError as e:
            self.display_notification(f"Error: Invalid amount entered {e}")
        except Exception as e:
            self.display_notification(f"Error: Deposit failed. {e}")
            print(f"Error, deposit failed {e}")


    def check_balance(self):
        try:
            customer_id = self.entry_customer_id.get()
            account_number = self.entry_account_number.get()

            if not customer_id:
                raise ValueError("Please enter a valid customer ID.")

            if not account_number:
                raise ValueError("Please enter a valid account_number.")

            if not self.data_ops.selected_customer:
                raise ValueError("Please select a customer first.")

            self.data_ops.selected_customer.check_balance(customer_id, account_number)
            messagebox.showinfo("Account Balance", f"Dear {self.selected_customer.customer_name} your acount balance is ${self.selected_customer.default_balance}.")
            self.update_gui()
        except ValueError:
            self.display_notification("Error: Invalid input. Please try again.")
        except Exception as e:
            self.display_notification(f"Error: Check balance failed. {e}")

    def show_transactions(self):
        try:
            customer_id = self.entry_customer_id.get()
            account_number = self.entry_account_number.get()

            if not customer_id:
                raise ValueError("Please enter a valid customer ID.")

            if not account_number:
                raise ValueError("Please enter a valid account_number amount.")

            if not self.data_ops.selected_customer:
                raise ValueError("Please select a customer first.")
            self.data_ops.selected_customer.transactions(customer_id, account_number)
        except ValueError as e:
            self.display_notification(f"Error: Invalid input for transactions: {e}")
        except TypeError as e:
            self.display_notification(f"Error: {e}")

    def set_budget(self):
        try:
            customer_id = self.entry_customer_id.get()
            limit = self.entry_budget_limit.get()

            if not customer_id:
                raise ValueError("Please enter a valid customer ID.")

            if not limit:
                raise ValueError("Please enter a valid limit amount.")

            if not self.data_ops.selected_customer:
                raise ValueError("Please select a customer before setting budget.")

            self.data_ops.selected_customer.set_budget(limit, customer_id)

        except ValueError as e:
            self.display_notification(f"Error: Invalid input for set budget: {e}")
        except TypeError as e:
            self.display_notification(f"Error: {e}")


    def spend_budget(self):
        pass


    def set_threshold(self):
        try:
            customer_id = self.entry_customer_id.get()
            threshold = self.entry_set_threshold.get()

            if not customer_id:
                raise ValueError("Please enter a valid customer ID.")

            if not threshold:
                raise ValueError("Please enter a valid threshold amount.")

            if not self.data_ops.selected_customer:
                raise ValueError("Please select a customer before setting a threshold.")

            self.data_ops.selected_customer.set_threshold(threshold, customer_id)
            self.display_notification(f"Threshold successfully set for customer {customer_id}.")
        except ValueError as e:
            self.display_notification(f"Error setting threshold: {e}")
        except TypeError as e:
            self.display_notification(f"Unexpected error occurred: {e}")


    def update_gui(self):
        if self.data_ops.selected_customer:
            label_customer_name.config(text=f"Customer's Name:{self.data_ops.selected_customer.customer_name}")
            label_customer_id.config(text=f"Customer's Name: {self.data_ops.selected_customer.customer_id}")

            # Loop through selected customer's accounts
            for account in self.selected_customer.accounts:
                interface.label_balance.config(text=f"Current Balance: ${self.data_ops.selected_customer.account_balance:.2f}")
        else:
            # Handle no customer selected case
            self.display_notification("No customer selected")


    def clear_data(self):
        try:
            customer_id = self.entry_customer_id.get()

            if not customer_id:
                raise ValueError("Please enter a valid customer ID.")

            if not self.data_ops.selected_customer:
                raise ValueError("Please select a customer first.")

            # Prompt user for confirmation
            confirmation = messagebox.askokcancel("Clear Account Data", "Are you sure you want to clear all account data? This action is permanent and cannot be undone.")

            if not confirmation:
                return

            if confirmation:
                self.data_ops.selected_customer.clear_data(customer_id)
                self.display_notification("Contents of the data file have been successfully removed")
                messagebox.showinfo("Contents of the data file have been successfully removed")

        except TypeError as e:
            messagebox.showerror("Error", e)
        except ValueError as e:
            messagebox.showerror("Error", e)
        except Exception as e:
            messagebox.showerror("Error", e)


    # save the account data when the application is closed
    def on_closing(self):
        #self.data_ops.save_data()
        self.master.destroy()




class AccountTransactions(BankAccount):
    """
       Responsible for encapsulating the logic for account transactions. It inherits from the BankAccount class in the Alpha module.

      Attributes:
                data_ops (DataOps): Object providing data access operations.
                interface (InterfaceBank): Object responsible for interface updates.

    Methods:
        withdraw(amount, customer_id): Allows a withdrawal from the current account, raising exceptions for insufficient funds, invalid amounts, or incorrect customer ID.
        deposit(amount, customer_id): Allows a deposit to the current account, raising exceptions for invalid amounts or incorrect customer ID.
        check_balance(customer_id, account_number): Verifies the account number and customer ID before retrieving and displaying the current account balance.
        transactions(customer_id, account_number): Retrieves and displays the transaction history for the specified customer account.
    """

    def __init__(self, account_number, account_holder, customer_id, default_balance, data_ops: DataOps, interface: InterfaceBank):
        super().__init__(account_number, account_holder, customer_id, default_balance)
        self.data_ops = data_ops
        self.interface = interface


    def withdraw(self, amount, customer_id):
        """
        Performs a withdrawal from the current account, raising exceptions for various error conditions.

        Args:
            amount (float): The amount to withdraw.
            customer_id (str): The customer ID associated with the account.

        Returns:
            boolean: True if the withdrawal is successful, False otherwise.

        Raises:
            ValueError: If the amount is not a valid number.
            TypeError: If the customer ID is not a string.
            InsufficientFundsError: If the account balance is insufficient for the withdrawal.
            InvalidWithdrawalAmountError: If the withdrawal amount is less than $1.
            InvalidCustomerIDError: If the provided customer ID does not match the current customer.
        """

        try:
            amount = float(amount)

            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if amount > self.data_ops.selected_customer.account_balance:
                raise InsufficientFundsError("Insufficient funds to proceed to withdrawal.")

            if amount < 1:
                raise InvalidWithrawalAmountError("Invalid withdrawal amount. Please enter a valid number.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Invalid customer ID.")

            self.account_balance -= amount
            self.transaction_history.append({"Type of transaction": "withdrawal", "Amount withdrawn": amount})
            self.interface.display_notification(f"{amount} was successfully withdrawn")
            messagebox.showinfo("Success", f"Withdrawal of ${amount} was successful. Your new account balance is {self.account_balance}")
            return True

        except ValueError:
            messagebox.showerror("Error", "Invalid withdrawal amount. Please enter a valid number.")
            return False
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            return False
        except InsufficientFundsError as e:
            messagebox.showerror("Error", e.message)
            print("Insufficient funds to proceed to withdrawal")
            return False
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            return False
        except InvalidWithrawalAmountError as e:
            messagebox.showerror("Error", e.message)
            return False

    def deposit(self, amount, customer_id):
        """
        Deposits funds to the current account, raising exceptions for various error conditions.

        Args:
            amount (float): The amount to deposit.
            customer_id (str): The customer ID associated with the account.

        Returns:
            boolean: True if the deposit is successful, False otherwise.

        Raises:
            ValueError: If the amount is not a valid number.
            TypeError: If the customer ID is not a string.
            InvalidDepositAmountError: If the deposit amount is less than 1.
            InvalidCustomerIDError: If the provided customer ID does not match the current customer.
        """
        try:
            amount = float(amount)
            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if amount < 1:
                raise InvalidDepositAmountError(f"Minimum deposit amount is ${1}.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Invalid customer ID.")


            self.account_balance += amount
            self.transaction_history.append({"Type of transaction": "deposit", "Amount withdrawn": amount})
            self.interface.display_notification(f"Withdrawal of {amount} was successful")
            messagebox.showinfo("Success", f"Deposit of ${amount} was successful. Your new account balance is ${self.account_balance}")
            return True
        except ValueError:
            messagebox.showerror("Error", "Invalid deposit amount. Please enter a valid number.")
            return False
        except TypeError as e:
            messagebox.showerror("Error", e)
            return False
        except InvalidDepositAmountError as e:
            messagebox.showerror("Error", e.message)
            return False
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            return False

    def check_balance(self, customer_id, account_number):

        """
        Verifies the account number and customer ID before retrieving and displaying the current account balance.

        Args:
            customer_id (str): The customer ID associated with the account.
            account_number (str): The account number to verify.

        Returns:
            boolean: True if the balance retrieval is successful, False otherwise.

        Raises:
            ValueError: If any input is invalid.
            TypeError: If the customer ID or account number is not a string.
            InvalidCustomerIDError: If the provided customer ID does not match the current customer.
            InvalidAccountNumberError: If the provided account number does not match the current account.
        """
        try:
            if not isinstance(account_number, str):
                raise TypeError("Customer account number must be a string.")

            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Error. You entered a wrong PIN")

            if account_number != self.data_ops.selected_customer.account_number:
                raise InvalidAccountNumberError(f"Error. You entered an invalid account number")

            # Retrieve and display balance
            current_balance = self.data_ops.selected_customer.account_balance
            self.interface.display_notification(f"Your current account balance is ${current_balance}.")
            messagebox.showinfo(f"Your current account balance is ${current_balance}.")
            return True

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please try again.")
            return False
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            return False
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            return False
        except InvalidAccountNumberError as e:
            messagebox.showerror("Error", e.message)
            return False

    def transactions(self, customer_id, account_number):
        """
        Retrieves and displays the transaction history for the specified customer account.

        Args:
            customer_id (str): The customer ID associated with the account.
            account_number (str): The account number to verify.

        Returns:
            formatted_transactions

        Raises:
            ValueError: If any input is invalid.
            TypeError: If the customer ID or account number is not a string.
            InvalidCustomerIDError: If the provided customer ID does not match the current customer.
            InvalidAccountNumberError: If the provided account number does not match the current account.
            Exception: Any other unexpected exception encountered.
        """
        try:
            if not isinstance(account_number, str):
                raise TypeError("Customer account number must be a string.")

            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Error. You entered a wrong PIN")

            if account_number != self.data_ops.selected_customer.account_number:
                raise InvalidAccountNumberError(f"Error. You entered an invalid account number")

            transactions =  self.data_ops.selected_customer.get_transaction_history()
            if transactions:

                formatted_transactions = "\n".join(str(transaction) for transaction in transactions)
                messagebox.showinfo("Transactions", f"{self.data_ops.selected_customer.account_holder}'s transaction history:\n{formatted_transactions}")
                return formatted_transactions

            else:
                # Handle the case where there are no transactions
                messagebox.showinfo("Transactions", f"{self.data_ops.selected_customer.account_holder}'s transaction history is empty.")
                return ""

        # Handle specific exceptions with custom messages
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input for transaction history: {e}")
        except TypeError as e:
            messagebox.showerror("Error", str(e))
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
        except InvalidAccountNumberError as e:
            messagebox.showerror(f"Error", e.message)
        except Exception as e:
            messagebox.showerror(f"Error", {e})

class BudgetActions:
    def __init__(self, data_ops: DataOps, bank_account: BankAccount ):
        """
        Manages budget-related actions for customer accounts.

        This class encapsulates the logic for setting, managing, and interacting with budget categories and limits, as well as setting account thresholds for notifications and alerts.

        It relies on instances of the `DataOps` class for data access and storage, and the `BankAccount` class for account-specific operations.

        Attributes:
            * bank_account: An instance of the `BankAccount` class representing the active account.
            * data_ops: An instance of the `DataOps` class for data access and manipulation.

        Raises:
            * `TypeError`: If invalid data types are provided (e.g., non-string customer ID).
            * `InvalidBudgetLimitError`: If invalid budget limit values are invalid (e.g., negative values).
            * `BudgetCategoryAlreadyExistsError`: If a duplicate budget category is set.
            * `BudgetCategoryNotFoundError`: If a requested category does not exist.
            * `InvalidThresholdError`: If an invalid threshold value is set (e.g., less than $1).
            * `InvalidCustomerIDError`: If an incorrect customer ID is provided.
        """
        self.bank_account = bank_account
        self.data_ops = data_ops

    def set_budget_category(self, category, limit, customer_id):
        """
        Sets a budget limit for a specific spending category.

        Args:
            category (str): The name of the spending category.
            limit (float): The maximum amount allowed to be spent in the category.
            customer_id(str): Customer's secret identifier(PIN)
        Raises:
            TypeError: If the customer ID is not a string.
            InvalidBudgetLimitError: If the budget limit is not a valid number or negative.
            BudgetCategoryAlreadyExistsError: If the category already exists.
        """
        try:
            limit = float(limit)
        except ValueError:
            raise InvalidBudgetLimitError("Budget limit must be a valid number.")

        try:
            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if limit < 0:
                raise InvalidBudgetLimitError("Budget limit cannot be a negative value.")

            if limit > self.data_ops.selected_customer.account_balance:
                raise InsufficientFundsError("Insufficient funds to proceed, budget limit cannot exceed current account balance.")

            if category in self.bank_account.budget_categories:
                raise BudgetCategoryAlreadyExistsError(f"Budget category '{category}' already has a limit set.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Invalid customer_id")


            self.bank_account.set_budget(category, limit)
            #self.bank_account.budget_categories[category] = limit #updating the dict with the new key-value pair(The set_budget method takes of this anyway)
            messagebox.showinfo("Success", f"Dear customer a budget category of {category} with a limit of ${limit} was successfully added to your budget categories")
            return True

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input : {e}")
            raise
            return False
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            raise
            return False
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            raise
            return False
        except InvalidBudgetLimitError as e:
            messagebox.showerror("Error", e.message)
            raise
            return False
        except BudgetCategoryAlreadyExistsError as e:
            messagebox.showerror("Error", e.message)
            raise
            return False
        except InsufficientFundsError as e:
            messagebox.showerror("Error", e.message)
            raise
            return False


    def get_budget_categories(self, customer_id):
        """
        Returns a dictionary of all budget categories and their limits.

        Args:
            customer_id(str): Customer secret identifier(PIN)

        Returns:
            dict: A dictionary where keys are category names and values are budget limits.
        Raises:
            TypeError: if the provided customer ID is not a string
        """
        try:
            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError("You entered the wrong Customer ID(PIN)")

            return self.bank_account.budget_categories
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            raise
            return False
        except WrongCustomerIdError as e:
            messagebox.showerror("Error", e.message)
            raise
            return False
        except Exception as e:
            messagebox.showerror("Error",e)
            raise

    def get_budget_category_limit(self, category, customer_id):
        """
        Returns the budget limit for a specific spending category.

        Args:
            category (str): The name of the spending category.
            customer_id(str): Customer secret identifier(PIN)

        Returns:
            float: The budget limit for the specified category.
        """
        try:
            if not isinstance(customer_id, str):
                raise TypeError("Invalid customer ID")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError("You entered the wrong Customer ID(PIN)")

            if category not in self.bank_account.budget_categories:
                raise BudgetCategoryNotFoundError(f"Budget category '{category}' not found.")

            return self.bank_account.budget_categories[category]

        except TypeError as e:
            messagebox.showerror("Error", str(e))
            raise
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            raise
        except WrongCustomerIdError as e:
            messagebox.showerror("Error", e.message)
            raise
        except BudgetCategoryNotFoundError as e:
            messagebox.showerror("Error", e.message)
            raise


    def update_budget_category_limit(self, category, new_limit, customer_id):
        """
        Updates the budget limit for a specific spending category.

        Args:
            category (str): The name of the spending category.
            new_limit (float): The new budget limit for the category.
            customer_id(str): customer secret identifier

        Raises:
            TypeError: if the provided customer ID is not a string.
            ValueError: if the new limit amount is not a float.
            InvalidThresholdError: If an invalid threshold value is set (e.g., less than $1).
            InvalidCustomerIDError: If an incorrect customer ID is provided.
        """
        try:
            new_limit = float(new_limit)
        except ValueError:
            raise InvalidBudgetLimitError("New budget limit must be a valid number.")

        try:
            if not isinstance(customer_id, str):
                raise TypeError ("Customer ID must be a string.")

            if new_limit < 1:
                raise InvalidBudgetLimitError (f"limit must be more than a ${1}")

            if new_limit > self.data_ops.selected_customer.account_balance:
                raise InsufficientFundsErro ("Insufficient funds to proceed, budget limit cannot exceed current account balance.")

            if new_limit < 0:
                raise InvalidBudgetLimitError ("New budget limit cannot be a negative value.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError ("Invalid Customer ID")

            if category not in self.bank_account.get_budget_categories:
                raise BudgetCategoryNotFoundError (f"Budget category '{category}' not found.")

            self.bank_account.budget_categories[category] = new_limit

        # Handle specific exceptions with custom messages
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input : {e}")
            raise
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            raise
        except BudgetCategoryNotFoundError as e:
            messagebox.showerror("Error", e.message)
            raise
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            raise
        except InvalidBudgetLimitError as e:
            messagebox.showerror("Error", e.message)
            raise
        except InsufficientFundsError as e:
            messagebox.showerror("Error", e.message)
            raise
        except Exception as e:
            messagebox.showerror("Error", e)


    def threshold(self, threshold, customer_id):
        """
        Sets the threshold amount for a customer's account.

        Args:
            threshold (float): The minimum account balance that triggers a notification.
            customer_id (str): The customer's unique identifier.

        Raises:
            TypeError: If the customer ID is not a string.
            InvalidThresholdError: If the threshold is invalid (less than 1 or more than account balance).
            InvalidCustomerIDError: If the customer ID is invalid.
        """
        try:
            threshold = float(threshold)
        except ValueError:
            raise InvalidThresholdError ("Threshold amount must be a valid number.")

        try:

            if not isinstance(customer_id, str):
                raise TypeError ("Customer ID must be a string.")

            if threshold < 1:
                raise InvalidThresholdError (f"Threshold must be more than a ${1}")

            if threshold > self.data_ops.selected_customer.account_balance:
                raise InsufficientFundsError(f"Threshold cannot be more than current account balance")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError ("Wrong Customer ID(PIN)")

            self.bank_account.set_threshold(threshold, customer_id)

        # Handle specific exceptions with custom messages
        except ValueError as e:
            messagebox.showerror("Error", e)
            raise
        except TypeError as e:
            messagebox.showerror("Error", str(e))
            raise
        except InvalidCustomerIDError as e:
            messagebox.showerror("Error", e.message)
            raise
        except InvalidThresholdError as e:
            messagebox.showerror("Error", e.message)
            raise
        except InsufficientFundsError as e:
            messagebox.showerror("Error", e.message)
            raise
        except WrongCustomerIdError as e:
            messagebox.showerror("Error", e.message)
            raise


class Extras:
    def __init__(self, data_ops: DataOps, bank_account: BankAccount ):

        self.data_ops = data_ops
        self.bank_account = bank_account

    def clear_data(self, customer_id):

        try:
            if not isinstance(customer_id, str):
                raise TypeError ("Customer ID must be a string.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError ("Cannot proceed to clear account data, You entered the wrong pin")

             # Open the file in write mode and write an empty JSON object
            with open("data_file.yaml", "w") as file:
                yaml.dump({}, file)
            messagebox.showinfo("The contents of the file have been deleted.")

        except TypeError as e:
            messagebox.showerror("Error", e)
            raise
        except WrongCustomerIdError as e:
            messagebox.showerror("Error", e)
            raise
        except Exception as e:
            messagebox.showerror("Error", e)









if __name__ == '__main__':
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='*.py')
    unittest.TextTestRunner().run(test_suite)


root = tk.Tk()

data_ops = DataOps(filename="data_file.yaml", bank_customers=[])

#bank_account =  BankAccount(account_number="", account_holder="", customer_id="", default_balance=0)

app = InterfaceBank(root, data_ops, CreateAccount, BankAccount)

root.protocol("WM_DELETE_WINDOW", app.on_closing)# Set up an event handler for when the application is closed

root.mainloop()











