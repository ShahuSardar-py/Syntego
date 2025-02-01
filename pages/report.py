import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from dotenv import load_dotenv
import cohere
from utils.test import Account  

# Load environment variables
load_dotenv()

# Initialize Cohere API Client
api_key = os.getenv('COHERE_API_KEY')
co = cohere.Client(api_key)

# Ensure user is logged in
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in first.")
    st.stop()

user_email = st.session_state.user_email
db_name = f"{user_email}.db"
account = Account(db_name=db_name)

st.title("📊 Financial Reports")

# Fetch Expenses & Income
expenses_df = account.expenseList()
income_df = account.incomeList()

# Convert Date Columns to DateTime
if not expenses_df.empty:
    expenses_df['date'] = pd.to_datetime(expenses_df['date'])
if not income_df.empty:
    income_df['date'] = pd.to_datetime(income_df['date'])

# Create layout for side-by-side Pie Charts
col1, col2 = st.columns(2)

# Expense Breakdown
with col1:
    st.subheader("📌 Expense Breakdown by Category")
    if not expenses_df.empty:
        category_data = expenses_df.groupby("category")["amount"].sum().reset_index()
        fig_expense_pie = px.pie(
            category_data,
            values="amount",
            names="category",
            title="Expenses by Category",
            hole=0.4
        )
        st.plotly_chart(fig_expense_pie)
    else:
        st.write("No expenses recorded yet.")

# Income Breakdown
with col2:
    st.subheader("💰 Income Breakdown by Source")
    if not income_df.empty:
        income_data = income_df.groupby("source")["amount"].sum().reset_index()
        fig_income_pie = px.pie(
            income_data,
            values="amount",
            names="source",
            title="Income Breakdown by Category",
            hole=0.4
        )
        st.plotly_chart(fig_income_pie)
    else:
        st.write("No income recorded yet.")

import plotly.express as px

# Check if data exists
st.subheader("📊 Monthly Expense & Income Trends")
if not expenses_df.empty and not income_df.empty:
    expenses_df["month"] = expenses_df["date"].dt.strftime("%Y-%m")
    income_df["month"] = income_df["date"].dt.strftime("%Y-%m")

    monthly_expense = expenses_df.groupby("month")["amount"].sum().reset_index()
    monthly_income = income_df.groupby("month")["amount"].sum().reset_index()

    # Create an area chart (stacked)
    fig = px.area(
        pd.concat([monthly_expense.assign(Type="Expense"), monthly_income.assign(Type="Income")]),
        x="month",
        y="amount",
        color="Type",
        title="Monthly Expense vs Income Trend",
        line_group="Type",  # Ensures the area is stacked by type
        markers=True
    )
    st.plotly_chart(fig)
else:
    st.write("Not enough data for trend analysis.")

# Bar Chart: Monthly Spending by Category
st.subheader("📊 Monthly Spending by Category")
if not expenses_df.empty:
    category_monthly_data = expenses_df.groupby(["month", "category"])["amount"].sum().reset_index()
    fig_category_bar = px.bar(category_monthly_data, x="month", y="amount", color="category", barmode="group", title="Monthly Spending by Category")
    st.plotly_chart(fig_category_bar)
else:
    st.write("No spending data available.")


# Stacked Bar Chart: Income vs Expenses
st.subheader("📊 Income vs Expenses (Stacked View)")
if not expenses_df.empty and not income_df.empty:
    stacked_data = pd.concat([
        monthly_expense.assign(Type="Expense"),
        monthly_income.assign(Type="Income")
    ])
    fig_stacked_bar = px.bar(stacked_data, x="month", y="amount", color="Type", barmode="stack", title="Stacked Income vs Expenses")
    st.plotly_chart(fig_stacked_bar)
else:
    st.write("Not enough data for stacked comparison.")

# Initialize Cohere API Client 
def get_budget_insights(user_query, transactions_text):
    # Request Cohere API for budget advice
    prompt = f"""User query: {user_query}\nTransactions list: {transactions_text}\n
    You are SynBot, a financial AI assistant developed by Sakshi & Shahu for the Syntego Finance Tracker.
    
    Your job is **ONLY** to assist users with their **financial queries**, including budgeting, expense tracking, and savings advice. **DO NOT** answer anything that is unrelated to finance. If a user asks something outside finance, firmly respond with: 
    "I can only assist with financial-related questions. Please ask me something about your finances."
    If user asks about making changes his expenses or income to delete or add ,simply respond:""I can assist you with managing your finances, but I cannot make changes to your expenses or income. You can update or modify them on the respective pages. Let me know if you'd like help with anything else!"
    If the user asks about **yourself**, simply respond:
    "I am SynBot, a financial assistant built by Sakshi & Shahu to help with budgeting and expense management."""

    response = co.generate(
        model='command-xlarge-nightly',  
        prompt=prompt,
        max_tokens=100
    )
    
    # Return the response from Cohere API
    return response.generations[0].text.strip()

# Floating Chatbot Button in Sidebar
with st.sidebar:
    st.markdown(
        """
        <style>
        .chatbot-container {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
            margin-bottom: 20px;
        }

        .chatbot-icon {
            background-color: #ff4b87;
            color: white;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            font-size: 20px;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
        }

        .chatbot-name {
            background-color: white;
            color: #333;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.2);
        }
        </style>
        <div class="chatbot-container" onclick="document.getElementById('chat_expander').click();">
            <div class="chatbot-icon">🤖</div>
            <div class="chatbot-name">SynBot - AI Assistant</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Expander for AI Chat (appears when button is clicked)
    with st.expander("💬 Chat with SynBot - AI Assistant", expanded=False):
        st.write(f"👋 Hi {st.session_state.user_email.split('@')[0]}! Ask me about your finances.")

        user_query = st.text_input("💬 Enter your question:")

        if st.button("💡 Get AI Budget Advice"):
            if user_query.strip():
                transactions_text = account.format_transactions_for_ai()
                budget_tip = get_budget_insights(user_query, transactions_text)
                st.write(budget_tip)
            else: 
                st.warning("Please enter a valid question.")
