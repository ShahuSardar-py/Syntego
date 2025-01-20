import streamlit as st
from Home import account

#show dataframe- using st.table
def ExpenseRecord():
    st.title("Your Expense Record")
    st.caption("View all expenses here")
    expenses= account.expenseList()
    if expenses.empty:
        st.write("Looks like no expenses added yet! ")
    else:
        st.table(expenses)

def IncomeRecord():
    st.title("Your Expense Record")
    st.caption("View all expenses here")
    incomes= account.incomeList()
    if incomes.empty:
        st.write("Looks like no expenses added yet! ")
    else:
        st.table(incomes)

#deletes by ID- calls dleteexpense from ExpenseManager()
def deleteEX():
    
        st.subheader("Delete A Record")
        with st.form("delete_form"):
            index= st.number_input("enter id", min_value=0,step=1)
            deleted= st.form_submit_button("⛔")
            if deleted:
                account.deleteExpense(index)
                st.toast("Deleted Expense!")
                
            else:
                st.write("enter valid index number")

def deleteIN():
    
        st.subheader("Delete A Record")
        with st.form("delete_form2"):
            index= st.number_input("enter id", min_value=0,step=1)
            deleted= st.form_submit_button("⛔")
            if deleted:
                account.deleteIncome(index)
                st.toast("Deleted Expense!")
                
            else:
                st.write("enter valid index number")


with st.expander("Expense Record 🧾"):
    ExpenseRecord()
    deleteEX()
with st.expander("Income Records 🧾"):
    IncomeRecord()
    deleteIN()

        
