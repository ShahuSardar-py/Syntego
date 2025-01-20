import pandas as pd
import streamlit as st

# EXPENSE MANAGER
class ExpenseManager:
    def __init__(self):
        # Empty dataframe storing expenses.
        self.expenses = pd.DataFrame(columns=['Name', 'Date', 'Amount', 'Category', 'Description'])
    
    # Add new expense
    def addExpense(self, date, name, amount, category, description):
        new_expense = {"Name": name, "Date": date, "Amount": amount, "Category": category, "Description": description}
        # Concatenate the dataframe with the new expense
        self.expenses = pd.concat([self.expenses, pd.DataFrame([new_expense])], ignore_index=True)

    def deleteExpense(self, index):
        if 0 <= index < len(self.expenses):
            self.expenses = self.expenses.drop(self.expenses.index[index]).reset_index(drop=True)
        else:
            st.warning("Invalid index ⚠")
    
    def viewExpenses(self):
        # Return the complete expenses dataframe
        return self.expenses


# INCOME MANAGER
class IncomeManager:
    def __init__(self):
        self.income = pd.DataFrame(columns=['Name', 'Date', 'Amount', 'Source', 'Description'])
    
    def addIncome(self, date, name, amount, source, description):
        new_income = {"Name": name, "Date": date, "Amount": amount, "Source": source, "Description": description}
        self.income = pd.concat([self.income, pd.DataFrame([new_income])], ignore_index=True)

    def deleteIncome(self, index):
        if 0 <= index < len(self.income):
            self.income = self.income.drop(self.income.index[index]).reset_index(drop=True)
        else:
            st.warning("Invalid index ⚠")
        
    def viewIncome(self):
        return self.income


# MAIN ACCOUNT CLASS
class Account:
    def __init__(self):
        self.IncomeManager = IncomeManager()
        self.ExpenseManager = ExpenseManager()
        self.Balance = 1000000.0  # Initial balance
    
    # Income adding function
    def addIncome(self, date, name, amount, source, description):
        self.IncomeManager.addIncome(date, name, amount, source, description)
        self.Balance += amount

    # Expense adding function
    def addExpense(self, date, name, amount, category, description):
        if amount > self.Balance:
            st.warning("You have exhausted your balance ⚠")
        else:
            self.ExpenseManager.addExpense(date, name, amount, category, description)
            self.Balance -= amount
    
    # Get balance
    def getBalance(self):
        return self.Balance
    
    # Expense deletion function
    def deleteExpense(self, index):
        if 0 <= index < len(self.ExpenseManager.expenses):
            amount = self.ExpenseManager.expenses.loc[index, "Amount"]
            self.ExpenseManager.deleteExpense(index)
            self.Balance += amount
        else:
            st.warning("Invalid index ⚠")

    # Income deletion function
    def deleteIncome(self, index):
        if 0 <= index < len(self.IncomeManager.income):
            amount = self.IncomeManager.income.loc[index, "Amount"]
            self.IncomeManager.deleteIncome(index)
            self.Balance -= amount
        else:
            st.warning("Invalid index ⚠")
    
    # View all income
    def incomeList(self):
        return self.IncomeManager.viewIncome()
    
    # View all expenses
    def expenseList(self):
        return self.ExpenseManager.viewExpenses()
