import os
import json
import tkinter as tk
from calculate import Calculator
from tkinter import messagebox
from Alpha import BankAccount
from Alpha import BankCustomer
from json_utils import save_bank_account_data, load_bank_account_data

class BankInterface:
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


    def __init__(self, master):

        """
        Initialize the BankInterface.

        Parameters:
            master (tk.Tk): The master tkinter window.
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
        self.customer2_account = BankAccount(account_number="1000102", account_holder="Chachu Mulumba", customer_id="2567",  default_balance=1500)
        self.customer3_account = BankAccount(account_number="1000103", account_holder="Zigi Zige", customer_id="3678", default_balance=2000)

        # Add accounts to customers
        self.customer1.addAccount(self.customer1_account)
        self.customer2.addAccount(self.customer2_account)
        self.customer3.addAccount(self.customer3_account)


        self.selected_customer = None
        self.selected_account = None
        self.account_data = {}

         # Load account data from JSON file
        try:
            account_data = load_bank_account_data("account_data.json")
        except InvalidJSONFormatError as e:
            print("Error loading account data:", e)

        self.selected_account = self.customer2_account
        self.selected_customer = self.customer2

        self.account_data = load_bank_account_data(self.selected_account)
        # Update the display after setting the selected customer and account
        self.update_display()


    # Method to save the BankAccount data to the JSON file
    def save_account_data(self):
        try:
            save_bank_account_data(self.selected_account, "account_data.json")
        except Exception as e:
            print(f"An error occurred while saving account data: {e}")

    def load_account_data(self, account_data):
        # Check if the JSON file exists
        if not os.path.exists('account_data.json'):
            print("Account data file not found.")
            return None
        try:
            #account_data = load_bank_account_data("account_data.json")
            if account_data:
                self.selected_account = account_data
                print("Account data loaded successfully")
            else:
                print("No account data found")
        except Exception as e:
            print(f"An error occurred while loading account data: {e}")


    def update_display(self):

        # Load account data from JSON file
        try:
            account_data = load_bank_account_data("account_data.json")
        except Exception as e:
            print(f"An error occurred while loading account data: {e}")
            return

        if account_data:
            # Update selected account and customer if account data is valid
            self.selected_account = self.customer2_account
            self.selected_customer = self.customer2

            # Calculate total balance
            stored_balance = self.selected_account.account_balance
            previous_transactions = sum(
                entry["Amount deposited"]
                if entry["Type of transaction"] == "Deposit"
                else -entry["Amount withdrawn"]
                for entry in self.selected_account.transaction_history
            )
            total_balance = stored_balance + previous_transactions

            # Update display elements with valid data
            self.label_customer_name.config(text=f"Customer's Name: {self.selected_account.account_holder}")
            self.label_account_number.config(text=f"Customer's account number: {self.selected_account.account_number}")
            self.label_balance.config(text=f"Current Balance: ${total_balance:.2f}")

        else:
            # Display error message if account data is not found
            print("No account data found")


    # Method to switch customer and update the display
    def switch_customer(self, customer):
        self.selected_customer = customer1
        # For simplicity, every customer has only one account as of now
        self.selected_account = customer1.accounts[0]
        self.load_account_data(account_data)
        self.update_display()

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
            self.save_account_data()
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

            self.save_account_data()
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
            self.save_account_data()
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

                self.save_account_data()
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
            self.save_account_data()

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
                result = evaluate_expression(expression, calculator)
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
        self.save_account_data()
        print("saved data:", self.save_account_data)
        print("Account data saved. Destroying the window.")
        self.master.destroy()