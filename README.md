# A-Z TRAPEZA

Simple Banking System

## Overview

A-Z TRAPEZA is a simple banking system application built with Python and the tkinter library for the graphical user interface. This application allows users to manage bank accounts, make deposits, withdrawals, check balances, and view transaction history.

## Features

- **Account Management:** Users can create and manage multiple bank accounts.
- **Budget Management:** Set spending limits for specific categories, track expenses, and receive notifications for budget thresholds.
- **Deposit:** Make deposits into the selected account with a customizable notification for large deposits.
- **Withdrawal:** Perform withdrawals with balance validation and notifications for large withdrawals.
- **Check Balance:** View the current balance of the selected account.
- **Transaction History:** Access a detailed transaction history for the selected account.
- **Graphical User Interface:** User-friendly interface intergrated with a basic **calculator** for quick calculations and easy interaction.
-Additionally there is a **CLEAR** feature that enables you to clear ```account_data.json``` file

## Getting Started

Follow the installation instructions below to set up the A-Z TRAPEZA banking system on your local machine.

### Prerequisites

- Python (version 3.X.X)
- tkinter library (comes with Python)

### Installation

Clone the repository:

   ```bash
   git clone https://github.com/Topherchriss/A-Z.git

   cd A-Z

   python Alpha.py
   ```

## Running Tests

Ensure the stability and functionality of A-Z TRAPEZA by running a set of comprehensive tests. These tests cover various aspects of the application, including deposit, withdrawal, balance checking, transaction history, and the newly added budget management features

### Prerequisites

Before running the tests, make sure you have the required dependencies installed:

- Python (version 3.X.X)
- unittest library (comes with Python)

### Running the Tests

To run the tests, use the following command in your terminal:

```bash
python -m unittest discover -s tests -p 'test_Alpha.py'
```

### Usage

1. Launching the Application:

Run the application using the provided script ('python Alpha.py').
    The GUI will appear, allowing users to interact with the banking system.

2. ## Pre-loaded Test Accounts

For testing and demonstration purposes, three pre-loaded test accounts are available. Use these accounts to explore the application's features.

1. **Account 1**
   - Customer Name: Jean Maswa
   - Account Number: 1000101
   - Customer ID (PIN): 1456
   - Default Balance: $1000.00

2. **Account 2**
   - Customer Name: Chachu Mulumba
   - Account Number: 1000102
   - Customer ID (PIN): 2567
   - Default Balance: $1500.00

3. **Account 3**
   - Customer Name: Zigi Zige
   - Account Number: 1000103
   - Customer ID (PIN): 3678
   - Default Balance: $2000.00

**Important:** These accounts are not real, and any changes made will not have any impact on actual bank accounts or financial transactions. Do not use real information for testing purposes.


3. Performing Transactions:
    Use the provided entry fields to input customer name, account number, amount, and PIN for transactions.
    Buttons are available for deposit, withdrawal, checking balance, and viewing transactions.

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

This project is licensed under general Public License - see the LICENSE file for details

### Acknowledgments
. Special thanks to **tkinter** for providing  the  GUI framework.
. Special thanks to **Cisco skills for all** for the well structured Python lessons.
. Inspired by the idea of implementing OOP principles that i'm currently learning at **Cisco skills for all**.

