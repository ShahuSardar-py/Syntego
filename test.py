import sqlite3
import streamlit as st
import pandas as pd

# Database Functions
# Connect to the SQLite database (creates the file if it doesn't exist)
def create_connection():
    return sqlite3.connect("expenses.db")

# Create the necessary table
def create_table():
    connection = create_connection()
    cursor = connection.cursor()
    
    # Create the expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        category TEXT NOT NULL
    )
    """)
    
    connection.commit()
    connection.close()

# Add a new expense
def add_expense(name, amount, description, date, category):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
    INSERT INTO expenses (name, amount, description, date, category)
    VALUES (?, ?, ?, ?, ?)
    """, (name, amount, description, date, category))
    
    connection.commit()
    connection.close()

# Retrieve all expenses
def get_expenses():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()
    
    connection.close()
    return rows

# Delete an expense by ID
def delete_expense(expense_id):
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    
    connection.commit()
    connection.close()

# Streamlit App
# Initialize the database
create_table()

# Streamlit App Title
st.title("AI Finance Manager & Expense Tracker")

# Add a New Expense Section
st.header("Add New Expense")
with st.form("expense_form", clear_on_submit=True):
    expense_name = st.text_input("Name")
    expense_amount = st.number_input("Amount", min_value=0.01, step=0.01)
    expense_description = st.text_area("Description")
    expense_date = st.date_input("Date")
    expense_category = st.selectbox("Category", ["Food", "Transport", "Utilities", "Shopping", "Other"])
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        # Add the expense to the database
        add_expense(expense_name, expense_amount, expense_description, str(expense_date), expense_category)
        st.success("Expense added successfully!")

# Display All Expenses from the Database
st.header("View All Expenses in the Database")

# Fetch all expenses
expenses = get_expenses()

if expenses:
    # Format data for display
    expenses_data = [
        {
            "ID": e[0],
            "Name": e[1],
            "Amount": e[2],
            "Description": e[3],
            "Date": e[4],
            "Category": e[5],
        }
        for e in expenses
    ]
    # Convert to DataFrame for better display
    expenses_df = pd.DataFrame(expenses_data)

    # Display as an interactive table
    st.table(expenses_df)

    # Option to Delete an Expense
    st.subheader("Delete an Expense")
    expense_id = st.number_input("Enter the ID of the expense to delete:", min_value=1, step=1)
    if st.button("Delete Expense"):
        delete_expense(expense_id)  # Function to delete the expense by ID
        st.warning("Expense deleted!", icon="⚠️")
else:
    st.write("No expenses in the database yet!")
