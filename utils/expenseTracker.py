import pandas as pd
import streamlit as st

class ExpenseManager():
    def __init__(self):
        #making a empty dataframe here- this stores the expense. use this for any opreations on the expense. 
        self.expenses=pd.DataFrame(columns=['Name','Date','Amount','Description','Category'])
    
    #adding new expense
    def addExpense(self,date, name, amount,category, description):
        #a dictionary for the expense
        new_expense={"Name": name,"Date":date,"Amount":amount,"Category":category,"Description":description}
        #concated the df expenses with the new_expense
        self.expenses=pd.concat([self.expenses,pd.DataFrame([new_expense])], ignore_index=True)

    def deleteExpense(self,index):
        #uses index to delete that index number
        if 0 <= index <len(self.expenses):
            del self.expenses[index]
        else:
            st.warning("Invalid index ⚠")
    
    def viewExpenses(self):
        #return the complete expenses df
        return self.expenses


