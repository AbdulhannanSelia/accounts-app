import streamlit as st
from datetime import date

st.set_page_config(
    page_title="Daily Cash Tracker",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Daily Cash Tracker")
st.caption("Quick daily income & expense tracker")

# ---------------- SESSION STATE ----------------
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "incomes" not in st.session_state:
    st.session_state.incomes = []

# ---------------- DATE & BALANCE ----------------
selected_date = st.date_input("Date", value=date.today())
previous_balance = st.number_input("Previous Balance (₹)", min_value=0.0, step=100.0)

st.divider()

# ---------------- EXPENSES ----------------
st.subheader("Expenses")

expense_desc = st.text_input("Expense Description")
expense_amount = st.number_input("Expense Amount (₹)", min_value=0.0, step=50.0)

if st.button("➕ Add Expense", use_container_width=True):
    if expense_desc and expense_amount > 0:
        st.session_state.expenses.append((expense_desc, expense_amount))

expense_total = 0

for i, (desc, amt) in enumerate(st.session_state.expenses):
    col1, col2 = st.columns([5,1])
    with col1:
        st.write(f"• {desc} — ₹{amt:,.0f}")
    with col2:
        if st.button("➖", key=f"remove_exp_{i}"):
            st.session_state.expenses.pop(i)
            st.rerun()

    expense_total += amt

st.write(f"**Expense Total: ₹{expense_total:,.0f}**")

st.divider()

# ---------------- INCOME ----------------
st.subheader("Income")

income_desc = st.text_input("Income Description")
income_amount = st.number_input("Income Amount (₹)", min_value=0.0, step=50.0)

if st.button("➕ Add Income", use_container_width=True):
    if income_desc and income_amount > 0:
        st.session_state.incomes.append((income_desc, income_amount))

income_total = 0

for i, (desc, amt) in enumerate(st.session_state.incomes):
    col1, col2 = st.columns([5,1])
    with col1:
        st.write(f"• {desc} — ₹{amt:,.0f}")
    with col2:
        if st.button("➖", key=f"remove_inc_{i}"):
            st.session_state.incomes.pop(i)
            st.rerun()

    income_total += amt

st.write(f"**Income Total: ₹{income_total:,.0f}**")

st.divider()

# ---------------- CALCULATION ----------------
cash_in_hand = previous_balance + income_total - expense_total

# Build detailed lists with amounts
if st.session_state.expenses:
    expenses_text = "\n".join(
        [f"{desc} — ₹{amt:,.0f}" for desc, amt in st.session_state.expenses]
    )
else:
    expenses_text = "None"

if st.session_state.incomes:
    income_text = "\n".join(
        [f"{desc} — ₹{amt:,.0f}" for desc, amt in st.session_state.incomes]
    )
else:
    income_text = "None"

# Full report
report = f"""{selected_date.strftime('%B %d, %Y')}

EXPENSES:
{expenses_text}
------------------------------
₹{expense_total:,.0f}

INCOME:
{income_text}
------------------------------
₹{income_total:,.0f}

Previous balance:       ₹{previous_balance:,.0f}
+ Income total:         ₹{income_total:,.0f}
- Expense total:        ₹{expense_total:,.0f}
------------------------------
Cash in hand:           ₹{cash_in_hand:,.0f}
"""

# ---------------- REPORT ----------------
st.subheader("Report (Copy-Paste Ready)")

num_lines = max(len(st.session_state.expenses) + len(st.session_state.incomes) + 12, 15)
height = num_lines * 26

st.text_area("Select all and copy", report, height=height)

# ---------------- RESET ----------------
if st.button("🔄 Reset All", use_container_width=True):
    st.session_state.expenses = []
    st.session_state.incomes = []
    st.rerun()