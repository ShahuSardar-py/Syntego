import sqlite3
import pandas as pd
import streamlit as st

class ExpenseManager:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                date DATE,
                                amount REAL,
                                category TEXT,
                                description TEXT)''')
        self.conn.commit()

    def addExpense(self, date, name, amount, category, description):
        self.cursor.execute('''INSERT INTO expenses (name, date, amount, category, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               (name, date, amount, category, description))
        self.conn.commit()

    def viewExpenses(self):
        query = "SELECT * FROM expenses"
        return pd.read_sql(query, self.conn)

    def deleteExpense(self, expense_id):
        self.cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        self.conn.commit()


class IncomeManager:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS income (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                date DATE,
                                amount REAL,
                                source TEXT,
                                description TEXT)''')
        self.conn.commit()

    def addIncome(self, date, name, amount, source, description):
        self.cursor.execute('''INSERT INTO income (name, date, amount, source, description)
                               VALUES (?, ?, ?, ?, ?)''', 
                               (name, date, amount, source, description))
        self.conn.commit()

    def viewIncome(self):
        query = "SELECT * FROM income"
        return pd.read_sql(query, self.conn)

    def deleteIncome(self, income_id):
        self.cursor.execute("DELETE FROM income WHERE id=?", (income_id,))
        self.conn.commit()


class Account:
    def __init__(self, db_name="expenses.db"):
        self.IncomeManager = IncomeManager(db_name)
        self.ExpenseManager = ExpenseManager(db_name)
        self.Balance = 1000000.0  

    def getBalance(self):
        total_income = self.IncomeManager.viewIncome()["amount"].sum()
        total_expense = self.ExpenseManager.viewExpenses()["amount"].sum()
        self.Balance = total_income - total_expense
        return self.Balance


    # Add expense
    def addExpense(self, date, name, amount, category, description):
        self.ExpenseManager.addExpense(date, name, amount, category, description)
        self.Balance -= amount  # Deduct from balance
        st.success(f"Expense '{name}' added successfully!")

    # Add income
    def addIncome(self, date, name, amount, source, description):
        self.IncomeManager.addIncome(date, name, amount, source, description)
        self.Balance += amount  # Add to balance
        st.success(f"Income '{name}' added successfully!")

    # View expenses
    def expenseList(self):
        return self.ExpenseManager.viewExpenses()

    # View income
    def incomeList(self):
        return self.IncomeManager.viewIncome()

    # Delete expense
    def deleteExpense(self, expense_id):
        expenses = self.ExpenseManager.viewExpenses()
        if expenses.empty:
            st.warning("No expenses to delete.")
            return

        if expense_id in expenses["id"].values:
            amount = expenses.loc[expenses["id"] == expense_id, "amount"].iloc[0]
            self.ExpenseManager.deleteExpense(expense_id)
            self.Balance += amount
            st.success(f"Expense with ID {expense_id} deleted successfully!")
        else:
            st.warning(f"Invalid Expense ID: {expense_id}")

    # Delete income
    def deleteIncome(self, income_id):
        incomes = self.IncomeManager.viewIncome()
        if incomes.empty:
            st.warning("No income records to delete.")
            return

        if income_id in incomes["id"].values:
            amount = incomes.loc[incomes["id"] == income_id, "amount"].iloc[0]
            self.IncomeManager.deleteIncome(income_id)
            self.Balance -= amount
            st.success(f"Income with ID {income_id} deleted successfully!")
        else:
            st.warning(f"Invalid Income ID: {income_id}")


    # View all income
    def incomeList(self):
        return self.IncomeManager.viewIncome()

    # View all expenses
    def expenseList(self):
        return self.ExpenseManager.viewExpenses()
