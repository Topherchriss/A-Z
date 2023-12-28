# A-Z TRAPEZA

A Simple Banking System

## Overview

A-Z TRAPEZA is a simple banking system application built with pure Python and the Tkinter library for the graphical user interface. This application allows users to interact with a real life banking and finacial managment tool.

## Features

- **Account Management:** Users can create and manage multiple bank accounts.
- **Budget Management:** Set spending limits for specific categories, track expenses, view budget limits,
- **Deposit:** Make deposits into the selected account with a customizable notification for large deposits.
- **Withdrawal:** Perform withdrawals with balance validation and notifications for large withdrawals.
- **Check Balance:** View the current balance of the selected account.
- **Transaction History:** Access a detailed transaction history for the selected account.
- **Graphical User Interface:** User-friendly interface intergrated with a basic **calculator** for quick calculations and easy interaction.
-Additionally there is a **CLEAR** feature that enables the user to clear ```data_file.yaml``` file

## Getting Started

Follow the installation instructions below to set up the A-Z TRAPEZA on your local machine.

### Prerequisites

- Python (version 3.X.X)
- Tkinter library (comes with Python)

### Installation

Clone the repository:

   ```bash
   git clone https://github.com/Topherchriss/A-Z.git

   cd A-Z

   python Gui_Trapeza.py
   ```

## Running Tests

Ensure the stability and functionality of A-Z TRAPEZA by running a set of comprehensive tests. These tests cover various aspects of the application, including deposit, withdrawal, balance checking, transaction history, and the newly added budget management features

### Prerequisites

Before running the tests, make sure you have the required dependencies installed:

- Python (version 3.X.X)
- unittest library

### Running the Tests

To run the tests, use the following command in your terminal:

```bash
python -m unittest discover -s tests -p 'test_Alpha.py'
```

### Usage

1. Launching the Application:

Run the application using the provided script ('python Gui_Trapeza.py').
   The GUI will appear, allowing users to interact with the banking system.

2. Account Creation and Selection

A-Z TRAPEZA unlike before where there were only 3 predefined accounts; now allows users to create their bank accounts, providing a more personalized experience. Below is an overview of the account creation and selection process:

### Creating an Account

Users can create a new bank account by entering the required information; customer name, account number, account holder, initial balance(regardless of the amount entered the account balance will always be initialized to zero($0)), and a secure Customer ID(PIN). The application validates the input and creates a new account for the user. Enhancing user interaction and customization!

### Selecting an Account

After creating an account, users can select it for performing various banking operations by inputting the account number used to create the account and pressing the select customer button. The selected account becomes the active account for the session but can as well as quickly change to another valid account through the same process.

### Account Selection Fallback

In case of any issues with account selection, such as entering a non-recognized Account Number, selecting a non-existing account, or failing to correctly load data, the application provides a fallback mechanism(You will encounter an error when you try to interact with the application without selecting a customer). A predefined default account, named 'IamTheDefaultCustomer' is available for users to interact with the application even if the account selection process fails. The details of the default account are as follows:

- **Account Name:** IamTheDefaultCustomer
- **Account Number:** 1010101
- **Customer ID (PIN):** 2345
- **Account Balance:** $100,000.00

This default account ensures that users can continue exploring and testing the application even if they encounter difficulties with their created accounts.


3. Performing Transactions:

    Use the provided entry fields to input, the account number, amount, budget category name, budget limit, threshold, and PIN for transactions Different transactions require different inputs but ALL transactions require the customer ID(PIN).
    Buttons are available "Deposit", "Withdraw", "Transactions(The transaction history)", "Create Account(The create account window)", "Select Customer(The MUST press button with a valid account number before performing any actions)", "Set Budget(Button to set a specific budget limit)", "Budget Limit(Button to check the budget limit of a given budget category)", "Spend Budget(Button to spend from a given budget category)", "Check Balance", "Set Threshold(Button to set a threshold for the active account)", "Clear Data(Button to clear data)", "Calculate(Button to open calculator window)", "Budget Categories(Button to view all of your budget categories and their limits)", "Exit A-Z(Button to safely exit the App)".

4. Budget Management

### Setting a Budget

Users can set spending limits for different categories. When setting a budget, users need to provide the customer ID, the desired budget limit, and the category for which the budget is being set. The application does a series of validations before proceeding to set the budget.

### Viewing Budget Categories

Users can view their existing budget categories along with their respective limits. This provides a quick overview of the allocated budgets for different spending categories.

### Viewing Budget Limit

Users can check the current limit for a specific budget category. This is helpful for users to stay informed about their spending limits in various categories.

### Spending from Budget

To maintain control over expenses, users can spend from their budget by providing the customer ID, the category from which they want to spend from, and the amount. The application checks whether the spending amount is within the budget limit for the specified category before proceedin.

### Notifications

Users receive notifications for budget-related actions, such as setting a budget, reaching budget limits, or overspending. Notifications provide timely alerts to help users manage their finances effectively.

### Contributing

Constructive contributions are welcomed and highly appreciated! 
To get started

1. **Fork the Repository:**

   - Click the "Fork" button on the top right of this repository to create your own copy.

2. **Clone Your Fork:**

   ```bash
   git clone https://github.com/Topherchriss/A-Z.git
   cd A-Z
  ```
3. ***Create New Branch***
   ```bash
   git checkout -b feature/new-feature

   ```
4. ***Make Your Changes***

Implement your changes and improvements.

Run Tests:
Before submitting a pull request, make sure your changes pass any existing tests.
If there are no existing tests, consider adding new ones to cover your changes.
commit and push your changes using descriptive commit names

5. ***Submit a Pull Request***

Open a pull request on GitHub with clear descriptions of your changes.

6. ***Collaborate***:

Engage in discussions related to your pull request.
Be responsive to feedback and make necessary adjustments.

***Thank you for your contribution!***

### License

This project is licensed under General Public License - see the LICENSE file for details

## Future Vision

A-Z TRAPEZA is an evolving project with a vision to incorporate additional features and improvements in the future.

### 1. Web Application

Explore the development of a web application to provide users with the flexibility to manage their accounts on the go. Allowing users to customize their account settings, including profile pictures, account names, and notification preferences, for a more personalized banking experience.

### 2. Implement Security Features

Implement security layers, to ensure a secure and trustworthy banking experience for users.

### 3. Advanced Budget Analytics

Introduce advanced analytics tools to help users analyze their spending patterns, set dynamic budget limits, and receive personalized financial insights.

### 4. Community Collaboration

Encourage collaboration and contributions from the community to enhance the application's features, fix bugs, and provide feedback.

### 5. Integration with Financial Institutions

Explore possibilities for integrating the application with real financial institutions, providing users with the ability to link their actual bank accounts and manage them through A-Z TRAPEZA.

These plans align with commitments to delivering a robust and user-friendly banking system. Contributions and feedback from the community are highly valued as work towards achieving these goals goes on.

### Acknowledgments
. Special thanks to **tkinter** for providing  the  GUI framework.
. Special thanks to **Cisco Skills for all** for the well-structured Python lessons.
. Inspired by the idea of implementing OOP principles that I'm currently learning at **Cisco Skills for All**.

