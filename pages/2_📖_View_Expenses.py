import streamlit as st
from Home import account

#show dataframe- using st.table
def View():
    st.title("Your Expenses")
    st.caption("View all expenses here")
    expenses= account.ExpenseList()
    if expenses.empty:
        st.write("Looks like no expenses added yet! ")
    else:
        st.table(expenses)

#deletes by ID- calls dleteexpense from ExpenseManager()
def delete():
    st.header("Delete expense")
    with st.expander("delete"):
        with st.form("delete_form"):
            index= st.number_input("enter id", min_value=0,step=1)
            deleted= st.form_submit_button("⛔")
            if deleted:
                account.deleteExpense(index)
                st.toast("Deleted Expense!")
                
            else:
                st.write("enter valid index number")


View()
delete()

        
