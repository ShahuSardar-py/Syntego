import streamlit as st
from Home import manager

def View():
    st.title("Your Expenses")
    st.caption("View all expenses here")
    expenses= manager.viewExpenses()
    if expenses.empty:
        st.write("Looks like no expenses added yet! ")
    else:
        st.table(expenses)

def delete():
    st.header("Delete expense")
    with st.expander("delete"):
        with st.form("delete_form"):
            index= st.number_input("enter id", min_value=0,step=1)
            deleted= st.form_submit_button("DSeleteee")
            if deleted:
                manager.deleteExpense(index)
            else:
                st.write("invaslid!!E")


View()
delete()

        
