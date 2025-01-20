import pandas as pd
import streamlit as st


#EXPENSE MANAGER
class ExpenseManager():
    def __init__(self):
        #Empty dataframe storing expense.   
        self.expenses=pd.DataFrame(columns=['Name','Date','Amount','Category','Description'])
    
    #Add new expense
    def addExpense(self,date, name, amount,category, description):
        new_expense={"Name": name,"Date":date,"Amount":amount,"Category":category,"Description":description}
        #Concated the df expenses with the new_expense
        self.expenses=pd.concat([self.expenses,pd.DataFrame([new_expense])], ignore_index=True)

    def deleteExpense(self,index):
        if 0 <= index <len(self.expenses):
            self.expenses = self.expenses.drop(self.expenses.index[index]).reset_index(drop=True)
            
        else:
            st.warning("Invalid index ⚠")
    
    def viewExpenses(self):
        #return the complete expenses df
        return self.expenses


#INCOME MANAGER
class IncomeManager():
    def __init__(self):
         self.income=pd.DataFrame(columns=['Name','Date','Amount','Source','Description'])
    
    def addIncome(self,date, name, amount,source, description):
        new_income={"Name": name,"Date":date,"Amount":amount,"Source":source,"Description":description}
        self.income=pd.concat([self.expenses,pd.DataFrame([new_income])], ignore_index=True)

    def deleteIncome(self,index):
        if 0 <= index <len(self.income):
            self.income = self.income.drop(self.income.index[index]).reset_index(drop=True)
            
        else:
            st.warning("Invalid index ⚠")
        
    def viewIncome(self):
        return self.income



#MAIN ACCOUNT CLASS.
class Account:
    def __init__(self):
        self.IncomeManager= IncomeManager()
        self.ExpenseManager= ExpenseManager()
        self.Balance=1000000.0
    
    #income adding funtion
    def addIncome(self,name,date,amount,source, description):
        self.IncomeManager.addIncome(name,date,amount,source, description)
        self.Balance+=amount

    #expense adding function
    def addExpense(self, name, date, amount, category, description):
        self.ExpenseManager.addExpense(name,date,amount,category,description)
        if amount > self.Balance:
            st.warning("You have exausted your balance")
        else:
            self.Balance-=amount
    
    #Balance number
    def getBalance(self):
        return self.Balance
    
    #expense deletion function
    def DeleteExpense(self,index):
        self.ExpenseManager.deleteExpense(index)
        amount = self.ExpenseManager.expenses.loc[index, "Amount"]
        self.Balance+= amount
    
    #income deletion function
    def DeleteIncome(self,index):
        self.IncomeManager.deleteIncome(index)
        amount = self.IncomeManager.income.loc[index, "Amount"]
        self.Balance-= amount
    

    def IncomeList(self):
        AllIncome = self.IncomeManager.viewIncome()
        return AllIncome
    
    def ExpenseList(self):
        AllExpense = self.ExpenseManager.viewExpenses()
        return AllExpense



        
