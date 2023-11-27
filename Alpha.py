import tkinter as tk
from tkinter import messagebox

class BankAccount:
    def __init__(self, account_number, account_holder, customer_id, default_balance = 0):

        self.account_number = account_number
        self.account_holder = account_holder
        self.customer_id = customer_id
        self.account_balance = default_balance
        self.transaction_history = []


    def deposit(self, amount):
        if amount > 0:
            self.account_balance += amount

            self.transaction_history.append({"Type of transaction": "Deposit", "Amount deposited": amount})
            self.send_notification()

            print(f"Dear customer your deposit of {amount} was succesful. Your new balance is: {self.account_balance}")
        else:
            raise ValueError("Invalid deposit amount. Please enter a positive value.")

    def withdraw(self, amount):

        if amount >= 10 and amount <= self.account_balance:
            self.account_balance -= amount

            self.transaction_history.append({"Type of transaction": "withdrawal", "Amount withdrawn": amount})
            self.send_notification()

            print(f"Withdrawl of {amount} was succesful. Your new account balance is {self.account_balance}")
        else:
            print(f"Invalid withdrawal amount or Insufficient funds to withdraw: {amount}")


    def checkBalance(self):
        print(f"Your Current account balance is: {self.account_balance}" )


    def get_transaction_history(self):
        return self.transaction_history


    def send_notification(self):
        # Check for significant events
        if self.transaction_history:
            last_transaction = self.transaction_history[-1]
            if last_transaction["Type of transaction"].lower() == "Deposit" and last_transaction["Amount deposited"] > 50000:
                print("Notification: A large deposit was made to your account.")
            elif last_transaction["Type of transaction"].lower() == "Withdrawl" and last_transaction["Amount withdrawn"] > 5000:
                print("Notification: A large withdrawal was made from your account.")

        # Check balance threshold
        if self.account_balance < 100:
            print("Notification: Your account balance is below $100.")

class BankCustomer:

    def __init__(self, customer_name):

        self.customer_name = customer_name
        self.accounts = []

    def addAccount(self, account):


        self.accounts.append(account)

        print(f"Account {account.account_number} added for {self.customer_name}. Thank you for choosing our bank.")


    def total_balance(self):
        total = sum(account.account_balance for account in self.accounts)

        print(f"The total amount in {self.customer_name} accounts is: {total}")


    def __str__(self):
        return str(self.accounts)


class BankGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("A-Z TRAPEZA")

        #Labels for Customer info:
        self.label_customer_name = tk.Label(master, text="Customer's Name:")
        self.label_account_number = tk.Label(master, text="Customer's account number:")
        self.label_amount = tk.Label(master, text="Amount:")
        self.label_customer_id = tk.Label(master, text="Enter your pin:")

        #Entry fields
        self.entry_customer_name = tk.Entry(master)
        self.entry_account_number= tk.Entry(master)
        self.entry_amount = tk.Entry(master)
        self.entry_customer_id = tk.Entry(master)


        #Buttons
        self.button_deposit = tk.Button(master, text="Deposit", command=self.deposit_amount)
        self.button_withdraw = tk.Button(master, text="Withdraw", command=self.withdraw_cash)
        self.button_transactions = tk.Button(master, text="Transactions", command=self.show_transactions)
        self.button_balance = tk.Button(master, text="Check Balance", command=self.check_balance)


        #Grid layoutP
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

        #show updated balance on the GUI
        self.label_balance = tk.Label(master, text="Current Balance: $0.00")
        self.label_balance.grid(row=8, column=0, columnspan=2, pady=10)

        # Notification area on GUI
        self.notification_text = tk.Text(master, height=2, width=40)
        self.notification_text.grid(row=9, column=0, columnspan=2, pady=20)

        #Create Three customers
        self.customer1 = BankCustomer(customer_name="Jean Maswa")
        self.customer2 = BankCustomer(customer_name="Chachu Mulumba")
        self.customer3 = BankCustomer(customer_name="Zigi Zige")

        self.customer1_account = BankAccount(account_number="1000101", account_holder="Jean Maswa", customer_id="1456", default_balance=1000)
        self.customer2_account = BankAccount(account_number="1000102", account_holder="Chachu Mulumba", customer_id="2567",  default_balance=1500)
        self.customer3_account = BankAccount(account_number="1000103", account_holder="Zigi Zige", customer_id="3678", default_balance=2000)

        # Add accounts to customers
        self.customer1.addAccount(self.customer1_account)
        self.customer2.addAccount(self.customer2_account)
        self.customer3.addAccount(self.customer3_account)

        # Select the first customer and account by default
        self.selected_customer = self.customer3
        self.selected_account = self.customer3_account
        self.update_display()

        # Method to update the GUI display based on the selected customer and account
    def update_display(self):
        self.label_customer_name.config(text=f"Customer's Name: {self.selected_customer.customer_name}")
        self.label_account_number.config(text=f"Customer's account number: {self.selected_account.account_number}")
        self.label_balance.config(text=f"Current Balance: ${self.selected_account.account_balance:.2f}")


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

        else:
            self.selected_account.deposit(amount)

            self.label_balance.config(text=f"Current Balance: ${self.selected_account.account_balance:.2f}") #Update the GUI after every transaction

            if amount >= 50000:
                self.display_notification(f"A large deposit of ${amount} was made to your account.") #Notify the user of large deposit amounts

            messagebox.showinfo("Success", f"Deposit of ${amount} was succesful. New account balance: ${self.selected_account.account_balance}")

    # Method to withdraw
    def withdraw_cash(self):
        customer_name = self.entry_customer_name.get()
        account_number = self.entry_account_number.get()
        customer_id = self.entry_customer_id.get()
        amount = 0.0  # Initialize with a default value

        #Validate Input
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
        else:
            self.selected_account.withdraw(amount)

            self.label_balance.config(text=f"Current Balance: ${self.selected_account.account_balance:.2f}") #Update the GUI after every transaction

            if amount >= 5000:
                self.display_notification(f" A large amount of ${amount} was successfully withdrawn from your account.") #Inform the customer of large withdrawls from their account

            messagebox.showinfo("Success", f"Withdrawal of ${amount} was a success. Your new account balance is: ${self.selected_account.account_balance}")


    # Method to check balance
    def check_balance(self):
        customer_name = self.entry_customer_name.get()
        account_number = self.entry_account_number.get()
        customer_id = self.entry_customer_id.get()

        if customer_name != self.selected_account.account_holder or account_number != self.selected_account.account_number:
            messagebox.showerror("Invalid Customer", "Customer not found!")

        elif customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong Pin", "Cannot proceed to check balance. You entered a wrong Pin")

        else:
            self.selected_account.checkBalance()
            messagebox.showinfo("Account Balance", f"Dear ${customer_name}, your current account balance is: ${self.selected_account.account_balance}")

    # Method to display transactions
    def show_transactions(self):
        customer_name = self.entry_customer_name.get()
        account_number = self.entry_account_number.get()
        customer_id = self.entry_customer_id.get()

        if customer_name != self.selected_account.account_holder or account_number != self.selected_account.account_number:
            messagebox.showerror("Invalid Customer", "Customer not found!")

        elif customer_id != self.selected_account.customer_id:
            messagebox.showerror("Wrong Pin", f"Cannot proceed to show account transaction You entered a wrong pin!")

        else:
            transaction_history = self.selected_account.get_transaction_history()
            if not transaction_history: #check the case where there are no transactions
                messagebox.showinfo("Transactions", "No transactions available so far.")
            else:
                formatted_transactions = "\n".join(str(transaction) for transaction in transaction_history)
                messagebox.showinfo("Transactions", f"{customer_name}'s transaction history:\n{formatted_transactions}")

root = tk.Tk()
app = BankGUI(root)
root.mainloop()

