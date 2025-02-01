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

# Category-Wise Expense Breakdown
st.subheader("📌 Expense Breakdown by Category")
if not expenses_df.empty:
    category_data = expenses_df.groupby("category")["amount"].sum().reset_index()
    fig = px.pie(category_data, values="amount", names="category", title="Expenses by Category")
    st.plotly_chart(fig)
else:
    st.write("No expenses recorded yet.")

# Monthly Expense & Income Trends
st.subheader("📈 Monthly Expense & Income Trends")
if not expenses_df.empty and not income_df.empty:
    expenses_df["month"] = expenses_df["date"].dt.strftime("%Y-%m")
    income_df["month"] = income_df["date"].dt.strftime("%Y-%m")

    monthly_expense = expenses_df.groupby("month")["amount"].sum().reset_index()
    monthly_income = income_df.groupby("month")["amount"].sum().reset_index()

    fig = px.line(
        pd.concat([monthly_expense.assign(Type="Expense"), monthly_income.assign(Type="Income")]),
        x="month",
        y="amount",
        color="Type",
        markers=True,
        title="Monthly Expense vs Income Trend",
    )
    st.plotly_chart(fig)
else:
    st.write("Not enough data for trend analysis.")

    import cohere

# Initialize Cohere API Client 
def get_budget_insights(user_query, transactions_text):
    # Request Cohere API for budget advice
    prompt = f"""User query: {user_query}\nTransactions list: {transactions_text}\n
    You are our special financial expert. Your role here is to help users to manage finances and provide factual and practical financial tips based on their Transactions list AND User query. 
    Do not answer anything beyond that. If you encounter any question beyond finance or Transaction list then ask the user to ask something else. 
    If asked about yourself then describe yourself as a handy AI feature- named SynBot devolped by Sakshi & Shahu for Syntego Finance tracker. Do not mention it other than asked specifically. Keep your responses short & consise   """
    response = co.generate(
        model='command-xlarge-nightly',  
        prompt=prompt,
        max_tokens=100
    )
    
    # Return the response from Cohere API
    return response.generations[0].text.strip()

# Floating Chatbot Button
if "chat_visible" not in st.session_state:
    st.session_state.chat_visible = False

def toggle_chat():
    st.session_state.chat_visible = not st.session_state.chat_visible

# Floating Chatbot Button
if "chat_visible" not in st.session_state:
    st.session_state.chat_visible = False

def toggle_chat():
    st.session_state.chat_visible = not st.session_state.chat_visible


# Chatbot Button in the Center 
st.markdown(
    """
    <style>
    .chatbot-container {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        cursor: pointer;
        margin-top: 60px; /* Space above the button */
    }

    .chatbot-icon {
        background-color: #ff4b87;
        color: white;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    }

    .chatbot-name {
        background-color: white;
        color: #333;
        padding: 10px 15px;
        border-radius: 10px;
        font-size: 16px;
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
st.markdown("<br>", unsafe_allow_html=True)  

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
