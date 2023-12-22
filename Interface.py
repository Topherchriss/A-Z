"""The grand GUI for A-Z in slow development"""

from tkinter import Tk, Label, Frame, Button, Entry, font

# Theme colors and fonts
ACCENT_COLOR = "#3498DB"
SECONDARY_COLOR = "#F1F5F8"
PRIMARY_FONT = ("Roboto", 14)
SECONDARY_FONT = ("Roboto", 12)


class GuiManager:
    def __init__(self, master):
        self.master = master
        self.master.title("A-Z Trapeza 2.0")

        # Define custom styles for widgets
        def style_widget(widget, bg_color=SECONDARY_COLOR, fg_color=ACCENT_COLOR, font=PRIMARY_FONT):
            widget.config(bg=bg_color, fg=fg_color, font=font)

        # Create main container frames
        self.account_info_frame = Frame(self.master, bg=SECONDARY_COLOR, padding=10)
        self.transaction_actions_frame = Frame(self.master, bg=SECONDARY_COLOR, padding=10)
        self.budget_management_frame = Frame(self.master, bg=SECONDARY_COLOR, padding=10)

        # Initialize sections with titles and widgets
        self._init_account_info(style_widget)
        self._init_transaction_actions(style_widget)
        self._init_budget_management(style_widget)

        # Apply custom styles to frames
        style_widget(self.account_info_frame)
        style_widget(self.transaction_actions_frame)
        style_widget(self.budget_management_frame)

        # Configure responsive grid layout
        self._configure_grid_layout()

    def _init_account_info(self, style_func):
        title = Label(self.account_info_frame, text="Account Information", font=PRIMARY_FONT, bg=SECONDARY_COLOR)
        title.pack(pady=5)

        # Add custom labels and entries for customer name, account number, etc.
        customer_name_label = Label(self.account_info_frame, text="Customer Name:", font=SECONDARY_FONT, bg=SECONDARY_COLOR)
        customer_name_entry = Entry(self.account_info_frame, font=SECONDARY_FONT, bg=SECONDARY_COLOR)

        account_number_label = Label(self.account_info_frame, text="Account Number:", font=SECONDARY_FONT, bg=SECONDARY_COLOR)
        account_number_entry = Entry(self.account_info_frame, font=SECONDARY_FONT, bg=SECONDARY_COLOR)
        balance_label = Label(self.account_info_frame, text="Current Balance: $0.00", font=SECONDARY_FONT, bg=SECONDARY_COLOR)

        style_func(title)

    def _init_transaction_actions(self, style_func):
        title = Label(self.transaction_actions_frame, text="Transaction Actions", font=PRIMARY_FONT, bg=SECONDARY_COLOR)
        title.pack(pady=5)

        #custom buttons for deposit, withdraw, transactions, check balance

        style_func(title)

    def _init_budget_management(self, style_func):
        title = Label(self.budget_management_frame, text="Budget Management", font=PRIMARY_FONT, bg=SECONDARY_COLOR)
        title.pack(pady=5)

        # custom labels, entries, and buttons for budget category, limit

        style_func(title)

    def _configure_grid_layout(self):
        self.account_info_frame.grid(row=0, column=0, sticky="nsew")
        self.transaction_actions_frame.grid(row=1, column=0, sticky="nsew")
        self.budget_management_frame.grid(row=2, column=0, sticky="nsew")

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1, minsize=50)
        self.master.grid_rowconfigure(1, weight=1, minsize=50)
        self.master.grid_rowconfigure(2, weight=1, minsize=50)



# Start the party!
root = Tk()
gui_manager = GuiManager(root)
root.mainloop()


