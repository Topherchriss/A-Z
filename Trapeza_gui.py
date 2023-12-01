import tkinter as tk
from Extras import Calc
from tkinter import messagebox
from Alpha import BankAccount
from Alpha import BankCustomer
from json_utils import save_bank_account_data, load_bank_account_data

class BankInterface:
    def __init__(self, master):
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


        self.notification_text = tk.Text(master, height=2, width=40)
        self.notification_text.grid(row=14, column=0, columnspan=2, pady=20)

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

        # Select the first customer and account by default
        self.selected_customer = self.customer2
        self.selected_account = self.customer2_account
        self.update_display()

        # Load the initial BankAccount data from the JSON file
        try:
            self.selected_account = load_bank_account_data("account_data.json")
        except FileNotFoundError:
            # If the file doesn't exist, create a default account
            self.selected_account = BankAccount(account_number="1000102", account_holder="Chachu Mulumba", customer_id="2567", default_balance=1500)

      # Method to save the BankAccount data to the JSON file
    def save_account_data(self):
        save_bank_account_data(self.selected_account, "account_data.json")

        # Method to update the GUI display based on the selected customer and account
    def update_display(self):
        stored_balance = self.selected_account.account_balance if hasattr(self.selected_account, 'account_balance') else 0.0 # Initialize stored_balance to previous account balance or 0.0 if there is none

        # Add the total of previous transactions to the stored balance
        previous_transactions = sum(self.selected_account.transaction_history)
        total_balance = stored_balance + previous_transactions

        self.label_customer_name.config(text=f"Customer's Name: {self.selected_customer.customer_name}")
        self.label_account_number.config(text=f"Customer's account number: {self.selected_account.account_number}")
        self.label_balance.config(text=f"Current Balance: ${total_balance:.2f}")


    # Method to switch customer and update the display
    def switch_customer(self, customer):
        self.selected_customer = customer
        # For simplicity, every customer has only one account as of now
        self.selected_account = customer.accounts[0]
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
        amount = 0.0  # Initialize with a default value

        #Validate input
        try:
            amount = float(self.entry_amount.get())
        except ValueError:
            messagebox.showerror("Invalid amount", f"Amount must be a numeric figure more than 10 dollars")

        if customer_name != self.selected_account.account_holder or account_number != self.selected_account.account_number:
            messagebox.showerror("Unsuccessful", f"Cannot proceed to deposit, Customer not found!")

        elif customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong Pin", "Cannot proceed to deposit. You entered a wrong Pin!")


        elif amount < 10:
            messagebox.showerror("Unsuccessful", f"Deposit of ${amount} is below the minimum (USD 10)")

            self.entry_customer_id.delete(0, 'end')

        else:
            self.selected_account.deposit(amount)

            self.label_balance.config(text=f"Current Balance: ${self.selected_account.account_balance:.2f}") #Update the GUI after every transaction

            if amount >= 50000:
                self.display_notification(f"A large deposit of ${amount} was made to your account.") #Notify the user of large deposit amounts

            messagebox.showinfo("Success", f"Deposit of ${amount} was succesful. New account balance: ${self.selected_account.account_balance}")
            self.save_account_data()
            self.entry_customer_id.delete(0, 'end')

    # Method to withdraw
    def withdraw_cash(self):
        customer_name = self.entry_customer_name.get()
        account_number = self.entry_account_number.get()
        customer_id = self.entry_customer_id.get()
        amount = 0.0
        try:
            threshold = float(self.entry_set_threshold.get())
        except ValueError:
            messagebox.showerror("Invalid", "Invalid Threshold amount")


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
            if not transaction_history: #check the case where there are no transactions
                messagebox.showinfo("Transactions", "No transactions available so far.")
            else:
                formatted_transactions = "\n".join(str(transaction) for transaction in transaction_history)
                messagebox.showinfo("Transactions", f"{customer_name}'s transaction history:\n{formatted_transactions}")

                self.entry_customer_id.delete(0, 'end')

    def set_budget(self):
        customer_id = self.entry_customer_id.get()
        category = self.entry_budget_category.get()
        try:
            limit = float(self.entry_budget_limit.get())
        except ValueError:
            messagebox.showerror("Error", "Cannot proceed.Invalid limit amount!")

        if customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong Pin", f"Cannot proceed to set budget category. You entered a wrong pin!")

        elif limit < 1 or limit > self.selected_account.account_balance or limit == '':
            messagebox.showerror("Unsuccessful", f"Invalid limit input ${limit}!")

        else:
            self.selected_account.set_budget(category, limit)
            messagebox.showinfo("Success", f"Dear {self.selected_account.account_holder} a budget category of {category} with a limit of ${limit} was added on your acccount. Thank you for keeping it A-Z!")
            self.save_account_data()
            self.entry_customer_id.delete(0, 'end')

    def spend_budget(self):
        category = self.entry_budget_category.get()
        customer_id = self.entry_customer_id.get()
        amount = 0.0
        limit = 0.0
        try:
            limit = float(self.entry_budget_limit.get())
        except ValueError:
            messagebox.showerror("Invalid", "Invalid limit amount")

        try:
            amount = float(self.entry_amount.get())
        except ValueError:
            messagebox.showerror("Invalid", "Invalid amount!")



        if customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong PIN", "Cannot proceed. You entered the wrong PIN")

        elif category not in self.selected_account.budget_categories:
            messagebox.showerror("Error", f"Cannot proceed, category {category} not found!")

        elif amount < 10:
            messagebox.showerror("Error", f"Cannot proceed, amount ${amount} must be more than or equal to $10")

        elif amount > limit:
            messagebox.showerror("Error", f"Dear {self.selected_account.account_holder} ${amount} exceeds budget allocation of ${limit}")



        else:
        # Check if the category exists in cumulative_expenses, if not, initialize it
            if category not in self.selected_account.cumulative_expenses:
                self.selected_account.cumulative_expenses[category] = 0

            elif category == "":
                messagebox.showerror("Invalid", "Please provide a descriptive name for your budget!")

            elif amount + self.selected_account.cumulative_expenses[category] > limit:
                messagebox.showerror("Warning", "Exceeding budget limit")

            else:
                self.selected_account.get_expense(category, amount)
                messagebox.showinfo("Success", f"Dear {self.selected_account.account_holder}, you have spent ${amount} from {category} budget. You budgt limit is ${limit}")
                self.save_account_data()
                self.entry_customer_id.delete(0, 'end')


    def set_threshold(self):
        customer_id = self.entry_customer_id.get()
        threshold = 0.0
        try:
            threshold = float(self.entry_set_threshold.get())
        except ValueError:
            messagebox.showerror("Invalid", "Cannot proceed to set threshold. You entered an invalid threshold amount")


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
            try:
                result = eval(entry_calc.get())
                entry_calc.delete(0, tk.END)
                entry_calc.insert(tk.END, str(result))
                #entry_calc.delete(0, tk.END)
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


    #save the account data when the application is closed
    def on_closing(self):
        # Save the account data before closing the application
        self.save_account_data()
        self.master.destroy()