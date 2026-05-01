# Members
## • Angel Mae B. Asucan
## • Jhonavie B. Dico
## • Bea Rose A. Pacaldo
## • Isagani Dacapio
# BSCS - 1A

# Username: admin
# Password: admin

# Title and Description: HomeTech Solution
## • The HomeTech Solution is a menu driven application that generate invoices, records monthly payment and monitor outstanding balances. It is design for customer who purchased products such as motorcycle, refrigerators, television, washing machine and other products an installment basis. The system helps staff accurately track customer payments, compute remaining balance and produce billing and payment records.

# Prerequisites
## • Python (version 3.x)
## • Flask
## • Web browser (Google Chrome, Edge, etc.)
## • Code editor (VS code recommended)

# Installation
## Follow these steps to run the projects:
## Clone the repository
## • git clone https://github.com/angelmaeasucan/hometech-solution.git

## Go to project folder
## • cd hometech-solution

## Install Flask (if not installed)
## • pip install flask

## Run the application
## • python.py

## Then open your browser and go to:
## • http://127.0.0.1:5000/

# Usage
## • Open the system in your browser
## • Log in using your username and password
## • Access the dashboard
## • Add or manage customer information
## • Create billing transactions (cash or installment)

## Example (Python Flask Route)
## • @app.route('/dashboard')
##   def dashboard():
##        return render_template('dashboard.html')

# Module 1
# Customer Management Module
## • The Customer Management Module is a core component of the system designed to facilitate the organization, storage, retrieval, and maintenance of customer data. Built as a web-based application (indicated by the development context referencing Flask framework), this module enables users to perform key operations such as adding new customer records and searching for existing entries. It is developed with a user-centric interface and structured data handling to ensure ease of use and data accuracy.
 
# Key Features & Functionalities
 
# Add New Customer
### • Data Entry Form: A structured input section that captures essential customer details:
### • Customer ID: Unique identifier assigned to each customer to ensure record distinctiveness.
### • Customer Name: Full name of the customer.
### • Contact No.: Valid phone or mobile number for communication purposes.
### • Address: Physical location of the customer.

## Operation Buttons:
### • Save Button: A green-colored interactive button that submits and stores the entered information into the system database after basic validation.
### • Clear Button: A red-colored interactive button that resets all input fields to empty, allowing users to restart data entry without navigating away.
 
# Search and Retrieve Customer
## Search Functionality:
​• A dedicated search bar labeled "Search by ID or Name", which accepts partial or full inputs of Customer ID or Customer Name.
​• Search Button: Green-colored button that triggers the system to filter and display records matching the entered criteria.
​• Show All Button: Blue-colored button that retrieves and displays all stored customer records at once, bypassing filtering.
​
# Result Display:
​• A structured table titled "All Customers" that lists retrieved data with columns: Customer ID, Name, Contact, Address, and Actions.
​​• The table also displays the total count of available records (e.g., "All Customers (7)"), providing users with immediate visibility on data volume.

# Record Management
### • Delete Function: Under the Actions column, each customer record is paired with a red-colored Delete button. This enables authorized users to remove obsolete or incorrect records from the system.


# Module 2

# Description
## This module is used to manage appliance products in a system. It helps the user add, update, view, and delete product information in an organized way. It also makes sure that each product has correct details before being saved.

## Features
### • Add new appliances
### • Update product details
### • View available products
### • Delete products
### • Validates product information (unique ID, correct price, valid stock)

## How it works
### • User inputs product details (Product ID, Product name, price, select status)
### • User can search customers
### • System checks if Product ID is unique
### • System verifies that price is greater than 0
### • System ensures stock quantity is not negative
### • If all conditions are met, the product is saved
### • User can then view, update, or delete the product anytime

# Module 3
## Description
### • A system module for handling sales and installment transactions
### • Allows users to process purchases using cash or installment payments
### • Manages product selection, payments, and automatic computation of monthly dues

# Features / Functionalities
### • Create new sales transaction
### • Start and record a new sale
### • Select appliances to buy
### • Choose one or more items from available stock
### • Choose payment type (Cash / Installment)
### • Decide whether the payment is full or partial over time
### • Record down payment
### • Input the initial payment amount
### • Set installment term (e.g., 12 months)
### • Define how long the payment will be divided
### • Automatic monthly amortization calculation
### • System computes the monthly payment amount
### • Inventory is updated once the sale is confirmed

## Rules
### • At least one appliance must be selected
### • A payment type must be chosen
### • Down payment must not exceed the total price
### • For installment, monthly payment must be generated
### • Cannot proceed if the item is out of stock

# How It Works
## Step 1: Create transaction
### • User starts a new sale
## Step 2: Enter appliances want to buy
### • Choose items from inventory
### • System checks stock availability
## Step 3: Choose payment type
### • Cash → full payment
### • Installment → proceed to next steps
## Step 4: Enter payment details (if installment)
### • Input down payment
### • Set installment term (e.g., 12 months)
### • System calculates monthly amortization
## Step 5: Validation
### • Ensure all rules are followed (item selected, valid payment, stock available)
## Step 6: Approval
### • Transaction is approved if all conditions are met



