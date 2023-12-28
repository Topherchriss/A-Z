"""
import os
import json
import tkinter as tk
from tkinter import messagebox
from Alpha import BankAccount
from Alpha import BankCustomer
from json_utils import save_bank_account_data, load_bank_account_data, save_bank_customer_data, load_bank_customer_data

class BankInterface:
    """
    """
    A graphical user interface for the A-Z TRAPEZA banking system.

    Methods:
        __init__(self, master: tk.Tk) -> None:
            Initialize the BankInterface.

        save_account_data(self) -> None:
            Save the BankAccount data to the JSON file.

        update_display(self) -> None:
            Update the GUI display based on the selected customer and account.

        switch_customer(self, customer: BankCustomer) -> None:
            Switch the selected customer and update the display.

        display_notification(self, message: str) -> None:
            Display notifications in the GUI.

        deposit_amount(self) -> None:
            Process a deposit transaction.

        withdraw_cash(self) -> None:
            Process a withdrawal transaction.

        check_balance(self) -> None:
            Check and display the account balance.

        show_transactions(self) -> None:
            Display the transaction history.

        set_budget(self) -> None:
            Set a budget for a specific spending category.

        spend_budget(self) -> None:
            Record an expense for a specific spending category.

        set_threshold(self) -> None:
            Set a threshold for the account balance.

        open_calc(self) -> None:
            Open a calculator window.

        clear_account_data(self) -> None:
            Clear the account data stored in the JSON file only with valid customer_id.

        on_closing(self) -> None:
            Save the account data before closing the application.
    """


    """


    def __init__(self, master):

        """
        Initialize the BankInterface.

        Parameters:
       #     master (tk.Tk): The master tkinter window.
        """

        self.master = master

        self.master.title("A-Z TRAPEZA")

        #Labels for Customer info:
        self.label_customer_name = tk.Label(master, text="Customer's Name:")
        self.label_account_number = tk.Label(master, text="Customer's account number:")
        self.label_amount = tk.Label(master, text="Amount:")
        self.label_customer_id = tk.Label(master, text="Enter your PIN:")
        self.label_budget_category = tk.Label(master, text="Budget Category:")
        self.label_budget_limit = tk.Label(master, text="Budget Limit:")
        self.label_balance = tk.Label(master, text="Current Balance: $0.00")
        self.label_set_threshold = tk.Label(master, text="Balance Threshold")


        #Entry fields
        self.entry_customer_name = tk.Entry(master)
        self.entry_account_number= tk.Entry(master)
        self.entry_amount = tk.Entry(master)
        self.entry_customer_id = tk.Entry(master)
        self.entry_budget_category = tk.Entry(master)
        self.entry_budget_limit = tk.Entry(master)
        self.entry_set_threshold = tk.Entry(master)


        #Buttons
        self.button_deposit = tk.Button(master, text="Deposit", command=self.deposit_amount)
        self.button_withdraw = tk.Button(master, text="Withdraw", command=self.withdraw_cash)
        self.button_transactions = tk.Button(master, text="Transactions", command=self.show_transactions)
        self.button_balance = tk.Button(master, text="Check Balance", command=self.check_balance)
        self.button_set_budget = tk.Button(master, text="Set Budget", command=self.set_budget)
        self.button_spend_budget = tk.Button(master, text="Spend Budget", command=self.spend_budget)
        self.button_calculator = tk.Button(master, text="Calculator", command=self.open_calc)
        self.button_set_threshold = tk.Button(master, text="Set Threshold", command=self.set_threshold)
        self.button_clear_json = tk.Button(master, text="Clear Data", command=self.clear_account_data)


        #Grid layout
        self.label_customer_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_customer_name.grid(row=0, column=1, padx=10, pady=10)
        self.label_account_number.grid(row=1, column=0, padx=10, pady=10)
        self.entry_account_number.grid(row=1, column=1, padx=10, pady=10)
        self.label_amount.grid(row=2, column=0, padx=10, pady=10)
        self.entry_amount.grid(row=2, column=1, padx=10, pady=10)
        self.label_customer_id.grid(row=3, column=0, padx=10, pady=10)
        self.entry_customer_id.grid(row=3, column=1, padx=10, pady=10 )
        self.button_deposit.grid(row=4, column=0, columnspan=2, pady=10)
        self.button_withdraw.grid(row=5, column=0, columnspan=2, pady=10)
        self.button_transactions.grid(row=6, column=0, columnspan=2, pady=10)
        self.button_balance.grid(row=7, column=0, columnspan=2, pady=10)
        self.label_balance.grid(row=8, column=0, columnspan=2, pady=10)
        self.label_set_threshold.grid(row=9, column=0, padx=10, pady=10)
        self.entry_set_threshold.grid(row=9, column=1, padx=10, pady=10)
        self.label_budget_category.grid(row=10, column=0, padx=10, pady=10)
        self.entry_budget_category.grid(row=10, column=1, padx=10, pady=10)
        self.label_budget_limit.grid(row=11, column=0, padx=10, pady=10)
        self.entry_budget_limit.grid(row=11, column=1, padx=10, pady=10)
        self.button_set_budget.grid(row=12, column=0, columnspan=2, pady=10)
        self.button_spend_budget.grid(row=12, column=1, columnspan=2, pady=10)
        self.button_set_threshold.grid(row=13, column=0, columnspan=2, pady=10)
        self.button_calculator.grid(row=13, column=1, columnspan=2, pady=10)
        self.button_clear_json.grid(row=14, column=1, columnspan=3, pady=10)


        self.notification_text = tk.Text(master, height=2, width=40)
        self.notification_text.grid(row=15, column=0, columnspan=2, pady=20)

        #Create Three customers
        self.customer1 = BankCustomer(customer_name="Jean Maswa")
        self.customer2 = BankCustomer(customer_name="Chachu Mulumba")
        self.customer3 = BankCustomer(customer_name="Zigi Zige")

        self.customer1_account = BankAccount(account_number="1000101", account_holder="Jean Maswa", customer_id="1456", default_balance=10000)
        save_bank_account_data(self.customer1_account, "account_data")
        self.customer2_account = BankAccount(account_number="1000102", account_holder="Chachu Mulumba", customer_id="2567",  default_balance=1500)
        save_bank_account_data(self.customer2_account, "account_data")
        self.customer3_account = BankAccount(account_number="1000103", account_holder="Zigi Zige", customer_id="3678", default_balance=2000)
        save_bank_account_data(self.customer3_account, "account_data")


        # Add accounts to customers
        self.customer1.addAccount(self.customer1_account)
        save_bank_customer_data(self.customer1, "customer_data.json")
        self.customer2.addAccount(self.customer2_account)
        save_bank_customer_data(self.customer2, "customer_data.json")
        self.customer3.addAccount(self.customer3_account)
        save_bank_customer_data(self.customer3, "customer_data.json")




        self.selected_customer = None
        self.selected_account = None
        self.account_data = {}

        """
         # Load account data from JSON file
         """
        try:
            self.account_data = load_bank_account_data("account_data.json")
            print("JSON here i come")
        except InvalidJSONFormatError as e:
            print("Error loading account data:", e)
        print("Account data found proceeding to select account...")
        """
        # Load customer data from JSON file
        """
        try:
            self.customer_data = load_bank_customer_data("customer_data.json")
            print("JSON here I come")
        except Exception as e:
            print("Error loading customer data:", e)

        self.switch_customer("Jean Maswa")


        # Select the account based on the loaded data, or choose a default account
        default_customer = self.customer2_account  # Default to customer1_account if necessary
        self.selected_customer = self.customer_data
        print(f"Customer selected: {self.selected_account}")

        default_account = self.customer2  # Default to customer2 if necessary
        self.selected_account = self.selected_customer.accounts[0] if self.selected_customer.accounts else default_account

        print(f"Account selected:{self.selected_account}")


        self.update_display(self.selected_account)



    #def select_customer(self, customer):
        #try:
            #self.account_data = load_bank_account_data('account_data.json')
        #except FileNotFoundError:
            #print("No existing account data")


    # Method to save the BankAccount data to the JSON file
    def save_account_data(self, selected_account, file_path="account_data.json"):
        try:
            save_bank_account_data(self.selected_account, "account_data.json")
        except Exception as e:
            print(f"An error occurred while saving account data: {e}")


    #Methd to load account data
    def load_account_data(self, selected_account, account_data="account_data.json"):
        # Check if the JSON file exists
        if not os.path.exists('account_data.json'):
            print("Account data file not found.")
            return None

        try:
            if account_data:
                self.selected_account = account_data
                print(f"{self.selected_account}'s Account data loaded successfully")
            else:
                print("No account data found")
        except Exception as e:
            print(f"An error occurred while loading account data: {e}")

    #Method to check is data exists and update if doesn't
    def check_and_save_data(self):
        # Load the saved account data from the JSON file
        saved_account_data = load_bank_account_data("account_data.json")

        # Compare the saved account data with the current selected account
        if saved_account_data != self.selected_account:
            # Save the updated selected account data to the JSON file
            save_bank_account_data(self.selected_account, "account_data.json")
            print("Account data updated and saved successfully")


    def update_display(self, selected_account):

        if self.selected_account and isinstance(self.selected_account, dict):
            # Ensure that 'account_balance' is present in the selected account
            stored_balance = self.selected_account.get("account_balance", 0)

            # Calculate previous transactions
            previous_transactions = sum(
                entry.get("Amount deposited", 0) if entry.get("Type of transaction") == "Deposit"
                else -entry.get("Amount withdrawn", 0)
                for entry in self.selected_account.get("transaction_history", [])
            )

            # Calculate total balance
            total_balance = stored_balance + previous_transactions

            # Update display elements with valid data
            self.label_customer_name.config(text=f"Customer's Name: {self.selected_account.get('account_holder', '')}")
            self.label_account_number.config(text=f"Customer's account number: {self.selected_account.get('account_number', '')}")
            self.label_balance.config(text=f"Current Balance: ${total_balance:.2f}")


        else:
            # Display error message if account data is not found
            print("No account data found")


    def switch_customer(self, customer_name):
    # Find the desired customer in the loaded customer data
        desired_customer = self.customer_data

        if desired_customer:
            # Set the selected customer and account
            self.selected_customer = desired_customer
            # Load account data for the selected customer
            self.account_data = self.load_account_data("account_data.json")

            self.selected_account = self.account_data


            # Update the display
            self.update_display(self.selected_account)
        else:
            print(f"Customer '{customer_name}' not found.")



    # Method to display notifications
    def display_notification(self, message):
        self.notification_text.config(state=tk.NORMAL) #Enable the widget to be edited
        self.notification_text.insert(tk.END, f"{message}\n") #insert message
        self.notification_text.config(state=tk.DISABLED) #Disable the widget from modification after inserting the message
        self.notification_text.see(tk.END)


    # Method to deposit
    def deposit_amount(self):
        customer_name = self.entry_customer_name.get()
        account_number = self.entry_account_number.get()
        customer_id = self.entry_customer_id.get()
        amount = float(0.0)  # Initialize with a default value

        #Validate input
        try:
            get_amount = float(self.entry_amount.get())
        except ValueError:
            messagebox.showerror("Invalid amount", f"Amount must be a numeric figure more than 10 dollars")

        if customer_name != self.selected_account.account_holder or account_number != self.selected_account.account_number:
            messagebox.showerror("Unsuccessful", f"Cannot proceed to deposit, Customer not found!")

        elif customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong Pin", "Cannot proceed to deposit. You entered a wrong Pin!")


        elif get_amount < 10:
            messagebox.showerror("Unsuccessful", f"Deposit of ${get_amount} is below the minimum (USD 10)")

            self.entry_customer_id.delete(0, 'end')

        else:
            self.selected_account.deposit(get_amount)

            self.label_balance.config(text=f"Current Balance: ${self.selected_account.account_balance:.2f}") #Update the GUI after every transaction

            if get_amount >= 50000:
                self.display_notification(f"A large deposit of ${get_amount} was made to your account.") #Notify the user of large deposit amounts

            messagebox.showinfo("Success", f"Deposit of ${get_amount} was succesful. New account balance: ${self.selected_account.account_balance}")

            self.check_and_save_data()
            self.save_account_data(self.selected_account, "account_data.json")
            save_bank_customer_data(self.selected_account, "customer_data.json")

            print("Deposit data saved")

            self.entry_customer_id.delete(0, 'end')

    # Method to withdraw
    def withdraw_cash(self):
        customer_name = self.entry_customer_name.get()
        account_number = self.entry_account_number.get()
        customer_id = self.entry_customer_id.get()
        try:
            amount = float(0.0)
            amount = float(self.entry_amount.get())
            threshold = float(self.entry_set_threshold.get()) if self.entry_set_threshold.get() else 0.0
        except ValueError:
            messagebox.showerror("Invalid", "Invalid Threshold amount")
            return

        try:
            amount = float(self.entry_amount.get())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid numeric amount to withdraw.")


        if customer_name != self.selected_account.account_holder or account_number != self.selected_account.account_number:
            messagebox.showerror("Unsuccessful", f"Cannot proceed to withdrawal, Customer not found!")

        elif amount > self.selected_account.account_balance:
            messagebox.showerror("Invalid Withdrawal", f"Cannot withdraw ${amount} it excedes your balance of ${self.selected_account.account_balance}")

        elif customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong Pin", "Cannot proceed to withdrawal. You entered a wrong!")

        elif amount < 10:
            messagebox.showerror("Invalid Amount", f"Cannot proceed to withdrawal. Withdrawal amount of ${amount} is below USD 10")

            self.entry_customer_id.delete(0, 'end')

        else:
            self.selected_account.withdraw(amount)

            self.label_balance.config(text=f"Current Balance: ${self.selected_account.account_balance:.2f}") #Update the GUI after every transaction

            if amount >= 5000:
                self.display_notification(f" A large amount of ${amount} was successfully withdrawn from your account.") #Inform the customer of large withdrawls from their account

            if self.selected_account.account_balance <= threshold:
                self.display_notification(f"Warning!, Dear {self.selected_account.account_holder} your account balance is bellow ${threshold}")

            messagebox.showinfo("Success", f"Withdrawal of ${amount} was a success. Your new account balance is: ${self.selected_account.account_balance}")

            self.save_account_data(self.selected_account, "account_data.json")
            self.entry_customer_id.delete(0, 'end')


    # Method to check balance
    def check_balance(self):
        customer_name = self.entry_customer_name.get()
        account_number = self.entry_account_number.get()
        customer_id = self.entry_customer_id.get()

        if customer_name != self.selected_account.account_holder or account_number != self.selected_account.account_number:
            messagebox.showerror("Invalid Customer", "Customer not found!")

        elif customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong Pin", "Cannot proceed to check balance. You entered a wrong Pin")

            self.entry_customer_id.delete(0, 'end')

        else:
            self.selected_account.checkBalance()
            messagebox.showinfo("Account Balance", f"Dear {customer_name}, your current account balance is: ${self.selected_account.account_balance}")

            self.entry_customer_id.delete(0, 'end')

    # Method to display transactions
    def show_transactions(self):
        customer_name = self.entry_customer_name.get()
        account_number = self.entry_account_number.get()
        customer_id = self.entry_customer_id.get()

        if customer_name != self.selected_account.account_holder or account_number != self.selected_account.account_number:
            messagebox.showerror("Invalid Customer", "Customer not found!")


        elif customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong Pin", f"Cannot proceed to show account transaction You entered a wrong pin!")

            self.entry_customer_id.delete(0, 'end')

        else:
            transaction_history = self.selected_account.get_transaction_history()
            if transaction_history: #check the case where there are transactions
                formatted_transactions = "\n".join(str(transaction) for transaction in transaction_history)
                messagebox.showinfo("Transactions", f"{customer_name}'s transaction history:\n{formatted_transactions}")
                self.save_account_data()
                print("Transaction saved")
            else: #check the case where there are no transactions
                messagebox.showinfo("Transactions", "No transactions available so far.")
                self.entry_customer_id.delete(0, 'end')

    def set_budget(self):
        customer_id = self.entry_customer_id.get()
        category = self.entry_budget_category.get()
        try:
            limit = float(self.entry_budget_limit.get())
        except ValueError:
            messagebox.showerror("Error", "Cannot proceed.Invalid limit amount!")
            return

        if customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong Pin", f"Cannot proceed to set budget category. You entered a wrong pin!")

        elif limit < 1 or limit > self.selected_account.account_balance or limit == '':
            messagebox.showerror("Unsuccessful", f"Invalid limit input ${limit}!")

        else:
            self.selected_account.set_budget(category, limit)
            messagebox.showinfo("Success", f"Dear {self.selected_account.account_holder} a budget category of {category} with a limit of ${limit} was added on your acccount. Thank you for keeping it A-Z!")
            self.save_account_data(self.selected_account, "account_data.json")
            print("Budget Set")
            self.entry_customer_id.delete(0, 'end')

    def spend_budget(self):
        category = self.entry_budget_category.get()
        customer_id = self.entry_customer_id.get()
        amount = 0.0

        try:
            amount = float(self.entry_amount.get())
        except ValueError:
            messagebox.showerror("Invalid", "Invalid amount!")
            return


        if customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong PIN", "Cannot proceed. You entered the wrong PIN")

        elif category not in self.selected_account.budget_categories:
            messagebox.showerror("Error", f"Cannot proceed, category {category} not found!")

        elif amount < 10:
            messagebox.showerror("Error", f"Cannot proceed, amount ${amount} must be more than or equal to $10")


        else:
            limit = self.selected_account.budget_categories.get(category, 0.0) # Use the limit associated with the category

            # Check if the category exists in cumulative_expenses, if not, initialize it
            if category not in self.selected_account.cumulative_expenses:
                self.selected_account.cumulative_expenses[category] = 0

            elif category == "":
                messagebox.showerror("Invalid", "Please provide a descriptive name for your budget!")

            elif amount + self.selected_account.cumulative_expenses[category] > limit:
                messagebox.showerror("Warning", "Exceeding budget limit")

            elif amount > limit:
                messagebox.showerror("Error", f"Dear {self.selected_account.account_holder} ${amount} exceeds budget allocation of ${limit}")

            else:
                self.selected_account.get_expense(category, amount)
                messagebox.showinfo("Success", f"Dear {self.selected_account.account_holder}, you have spent ${amount} from {category} budget. Your budget limit for {category} is at ${limit}")

                self.label_balance.config(text=f"Current Balance: ${self.selected_account.account_balance:.2f}") #Update the GUI after every transaction

                self.save_account_data(self.selected_account, "account_data.json")
                print("Budget expinditure")
                self.entry_customer_id.delete(0, 'end')


    def set_threshold(self):
        customer_id = self.entry_customer_id.get()
        threshold = 0.0
        try:
            threshold = float(self.entry_set_threshold.get())
        except ValueError:
            messagebox.showerror("Invalid", "Cannot proceed to set threshold. You entered an invalid threshold amount")
            return


        if customer_id != self.selected_account.customer_id or customer_id == '':
            messagebox.showerror("Wrong PIN", "Cannot proceed to set threshold. You entered a wrong pin")

        elif threshold < 0:
            messagebox.showerror("Invalid", f"Cannot proceed to set threshold of {threshold}")

        elif threshold > self.selected_account.account_balance:
            messagebox.showerror("Invalid", f"Cannot proceed ro set threshold. Threshold must be less than current account balance!")

        else:
            self.selected_account.set_threshold(threshold)
            messagebox.showinfo("succesful", f"Dear {self.selected_account.account_holder} a threshold of ${threshold} was set for account {self.selected_account.account_number}. Thank you for keeping it A-Z")
            self.save_account_data(self.selected_account, "account_data.json")

    def open_calc(self):
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

        Used the eval() function for simplicty but can as well as implement the Calculator class from Extras and express it using the logic below

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


    def clear_account_data(self):

            # Get the PIN entered by the user
        entered_pin = self.entry_customer_id.get() if self.entry_customer_id.get() else None

        if entered_pin ==  '':
            messagebox.showerror("Invalid", "Cannot proceed to delete data. You entered an invalid PIN.")

        # Check if the entered PIN matches the account's PIN
        elif entered_pin != self.selected_account.customer_id:
            messagebox.showerror("Wrong PIN", "Cannot proceed to delete data. You entered the wrong PIN.")

        else:
            if entered_pin == self.selected_account.customer_id:
                # Prompt user for confirmation
                confirmation = messagebox.askokcancel("Clear Account Data", "Are you sure you want to clear all account data? This action is permanent and cannot be undone.")

                if not confirmation:
                    return
                else:
                    try:
                        # Open the file in write mode and write an empty JSON object
                        with open("account_data.json", "w") as file:
                            json.dump({}, file)
                        self.display_notification("The contents of the file have been deleted.")
                    except Exception as e:
                        self.display_notification(f"An error occurred: {e}")
            else:
                messagebox.showerror("Error", "Unexpected error occurred.Please try again later")



    # save the account data when the application is closed
    def on_closing(self):
        # Save the account data before closing the application
        print("Closing application...")

        self.save_account_data(self.selected_account, "account_data.json")

        print("saved data:", self.save_account_data)
        print("Account data saved. Destroying the window.")

        self.master.destroy()






import tkinter as tk
from Alpha import BankAccount, BankCustomer

class InterfaceBank:
    # ... (other methods and attributes)

    def create_account_window(self):
        # Create a new window for creating accounts
        account_window = tk.Toplevel(self.master)
        account_window.title("Create Account")

        # Labels for account creation
        label_account_number = tk.Label(account_window, text="Account Number:")
        label_account_holder = tk.Label(account_window, text="Account Holder:")
        label_customer_id = tk.Label(account_window, text="Customer ID:")
        label_default_balance = tk.Label(account_window, text="Default Balance:")

        # Entry fields for account creation
        entry_account_number = tk.Entry(account_window)
        entry_account_holder = tk.Entry(account_window)
        entry_customer_id = tk.Entry(account_window)
        entry_default_balance = tk.Entry(account_window)

        # Button to add the account
        button_add_account = tk.Button(account_window, text="Add Account",
                                       command=lambda: self.add_account(entry_account_number.get(),
                                                                         entry_account_holder.get(),
                                                                         entry_customer_id.get(),
                                                                         entry_default_balance.get(),
                                                                         account_window))

        # Grid layout for account creation window
        label_account_number.grid(row=0, column=0, padx=10, pady=10)
        entry_account_number.grid(row=0, column=1, padx=10, pady=10)
        label_account_holder.grid(row=1, column=0, padx=10, pady=10)
        entry_account_holder.grid(row=1, column=1, padx=10, pady=10)
        label_customer_id.grid(row=2, column=0, padx=10, pady=10)
        entry_customer_id.grid(row=2, column=1, padx=10, pady=10)
        label_default_balance.grid(row=3, column=0, padx=10, pady=10)
        entry_default_balance.grid(row=3, column=1, padx=10, pady=10)
        button_add_account.grid(row=4, column=0, columnspan=2, pady=10)

    def add_account(self, account_number, account_holder, customer_id, default_balance, account_window):
        # Validate the input data
        if not account_number or not account_holder or not customer_id or not default_balance:
            self.display_notification("All fields are required for account creation.")
            return

        # Create a new account data dictionary
        account_data = {
            "account_number": account_number,
            "account_holder": account_holder,
            "customer_id": customer_id,
            "account_balance": float(default_balance),  # Assuming default_balance is a float
        }

        # Create a new account and add it to the customer
        new_account = self.create_account(self.bank_customer, account_data)

        # Display notification
        self.display_notification(f"Account {account_number} created successfully.")

        # Close the account creation window
        account_window.destroy()

        In this example, create_account_window creates a new window with entry fields for account details and a button to add the account. The add_account method is called when the "Add Account" button is clicked, and it validates the input data, creates a new account, and adds it to the associated customer. The notification is updated accordingly.


        def save_data(self):

        def create_account_window(self):
        # Create a new window for creating accounts
        account_window = tk.Toplevel(self.master)
        account_window.title("Create Account")

        # Labels for account creation
        self.label_account_number = tk.Label(account_window, text="Account Number:")
        self.label_account_holder = tk.Label(account_window, text="Account Holder:")
        self.label_customer_id = tk.Label(account_window, text="Customer ID:")
        self.label_default_balance = tk.Label(account_window, text="Default Balance:")

                # Entry fields for account creation
        self.entry_account_number = tk.Entry(account_window)
        self.entry_account_holder = tk.Entry(account_window)
        self.entry_customer_id = tk.Entry(account_window)
        self.entry_default_balance = tk.Entry(account_window)

            # Button to add the account
        self.button_add_account = tk.Button(account_window, text="Add Account",
                                            command=lambda: self.add_account(entry_account_number.get(),
                                                                              entry_account_holder.get(),
                                                                              entry_customer_id.get(),
                                                                              entry_default_balance.get(),
                                                                              account_window))

        # Grid layout for account creation window
        self.label_account_number.grid(row=0, column=0, padx=10, pady=10)
        self.entry_account_number.grid(row=0, column=1, padx=10, pady=10)
        self.label_account_holder.grid(row=1, column=0, padx=10, pady=10)
        self.entry_account_holder.grid(row=1, column=1, padx=10, pady=10)
        self.label_customer_id.grid(row=2, column=0, padx=10, pady=10)
        self.entry_customer_id.grid(row=2, column=1, padx=10, pady=10)
        self.label_default_balance.grid(row=3, column=0, padx=10, pady=10)
        self.entry_default_balance.grid(row=3, column=1, padx=10, pady=10)
        self.button_add_account.grid(row=4, column=0, columnspan=2, pady=10)

    Saves the current customer data to the JSON file
    try:
      with open(self.filename, "w") as file:
        json_data = []
        for customer in self.bank_customers:
          json_data.append(customer.to_json())
        json.dump(json_data, file, indent=4)
        print("Account data saved")
    except Exception as e:
      print(f"Error saving data to {self.filename}: {e}")


      def to_json(self):
        # Convert transaction_history list to a dictionary
        transaction_history_dict = [
            {"Type of transaction": entry.get("Type of transaction", ""),
             "Amount": entry.get("Amount deposited", 0.0)}
            for entry in self.transaction_history
        ]

        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "customer_id": self.customer_id,
            "account_balance": self.account_balance,
            "transaction_history": transaction_history_dict,
            "budget_categories": self.budget_categories,
            "cumulative_expenses": self.cumulative_expenses,
            "threshold": self.threshold
        }

    @classmethod
    def from_json(cls, data):
        print("Data before creating instance:", data)

        # Initialize instance with default values
        instance = cls()

         # Check if instance is successfully initialized
        if instance:
            print("succesfully initialized")

        # Check if data is a dictionary
            if isinstance(data, dict):
                print("Data is a dictionary. Processing...")

                # Retrieve the transaction history and convert it back to a list
                transaction_history_list = [
                    {"Type of transaction": entry.get("Type of transaction", ""),
                    "Amount deposited": entry.get("Amount", 0.0)}
                    for entry in data.get("transaction_history", [])
                ]

                    # Update instance with data
                instance.account_number = data.get("account_number", "")
                instance.account_holder = data.get("account_holder", "")
                instance.customer_id = data.get("customer_id", "")
                instance.default_balance = data.get("account_balance", 0)
                instance.transaction_history = transaction_history_list
                instance.budget_categories = data.get("budget_categories", {})
                instance.cumulative_expenses = data.get("cumulative_expenses", {})
                instance.threshold = data.get("threshold", 0)

                print("Created instance:", instance)
            else:
                print("Invalid data format. Expected dictionary.")
        return instance

     """
"""    account_data = {
        "account_number": account_number,
        "account_holder": account_holder,
        "customer_id": customer_id,
        "account_balance": default_balance,
    }

    # Create and add account using CreateAccount object
    new_account = self.create_account(account_data)

    # Update data storage
    # ...

    # Display success message and close window
    self.display_notification(f"Account {account_number} created successfully.")
    account_window.destroy()






    def create_example_instance(self):
        #self.data_ops.bank_customers = []


        #Create a BankAccount instance
        test_bank_account_instance1 = BankAccount(account_number="111", account_holder="MIMI",   customer_id="1234", default_balance=900)
        test_bank_account_instance2 = BankAccount(account_number="222", account_holder="WEWE",   customer_id="12345", default_balance=800)
        test_bank_account_instance3 = BankAccount(account_number="333", account_holder="SISI",   customer_id="123456", default_balance=8000)

        # Create a BankCustomer instance
        customer_1 = BankCustomer(customer_name="MIMI", account_number="111", account_holder="MIMI", customer_id="1234", default_balance=900)

        customer_2 = BankCustomer(customer_name="WEWE", account_number="222", account_holder="WEWE", customer_id="12345", default_balance=800)

        customer_3 = BankCustomer(customer_name="SISI", account_number="333", account_holder="SISI", customer_id="123456", default_balance=8000)

        # Add the BankAccount to the BankCustomer
        customer_1.addAccount(test_bank_account_instance1)
        customer_2.addAccount(test_bank_account_instance2)
        customer_3.addAccount(test_bank_account_instance3)
        self.data_ops.save_data()

        # Update the DataOps instance with the BankCustomer
        self.data_ops.bank_customers.append(customer_1)
        self.data_ops.bank_customers.append(customer_2)
        self.data_ops.bank_customers.append(customer_3)
        print("Customers have been appended")
        self.data_ops.save_data()

        """
        # Select the customers
        """
        #self.data_ops.selected_customer = test_bank_account_instance
        print(f"LIST: {len(self.data_ops.bank_customers)}")
        self.data_ops.selected_customer = self.load_customer_data(account_number="1002")
        #self.data_ops.selected_customer= self.data_ops.select_customer_by_account_number(account_number="1002")
        print(f"Seleted customer: {self.data_ops.selected_customer}")

        # Deposit and withdraw operations
        self.data_ops.selected_customer.deposit(1000)
        self.data_ops.selected_customer.withdraw(600)
        self.data_ops.selected_customer.checkBalance()#(customer_id="1234", account_number="111")

        # Save data
        self.on_closing()
        """
        """
        data_ops = DataOps("customers.yaml", []) #create DataOps instance
        data_ops.load_data("customers.yaml") #Load data from the file
        all_customers = data_ops.get_all_customers()
        data_ops.select_customer_by_account_number(account_number="123456")
        data_ops.selected_customer.deposit(1000)
        data_ops.selected_customer.withdraw(80)
        data_ops.selected_customer.checkBalance()
        #self.selected_customer.show_transactions()
        #data_ops.select_customer(0) #Select first customer
        #new_customer = BankCustomer(customer_name="John", account_number="123456", account_holder="John Mufuwe", customer_id="7890", default_balance=1000)
        #data_ops.bank_customers.append(new_customer)
        #data_ops.save_data("customers.yaml", new_customer)

        self.setup_data_ops("customers.yaml")
        account_data = {
            "customer_name": "Chici",
            "account_number": "c12345v",
            "account_holder": "Icihc",
            "customer_id": "987",
            "default_balance": "400",
        }
        create_account_service = CreateAccount(self.data_ops, self.customer)
        account = create_account_service.create_account(account_data)
        self.data_ops.save_data("customers.yaml", self.data_ops.bank_customers)
        """
    """
class TestDataOpsSaveData(unittest.TestCase):

    def setUp(self):
        self.valid_data_file = "valid_data_file.yaml"
        self.test_save_data = "test_save_data.yaml"
        self.creat_account_service = CreateAccount()
        self.customer = Mock(spec=BankCustomer)
        self.data_ops = DataOps(self.test_save_data, bank_customers=[])
        self.create_account_service = CreateAccount(self.data_ops, self.customer)

    @patch("builtins.open", side_effect=lambda f, m: mock_open().return_value)
    @patch("yaml.safe_load",return_value=[])

    def test_save_data(self, mock_safe_load, mock_open):
        account_data = {
            "customer_name": "Mwalimu Daktari",
            "account_number": "12345",
            "account_holder": "Teacher Doctor",
            "customer_id": "1",
            "default_balance": 0.0,
        }
        customer = self.create_account_service.create_customer(account_data)
        self.data_ops.save_data(self.test_save_data, customer)

        # Verify the saved data
        with open(self.test_save_data, "r") as file:
            saved_data = yaml.safe_load(file)
            self.assertEqual(len(saved_data), 2)


class InterfaceBank:

    def __init__(self, master, data_ops: DataOps, bank_account: BankAccount, account_creation: CreateAccount):
        self.master = master
        self.master.title("A-Z TRAPEZA")
        self.data_ops = data_ops
        self.bank_account = bank_account
        self.account_creation = account_creation
        self.customer = None


        #Labels for Customer info:
        self.label_customer_name = tk.Label(master, text="Customer's Name:")
        self.label_account_number = tk.Label(master, text="Customer's account number:")
        self.label_amount = tk.Label(master, text="Amount:")
        self.label_customer_id = tk.Label(master, text="Enter your PIN:")
        self.label_budget_category = tk.Label(master, text="Budget Category:")
        self.label_budget_limit = tk.Label(master, text="Budget Limit:")
        self.label_balance = tk.Label(master, text="Current Balance: $0.00")
        self.label_set_threshold = tk.Label(master, text="Balance Threshold")


        #Entry fields
        self.entry_customer_name = tk.Entry(master)
        self.entry_account_number= tk.Entry(master)
        self.entry_amount = tk.Entry(master)
        self.entry_customer_id = tk.Entry(master)
        self.entry_budget_category = tk.Entry(master)
        self.entry_budget_limit = tk.Entry(master)
        self.entry_set_threshold = tk.Entry(master)


        #Buttons
        self.button_deposit = tk.Button(master, text="Deposit", command=self.deposit_cash)
        self.button_withdraw = tk.Button(master, text="Withdraw", command=self.withdraw_cash)
        self.button_transactions = tk.Button(master, text="Transactions", command=self.show_transactions)
        self.button_balance = tk.Button(master, text="Check Balance", command=self.check_balance)
        self.button_set_budget = tk.Button(master, text="Set Budget", command=self.set_budget)
        self.button_spend_budget = tk.Button(master, text="Spend Budget", command=self.spend_budget)
        self.button_select_customer = tk.Button(master, text="Select Customer", command=self.create_example_instance) #000
        self.button_set_threshold = tk.Button(master, text="Set Threshold", command=self.set_threshold)
        self.button_create_account = tk.Button(master, text="create account", command=self.create_account_window)


        #Grid layout
        self.label_customer_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_customer_name.grid(row=0, column=1, padx=10, pady=10)
        self.label_account_number.grid(row=1, column=0, padx=10, pady=10)
        self.entry_account_number.grid(row=1, column=1, padx=10, pady=10)
        self.label_amount.grid(row=2, column=0, padx=10, pady=10)
        self.entry_amount.grid(row=2, column=1, padx=10, pady=10)
        self.label_customer_id.grid(row=3, column=0, padx=10, pady=10)
        self.entry_customer_id.grid(row=3, column=1, padx=10, pady=10 )
        self.button_deposit.grid(row=4, column=0, columnspan=2, pady=10)
        self.button_withdraw.grid(row=5, column=0, columnspan=2, pady=10)
        self.button_transactions.grid(row=6, column=0, columnspan=2, pady=10)
        self.button_balance.grid(row=7, column=0, columnspan=2, pady=10)
        self.label_balance.grid(row=8, column=0, columnspan=2, pady=10)
        self.label_set_threshold.grid(row=9, column=0, padx=10, pady=10)
        self.entry_set_threshold.grid(row=9, column=1, padx=10, pady=10)
        self.label_budget_category.grid(row=10, column=0, padx=10, pady=10)
        self.entry_budget_category.grid(row=10, column=1, padx=10, pady=10)
        self.label_budget_limit.grid(row=11, column=0, padx=10, pady=10)
        self.entry_budget_limit.grid(row=11, column=1, padx=10, pady=10)
        self.button_set_budget.grid(row=12, column=0, columnspan=2, pady=10)
        self.button_spend_budget.grid(row=12, column=1, columnspan=2, pady=10)
        self.button_set_threshold.grid(row=13, column=0, columnspan=2, pady=10)
        self.button_select_customer.grid(row=13, column=1, columnspan=2, pady=10)
        #self.button_calculator.grid(row=13, column=1, columnspan=2, pady=10)
        self.button_create_account.grid(row=14, column=1, columnspan=3, pady=10)

        #Notification panel
        self.notification_text = tk.Text(master, height=2, width=40)
        self.notification_text.grid(row=15, column=0, columnspan=2, pady=20)
"""
"""
class InterfaceBank:

    def __init__(self, master, data_ops: DataOps, account_trans: AccountTransaction, account_creation: CreateAccount):
        self.master = master
        self.master.title("A-Z TRAPEZA")
        self.data_ops = data_ops
        self.account_trans = account_trans
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

        button_commands = [
            self.deposit_money,
            self.withdraw_money,
            self.set_budget,
            self.create_account_window,
            self.show_account_transactions,
            self.spend_budget,
            self.set_threshold,
            self.select_customer,
            self.check_account_balance,
            self.calculate,
            self.clear_data,
            self.on_closing
        ]

        self.button_widgets = [tk.Button(master, text=text, command=cmd, bg=accent_color, fg=ff_color)
                               for text, cmd in zip(button_texts, button_commands)]

        # Grid layout
        for i, label_widget in enumerate(self.label_widgets):
            label_widget.grid(row=i, column=0, padx=10, pady=10, sticky="e")
        for i, entry_widget in enumerate(entry_widgets):
            entry_widget.grid(row=i, column=1, padx=10, pady=10, sticky="w")
        for i, button_widget in enumerate(self.button_widgets):
            button_widget.grid(row=i, column=2, columnspan=2, pady=10)

        # Notification panel
        self.notification_text = tk.Text(master, height=2, width=40)
        self.notification_text.grid(row=len(label_texts) + 1, column=0, columnspan=6, pady=20)

        # Apply the background color to widgets
        for widget in self.label_widgets + self.button_widgets + [self.notification_text]:
            widget.configure(bg=tt_color, fg=ff_color)
    """
    """
    class AccountTransactions(BankAccount):


    def __init__(self, account_number, account_holder, customer_id, default_balance, data_ops: DataOps, interface: InterfaceBank):
        super().__init__(account_number, account_holder, customer_id, default_balance)
        self.data_ops = data_ops
        self.interface = interface


    def withdraw(self, amount, customer_id):

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

            if amount >= 5000:
                self.display_notification(f" A large amount of ${amount} was successfully withdrawn from your account.") #Inform the customer of large withdrawls from their account
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

        try:
            amount = float(amount)
            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if amount < 1:
                raise InvalidDepositAmountError(f"Minimum deposit amount is ${1}.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Invalid customer ID.")

            self.account_balance += amount
            if amount >= 50000:
                self.display_notification(f" A large amount of ${amount} was successfully deposit to your account.") #Inform the customer of large deposits from their account

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

        try:
            if not isinstance(account_number, str):
                raise TypeError("Customer account number must be a string.")

            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise InvalidCustomerIDError("Error. You entered a wrong PIN")

            if account_number != self.data_ops.selected_customer.account_number:
                raise InvalidAccountNumberError(f"Error. You entered an invalid account number")

            transactions =  self.data_ops.selected_customer.account_transactions(customer_id, account_number)
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

    def budget_spending(self, category, amount):

        try:
            amount = float(amount)
        except ValueError as e:
            print(f"Error amount value has to be a float {e}")

        if category not in self.budget_categories:
            print(f"Dear {self.account_holder} category: {category} not set!")
            return

        if amount > 0:
            self.account_balance -= amount

            #check aganist budget limit
            if amount > self.budget_categories[category]:
                print(f"Dear {self.account_holder} you have exceded your budget for {category}")

            self.transaction_history.append({"Type of transaction": "Expense", "Category": category, "Amount spent": amount})

            self.send_notification()
            print(f"Expense of {amount} from {category} was successful. Your new balance is {
                self.account_balance}")
        else:
            print(f"Invalid expense amount {amount}. Please insert a positive value")
            return


    def get_expense(self, category, amount):

        try:
            amount = float(amount)
        except ValueError as e:
            print(f"Error invalid amount {e}")

        if category not in self.budget_categories:
            print(f"Category '{category}' not found in budget.")
            return

        if category not in self.cumulative_expenses:
            self.cumulative_expenses[category] = 0

        limit = self.budget_categories[category]

        if amount + self.cumulative_expenses[category] > limit:
            print("Exceeding budget limit")
            return

        else:
            self.account_balance -= amount

            self.cumulative_expenses[category] += amount  # Increment cumulative expenses

            limit_after_spending = self.budget_categories[category] - amount
            self.budget_categories[category] -= amount

            print(f"You have succesfully spent {amount} form category {category} remainig ${limit_after_spending}")

            self.transaction_history.append({"Type of transaction": "Expense", "Category": category, "Amount spent": amount})
            self.send_notification()

            return limit_after_spending
    def send_notification(self):

        # Check for significant events
        if self.transaction_history:
            last_transaction = self.transaction_history[-1]

            #check for large deposit
            if last_transaction["Type of transaction"].lower() == "deposit" and last_transaction["Amount deposited"] >= 50000:
                print("Notification: A large deposit was made to your account.")

            #check or large withdrawals
            elif last_transaction["Type of transaction"].lower() == "withdrawal" and last_transaction["Amount withdrawn"] >= 5000:
                print("Notification: A large withdrawal was made from your account.")

        # Check balance threshold
        if self.account_balance <= self.threshold:
            print(f"Notification: Your account balance is below ${self.threshold}.")


import tkinter as tk
from tkinter import ttk

class InterfaceBank:

    def __init__(self, master, data_ops, bank_account, account_creation):
        self.master = master
        self.master.title("A-Z TRAPEZA")
        self.data_ops = data_ops
        self.bank_account = bank_account
        self.account_creation = account_creation
        self.customer = None

        # Setting a modern color scheme
        bg_color_window = "#4d3d08"
        bg_color = "#5d6134"
        accent_color = "#548ca8"
        highlight_color = "#D8BFD8"
        tt_color = "#4d3d08"
        ff_color = "#ebc81a"

        # Set a modern font
        font_style = ("Segoe UI", 12)

        # Master window background
        master.configure(bg=bg_color_window)

        # Labels for Customer info:
        label_texts = ["Account number:", "Amount:",
                       "Customer ID(PIN):", "Budget Category:", "Budget Limit:", "Threshold:"]
        self.label_widgets = [ttk.Label(master, text=text, font=font_style) for text in label_texts]

        # Entry fields
        entry_widgets = [ttk.Entry(master, font=font_style) for _ in range(len(label_texts))]
        self.entry_account_number, self.entry_amount, \
            self.entry_customer_id, self.entry_budget_category, \
            self.entry_budget_limit, self.entry_threshold, = entry_widgets

        # Buttons
        button_texts = ["Deposit", "Withdraw", "Set Budget", "Create Account",
                        "Select Customer", "Budget Limit", "Budget Categories", "Transactions", "Check Balance", "Calculate", "Spend Budget", "Set Threshold", "Clear Data", "Exit A-Z"]

        button_commands = [self.deposit_money, self.withdraw_money, self.set_budget,
                           self.create_account_window, self.select_customer, self.get_budget_category_limit,
                           self.budget_categories_dict, self.show_account_transactions, self.check_account_balance, self.calculate, self.spend_budget, self.set_threshold, self.clear_data, self.exit_az]

        self.button_widgets = [ttk.Button(master, text=text, command=cmd, style='Accent.TButton')
                               for text, cmd in zip(button_texts, button_commands)]

        # Adding a modern style
        style = ttk.Style()
        style.configure('Accent.TButton', background=accent_color, foreground=ff_color, font=font_style)

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
            widget.configure(style='Accent.TButton')

    def clear_data(self):
        # Implement clearing data logic
        pass

    def exit_az(self):
        self.master.destroy()

# Example usage:
root = tk.Tk()
app = InterfaceBank(root, data_ops, bank_account, account_creation)
root.mainloop()

def update_gui(self):
        if self.data_ops.selected_customer:
            # Display current balance
            interface.label_balance.config(text=f"Current Balance: ${self.data_ops.selected_customer.account_balance:.2f}")

            # Display threshold or initialize to $0.0 if not set
            threshold_text = f"Threshold: ${self.data_ops.selected_customer.threshold:.2f}" if hasattr(self.data_ops.selected_customer, 'threshold') else "Threshold: $0.0"
            self.label_threshold.config(text=threshold_text)
        else:
            # Handle no customer selected case
            self.display_notification("No customer selected")

    """
    #def create_account_window(self):
        """
        Creates a window for adding accounts.

        # Create a new window
        account_window = tk.Toplevel(self.master)
        account_window.title("Create Account")

        # Define labels and entries with a dictionary
        account_fields = {
            "customer_name": {"label": "Customer Name:", "entry": tk.Entry(account_window)},
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

class InterfaceBank:

    def __init__(self, master, data_ops, bank_account, account_creation):
        self.master = master
        self.master.title("A-Z TRAPEZA")
        self.data_ops = data_ops
        self.bank_account = bank_account
        self.account_creation = account_creation
        self.customer = None

        # Setting a color scheme
        bg_color_window = "#4d3d08"
        bg_color = "#5d6134"
        accent_color = "#548ca8"
        highlight_color = "#D8BFD8"
        tt_color = "#4d3d08"
        ff_color = "#ebc81a"

        # Set a font scheme
        font_style = ("monospace", 12)
        font_label = ("Consolas", 10)

        # Master window background
        master.configure(bg=bg_color_window)

        # Labels for Customer info:
        label_texts = ["Account number:", "Amount:",
                       "Customer ID(PIN):", "Budget Category:", "Budget Limit:", "Threshold:"]
        self.label_widgets = [tk.Label(master, text=text, font=font_style) for text in label_texts]

        # Entry fields
        entry_widgets = [tk.Entry(master, font=font_style) for _ in range(len(label_texts))]
        self.entry_account_number, self.entry_amount, \
            self.entry_customer_id, self.entry_budget_category, \
            self.entry_budget_limit, self.entry_threshold, = entry_widgets

        # Hide PIN entry field
        self.entry_customer_id.config(show='*')

        # Buttons
        button_texts = ["Deposit", "Withdraw", "Transactions", "Create Account",
                        "Select Customer", "Set Budget", "Budget Limit","Spend Budget", "Check Balance", "Set Threshold", "Clear Data", "Calculate", "Budget Categories", "Exit A-Z"]

        button_commands = [self.deposit_money, self.withdraw_money, self.show_account_transactions,
                           self.create_account_window, self.select_customer, self.set_budget, self.get_budget_category_limit,
                           self.spend_budget, self.check_account_balance, self.set_threshold, self.clear_data, self.calculate, self.budget_categories_dict, self.on_closing]

        self.button_widgets = [tk.Button(master, text=text, command=cmd, bg=accent_color, fg=ff_color, font=font_style)
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

        # Label to display Account Holder
        self.label_name = tk.Label(master, text="Account Holder: ", font=font_label, bg=tt_color, fg=ff_color)
        self.label_name.grid(row=len(label_texts), column=1, columnspan=2, pady=10)

        # Label to display threshold
        self.label_threshold = tk.Label(master, text="Threshold: $0.0", font=font_label, bg=tt_color, fg=ff_color)
        self.label_threshold.grid(row=len(label_texts), column=2, columnspan=2, pady=10)

        # Apply the background color to widgets
        for widget in self.label_widgets + self.button_widgets + [self.notification_text]:
            widget.configure(bg=tt_color, fg=ff_color)





    def create_account_window(self):
        """
        Creates a window for adding accounts.
        """
        # Create a new window
        account_window = tk.Toplevel(self.master)
        account_window.title("Create Account")

        # Define labels and entries with a dictionary
        account_fields = {
            "customer_name": {"label": "Customer Name:", "entry": ttk.Entry(account_window)},
            "account_number": {"label": "Account Number:", "entry": ttk.Entry(account_window)},
            "account_holder": {"label": "Account Holder:", "entry": ttk.Entry(account_window)},
            "customer_id": {"label": "Customer ID:", "entry": ttk.Entry(account_window)},
            "default_balance": {"label": "Default Balance:", "entry": ttk.Entry(account_window)},
        }

        bg_color_window = "#4d3d08"
        tt_color = "#4d3d08"
        ff_color = "#ebc81a"

        # Adding a style
        style = ttk.Style()
        style.configure('Accent.TLabel', font=('monospace', 10))
        style.configure('Accent.TEntry', font=('monospace', 10), background=tt_color, foreground=ff_color)
        style.configure('Accent.TButton', font=('monospace', 10), background=tt_color, foreground=tt_color)

        # window background
        account_window.configure(background=bg_color_window)

        # Add labels and entries to the grid layout
        row = 0
        for field_name, field_data in account_fields.items():
            label = ttk.Label(account_window, text=field_data["label"], style='Accent.TLabel')
            label.grid(row=row, column=0, padx=10, pady=10, sticky="e")
            field_data["entry"].grid(row=row, column=1, padx=10, pady=10, sticky="w")
            row += 1

        # Add button to add the account
        button_add_account = ttk.Button(
            account_window, text="Create Account", command=lambda: self.add_account(account_fields), style='Accent.TButton')
        button_add_account.grid(row=row, column=0, columnspan=2, pady=10)

        # Apply the background color to widgets
        for widget in [label, field_data["entry"], button_add_account]:
            widget.configure(style='Accent.TEntry' if isinstance(widget, ttk.Entry) else 'Accent.TButton' if isinstance(widget, ttk.Button) else 'Accent.TLabel')


    def calculate(self):
        # Creating a window for the calculator pop up
        calc_window = tk.Toplevel(self.master)
        calc_window.title("Calculator")

        # Setting a modern color scheme
        tt_color = "#4d3d08"
        ff_color = "#ebc81a"

        # Configure the color scheme
        calc_window.configure(bg=tt_color)

        # Entry field for the calculator input
        entry_calc = tk.Entry(calc_window, font=('Consolas', 12), justify='right', bd=10)
        entry_calc.grid(row=0, column=0, columnspan=4, sticky='nsew')

        # Calculator buttons
        calc_buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('DEL', 5, 0), ('Exit', 5, 3),

        ]


        # Create calculator buttons
        for (text, row, column) in calc_buttons:
            if text == 'DEL':
                button = tk.Button(calc_window, text=text, command=lambda: entry_calc.delete(len(entry_calc.get()) - 1, tk.END), bg=tt_color, fg=ff_color, font=('Segoe UI', 10, 'bold'))

            elif text == 'Exit':
                button = tk.Button(calc_window, text=text, command=calc_window.destroy, bg=tt_color, fg=ff_color, font=('Consolas', 10, 'bold'))
            else:
                button = tk.Button(calc_window, text=text, command=lambda t=text: entry_calc.insert(tk.END, t), bg=tt_color, fg=ff_color, font=('Segoe UI', 10, 'bold'))
            button.grid(row=row, column=column, sticky='nsew')


        # Create equal button separately
        equal_button = tk.Button(calc_window, text='=', command=lambda: self.evaluate_expression(entry_calc), bg=tt_color, fg=ff_color, font=('Segoe UI', 10, 'bold'))
        equal_button.grid(row=4, column=2, columnspan=1, sticky='nsew')

        # Configure grid layout
        for i in range(6):
            calc_window.grid_rowconfigure(i, weight=1)
            calc_window.grid_columnconfigure(i, weight=1)


    def evaluate_expression(self, entry):
        try:
            expression = entry.get()
            result = eval(expression)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, f"Error: {e}")
            entry.delete(0, tk.END)



    #Used the eval() function for simplicty reasons but can as well as implement the Calculator class from Extras module and express it using the logic below

    #method to perform evaluation logic
    def evaluate_expressionn(expression, calculator):

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

        if len(customer_id) < 4:
            self.display_notification("Customer ID(PIN) must have atleast four characters!")
            messagebox.showerror("Error", "Customer ID(PIN) must have atleast four characters!")
            return False

        if len(account_number) < 5:
            self.display_notification("Account number must have atleast five characters!")
            messagebox.showerror("Error", "Account number must have atleast five characters!")
            return False

        if not isinstance(customer_name, str):
            self.display_notification("Customer Name must be a string")
            messagebox.showerror("Error", "Customer Name must be a string, Account Holder can have both intergers and strings")
            return False

        # Validate input data
        if not account_number or not account_holder or not customer_id:
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
        self.data_ops.load_data(filename="data_file.yaml")
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
        except TypeError as e:
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


    #Method to update the GUI after successful threshold set
    def update_gui(self):
        if self.data_ops.selected_customer:
            #Dispay customer name:
            name_text = f"Account Holder: {self.data_ops.selected_customer.account_holder}" if hasattr(self.data_ops.selected_customer, 'account_holder') else "Account Holder: None:"
            self.label_name.config(text=name_text)

            # Display threshold or initialize to $0.0 if not set
            threshold_text = f"Threshold: ${self.data_ops.selected_customer.threshold:.2f}" if hasattr(self.data_ops.selected_customer, 'threshold') else "Threshold: $0.0"
            self.label_threshold.config(text=threshold_text)
        else:
            # Handle no customer selected case
            self.display_notification("No customer selected")


    def setup_data_ops(self, filename: str):
        data_ops = DataOps(filename, [])
        # Load data when the app opens
        data_ops.load_data(filename)
        return True


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
                    messagebox.showinfo("Success", f"Customer with account number {self.data_ops.selected_customer.account_number} has been successfully selected")
                    self.display_notification(F"Success ,Customer with account number {self.data_ops.selected_customer.account_number} has been successfully selected")
                else:
                    self.display_notification("Something went wrong while Selecting Account. Default Account selected")
                    messagebox.showerror("Error", f"Account selection failed. Default Account selected!")
                self.update_gui()

        except TypeError as e:
            self.display_notification(f"Error: {e}")
        except InvalidAccountNumberError:
            self.display_notification("Error, Invalid account number entered")
        except Exception as e:
            self.display_notification(f"Error: account selection failed. {e}")


    def withdraw_money(self):
        try:
            amount = float(self.entry_amount.get())
            customer_id = self.entry_customer_id.get()

            if not amount:
                raise ValueError("Please enter a valid amount.")

            if not customer_id:
                raise InvalidCustomerIDError("Please enter a valid customer ID.")

            if not self.data_ops.selected_customer:
                raise NoCustomerSelectedError("Please select a customer first")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError("You entered a wrong PIN.")

            withdraw_successful = self.data_ops.selected_customer.withdraw_money(amount, customer_id)
            if withdraw_successful:
                self.display_notification(f"Success: Withdrawal of {amount} was successful")
                messagebox.showinfo("Success", f"Withdrawal of {amount} was successful")
            else:
                self.display_notification("Withdrawal failed.")
                messagebox.showerror("Error", f"Withdrawal of {amount} was unsuccessful!")

            # Clear input fields
            self.entry_amount.delete(0, tk.END)
            self. entry_customer_id.delete(0, tk.END)

        except ValueError as e:
            self.display_notification(f"Error: {e}")
        except WrongCustomerIdError as e:
            self.display_notification(f"Error: {e}")
        except InvalidCustomerIDError as e:
            self.display_notification(f"Error: {e}")
        except NoCustomerSelectedError as e:
            self.display_notification(f"Error: {e})")
        except Exception as e:
            self.display_notification(f"Error: Withdrawal failed. {e}")


    def deposit_money(self):
        try:
            amount = float(self.entry_amount.get())
            customer_id = self.entry_customer_id.get()

            if not amount:
                raise ValueError("Please enter a valid amount.")

            if not customer_id:
                raise InvalidCustomerIDError("Please enter a valid customer ID.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError("You entered a wrong PIN.")

            if not self.data_ops.selected_customer:
                raise NoCustomerSelectedError("Please select a customer first")

            if self.data_ops.selected_customer:
                deposit_succesful = self.data_ops.selected_customer.deposit_money(amount, customer_id)

                if deposit_succesful:
                    self.display_notification(f"Success: Deposit of ${amount} was successful")
                else:
                    self.display_notification("Deposit failed")
                    messagebox.showerror("Error", f"Deposit of {amount} was unsuccessful")

                # Clear input fields
                self.entry_amount.delete(0, tk.END)
                self.entry_customer_id.delete(0, tk.END)
            else:
                self.display_notification("No customer found")

        except ValueError as e:
            self.display_notification(f"Error: Invalid amount entered {e}")
        except WrongCustomerIdError as e:
            self.display_notification(f"Error: {e}")
        except InvalidCustomerIDError as e:
            self.display_notification(f"Error: {e}")
        except NoCustomerSelectedError as e:
            self.display_notification(f"Error: {e})")
        except InvalidDepositAmountError as e:
            self.display_notification(f"Error: {e})")
        except Exception as e:
            self.display_notification(f"Error: Deposit failed. {e}")
            print(f"Error, deposit failed {e}")


    def check_account_balance(self):
        try:
            customer_id = self.entry_customer_id.get()
            account_number = self.entry_account_number.get()

            if not customer_id:
                raise InvalidCustomerIDError("Please enter a valid customer ID.")

            if not account_number:
                raise InvalidAccountNumberError("Please enter a valid Account Number.")

            if not self.data_ops.selected_customer:
                raise NoCustomerSelectedError("Please select a customer first")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError("You entered a wrong PIN")

            if account_number != self.data_ops.selected_customer.account_number:
                raise InvalidAccountNumberError("Error. You entered an invalid account number")

            # Retrieve and display balance
            current_balance = self.data_ops.selected_customer.account_balance
            messagebox.showinfo("Account Balance", f"Your current account balance is ${current_balance}.")
            self.display_notification(f"Your current account balance is ${current_balance}.")
            return current_balance

            self. entry_customer_id.delete(0, tk.END)

        except ValueError as e:
            self.display_notification(f"Error: {e}")
        except WrongCustomerIdError as e:
            self.display_notification(f"Error: {e}")
        except InvalidAccountNumberError as e:
            self.display_notification(f"Error: {e}")
        except InvalidCustomerIDError as e:
            self.display_notification(f"Error: {e}")
        except NoCustomerSelectedError as e:
            self.display_notification(f"Error: {e})")
        except Exception as e:
            self.display_notification(f"Error: Check balance failed. {e}")


    def show_account_transactions(self):
        try:
            customer_id = self.entry_customer_id.get()
            account_number = self.entry_account_number.get()

            if not customer_id:
                raise InvalidCustomerIDError("Please enter a valid customer ID.")

            if not account_number:
                raise InvalidCustomerIDError("Please enter a valid Account Number amount.")

            if not self.data_ops.selected_customer:
                raise NoCustomerSelectedError("Please select a customer first")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIDError ("You entered a wrong PIN")

            if account_number != self.data_ops.selected_customer.account_number:
                raise InvalidAccountNumberError("You entered an invalid account number")

            #Retrive transacton history
            transactions =  self.data_ops.selected_customer.account_transactions(customer_id, account_number)
            if transactions:
                formatted_transactions = "\n".join(str(transaction) for transaction in transactions)
                messagebox.showinfo("Transactions", f"{self.data_ops.selected_customer.account_holder}'s transaction history:\n{formatted_transactions}")

                return formatted_transactions
            else:
                # Handles the case where there are no transactions
                messagebox.showinfo("Transactions", f"{self.data_ops.selected_customer.account_holder}'s transaction history is empty.")
                return ""

            # Clear input fields
            self.entry_customer_id.delete(0, tk.END)

        except ValueError as e:
            self.display_notification(f"Error: {e}")
        except InvalidAccountNumberError as e:
            self.display_notification(f"Error: {e}")
        except InvalidCustomerIDError as e:
            self.display_notification(f"Error: {e}")
        except WrongCustomerIdError as e:
            self.display_notification(f"Error: {e}")
        except NoCustomerSelectedError as e:
            self.display_notification(f"Error: {e})")
        except TypeError as e:
            self.display_notification(f"Error: {e}")
        except Exception as e:
            messagebox.showerror("Error", e.message)
            return {}


    def set_budget(self):
        try:
            customer_id = self.entry_customer_id.get()
            limit = float(self.entry_budget_limit.get())
            category = self.entry_budget_category.get()

            if not limit:
                raise ValueError("Please enter a valid limit amount.")

            if not customer_id:
                raise InvalidCustomerIDError("Please enter a valid customer ID.")

            if not self.data_ops.selected_customer:
                raise NoCustomerSelectedError ("Please select a customer before setting budget.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError("You entered a wrong PIN")

            if not category:
                self.display_notification("Error: Please select a category to proceed")
                messagebox.showerror("Error", "Please select a category to proceed")
                return

            selected_customer = self.data_ops.selected_customer
            if selected_customer:
                if limit > self.data_ops.selected_customer.account_balance:
                    raise InsufficientFundsError("Insufficient funds to proceed, budget limit cannot exceed current account balance.")

            if category in self.data_ops.selected_customer.budget_categories:
                raise BudgetCategoryAlreadyExistsError(f"Budget category '{category}' already has a limit set.")

            self.data_ops.selected_customer.budget_categories[category] = {"category": category, "limit": limit}

            messagebox.showinfo("Success", f"Dear customer, a budget category of {category} with a limit of ${limit} was successfully added to your budget categories. Thank you for keeping it A-Z!")
            return True

            # Clear input fields
            self.entry_budget_limit.delete(0, tk.END)
            self.entry_customer_id.delete(0, tk.END)

        except ValueError as e:
            self.display_notification(f"Error: {e}")
        except TypeError as e:
            self.display_notification(f"Error: {e}")
        except InvalidCustomerIDError as e:
            self.display_notification(f"Error: {e}")
        except WrongCustomerIdError as e:
            self.display_notification(f"Error: {e}")
        except NoCustomerSelectedError as e:
            self.display_notification(f"Error: {e})")
        except InsufficientFundsError as e:
            self.display_notification(f"Error: {e}")
        except BudgetCategoryAlreadyExistsError as e:
            self.display_notification(f"Error: {e}")


    def budget_categories_dict(self):
        customer_id = self.entry_customer_id.get()

        try:
            if not isinstance(customer_id, str):
                raise TypeError("Customer ID must be a string.")

            if not customer_id:
                raise InvalidCustomerIDError("Invalid Customer ID")

            if not self.data_ops.selected_customer:
                raise NoCustomerSelectedError("Please select a customer first")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError("You entered the wrong Customer ID(PIN)")

            #Retrive budget categories dict
            results = self.data_ops.selected_customer.budget_categories
            if results:
                formatted_results = "\n".join(f"{category}: ${limit}" for category, limit in results.items())
                messagebox.showinfo("Budget Categories", f"{self.data_ops.selected_customer.account_holder}'s Budget Categories:\n{formatted_results}")
                return formatted_results

            else:
                # Handles the case where there are no Budget Categories
                messagebox.showinfo("Budget Categories", f"{self.data_ops.selected_customer.account_holder} has not yet set any Budget Categories.")
                return ""

            # Clear input fields
            self.entry_customer_id.delete(0, tk.END)

        except TypeError as e:
            self.display_notification(f"Error: {e}")
        except WrongCustomerIdError as e:
            self.display_notification(f"Error: {e}")
        except InvalidCustomerIDError as e:
            self.display_notification(f"Error: {e}")
        except NoCustomerSelectedError as e:
            self.display_notification(f"Error: {e})")
        except Exception as e:
            messagebox.showerror("Error",e)
            return {}


    def get_budget_category_limit(self):
        customer_id = self.entry_customer_id.get()
        category = self.entry_budget_category.get()

        try:
            if not isinstance(customer_id, str):
                raise TypeError("Invalid customer ID")

            if not customer_id:
                raise InvalidCustomerIDError("Please enter a valid customer ID")

            if not category:
                self.display_notification("Please enter a valid category name")
                return

            if not self.data_ops.selected_customer:
                raise NoCustomerSelectedError ("Please select a customer to proceed.")

            if category not in self.data_ops.selected_customer.budget_categories:
                raise BudgetCategoryNotFoundError(f"Budget category '{category}' not found.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError("You entered the wrong Customer ID(PIN)")

            budget_limit_success = self.data_ops.selected_customer.get_budget_category_limit(category, customer_id)
            if budget_limit_success is not None:
                messagebox.showinfo("Success", f"Dear {self.data_ops.selected_customer.account_holder}, your set up for budget: {category} is: {budget_limit_success}")
                self.display_notification(f"Dear {self.data_ops.selected_customer.account_holder}, your current setup for budget: {category} is: {budget_limit_success}")
            else:
                self.display_notification(f"{self.data_ops.selected_customer.account_holder} has no budget Category set")

            # Clear input fields
            self.entry_customer_id.delete(0, tk.END)

        except TypeError as e:
            self.display_notification(f"Error: {e})")
        except InvalidCustomerIDError as e:
            self.display_notification(f"Error: {e})")
        except WrongCustomerIdError as e:
            self.display_notification(f"Error: {e})")
        except BudgetCategoryNotFoundError as e:
            self.display_notification(f"Error: {e})")
        except NoCustomerSelectedError as e:
            self.display_notification(f"Error: {e})")
        except Exception as e:
            self.display_notification(f"Error: {e})")
            return {}


    def spend_budget(self):
        customer_id = self.entry_customer_id.get()
        category = self.entry_budget_category.get()
        amount = self.entry_amount.get()

        try:
            if not amount:
                raise ValueError("Please enter a valid amount to spend.")

            if not customer_id:
                raise InvalidCustomerIDError("Please enter a valid customer ID.")

            if not self.data_ops.selected_customer:
                raise NoCustomerSelectedError ("Please select a to proceed.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError("Invalid customer_id")

            if not category:
                self.display_notification("Please select a category to proceed")
                messagebox.showerror("Error", "Please select a category to proceed")
                return False

            expense_success = self.data_ops.selected_customer.spend_from_budget(category, amount, customer_id)

            if expense_success:
                self.display_notification(f"Expense of ${amount} from category {category} was successful. Your new balance is ${self.data_ops.selected_customer.account_balance}.")
                return expense_success
            else:
                self.display_notification(f"Expense of ${amount} from category {category} was unsuccessful. Your budget limit for {category} is ${self.data_ops.selected_customer.budget_categories.get(category, 0)}.")
                return False

            # Clear input fields
            self.entry_amount.delete(0, tk.END)
            self.entry_customer_id.delete(0, tk.END)

        except ValueError as e:
            self.display_notification(f"Error: {e})")
        except TypeError:
            self.display_notification(f"Error: something unexpected happended, Please try again later!")
        except WrongCustomerIdError as e:
            self.display_notification(f"Error: {e})")
        except InvalidCustomerIDError as e:
            self.display_notification(f"Error: {e})")
        except NoCustomerSelectedError as e:
            self.display_notification(f"Error: {e})")
        except Exception:
            self.display_notification(f"Error: something unexpected happended, Please try again later!")
            return False


    def set_threshold(self):
        try:
            customer_id = self.entry_customer_id.get()
            threshold = self.entry_threshold.get()
            account_number = self.entry_account_number.get()

            if not account_number:
                raise InvalidAccountNumberError("Please enter a valid account_number.")

            if not customer_id:
                raise InvalidCustomerIDError("Please enter a valid customer ID.")

            if not threshold:
                raise InvalidThresholdAmountError("Please enter a valid threshold amount.")

            if account_number != self.data_ops.selected_customer.account_number:
                raise InvalidAccountNumberError("You entered an invalid account number")

            if not self.data_ops.selected_customer:
                raise NoCustomerSelectedError("Please select a customer before setting a threshold.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError("You entered a wrong pin")


            if self.data_ops.selected_customer.threshold:
                # Prompt user for confirmation
                confirmation = messagebox.askokcancel("Threshold Reset", f"Dear {self.data_ops.selected_customer.account_holder} you already have a threshold of ${self.data_ops.selected_customer.threshold} set for account number {self.data_ops.selected_customer.account_number}. Are you sure you want to continue?")

                if not confirmation:
                    self.display_notification("Thank you for keeping it A-Z")
                    return False

            self.data_ops.selected_customer.set_account_threshold(threshold, customer_id)
            self.display_notification(f"A threshold  of {threshold} has successfully been set for account: {self.data_ops.selected_customer.account_number}, account holder: {self.data_ops.selected_customer.account_holder}.")
            self.update_gui()

            # Clear input fields
            self.entry_threshold.delete(0, tk.END)
            self.entry_customer_id.delete(0, tk.END)

        except ValueError as e:
            self.display_notification(f"Error: {e}")
        except TypeError as e:
            self.display_notification(f"Error: {e}")
        except InvalidCustomerIDError as e:
            self.display_notification(f"Error: {e})")
        except InvalidAccountNumberError as e:
            self.display_notification(f"Error: {e})")
        except WrongCustomerIdError as e:
            self.display_notification(f"Error: {e})")
        except InvalidThresholdAmountError as e:
            self.display_notification(f"Error: {e})")
        except NoCustomerSelectedError as e:
            self.display_notification(f"Error: {e})")
        except Exception as e:
            self.display_notification(f"Error: {e}")


    def clear_data(self):
        try:
            customer_id = self.entry_customer_id.get()

            if not customer_id:
                raise InvalidCustomerIDError ("Please enter a valid customer ID.")

            if not self.data_ops.selected_customer:
                raise NoCustomerSelectedError ("Please select a customer first.")

            if customer_id != self.data_ops.selected_customer.customer_id:
                raise WrongCustomerIdError ("You entered a wrong PIN")

            # Prompt user for confirmation
            confirmation = messagebox.askokcancel("Clear Account Data", "Are you sure you want to clear all account data? This action is permanent and cannot be undone.")

            if not confirmation:
                return False

            self.data_ops.selected_customer.clear_data(customer_id)
            self.display_notification("Contents of the data file have been successfully removed")
            messagebox.showinfo("Succes", "Contents of the data file have been successfully removed")

            # Clear input fields
            self.entry_customer_id.delete(0, tk.END)

        except TypeError as e:
            messagebox.showerror("Error", e)
        except ValueError as e:
            messagebox.showerror("Error", e)
        except InvalidThresholdAmountError as e:
            self.display_notification(f"Error: {e})")
        except NoCustomerSelectedError as e:
            self.display_notification(f"Error: {e})")
        except WrongCustomerIdError as e:
            self.display_notification(f"Error: {e})")
        except Exception as e:
            self.display_notification(f"Error {e}")


    # save the account data when the application is closed
    def on_closing(self):
        self.master.destroy()

        """