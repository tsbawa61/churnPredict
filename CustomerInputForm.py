import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Setup Page
st.set_page_config(page_title="Churn Data Entry", layout="wide")

def main():
    st.title("📂 Customer Churn Business Dataset - Entry Portal")
    
    # 2. Load the existing file from your local path/upload
    # Replace 'customer_churn_business_dataset.csv' with your actual filename
    file_path = 'customer_churn_business_dataset.csv'
    
    if os.path.exists(file_path):
        df_master = pd.read_csv(file_path)
        st.sidebar.success(f"Connected to Master File: {len(df_master)} records found.")
    else:
        st.sidebar.warning("Master file not found. A new one will be created upon submission.")
        df_master = pd.DataFrame()

    # 3. Create the Input Form
    with st.form("main_entry_form", clear_on_submit=True):
        st.header("New Record Entry")
        
        # --- ROW 1: Identity & Demographics ---
        row1_1, row1_2, row1_3, row1_4 = st.columns(4)
        with row1_1:
            customer_id = st.text_input("Customer ID")
        with row1_2:
            gender = st.selectbox("Gender", ["Male", "Female"])
        with row1_3:
            age = st.number_input("Age", 18, 100, 30)
        with row1_4:
            country = st.selectbox("Country", ["Bangladesh", "Canada", "Germany", "Australia", "India", "USA", "UK"])

        # --- ROW 2: Geography & Segment ---
        row2_1, row2_2, row2_3 = st.columns(3)
        with row2_1:
            city = st.selectbox("City", ["London", "Sydney", "New York", "Dhaka", "Delhi", "Toronto", "Berlin"])
        with row2_2:
            customer_segment = st.selectbox("Customer Segment", ["SME", "Individual", "Enterprise"])
        with row2_3:
            signup_channel = st.selectbox("Signup Channel", ["Web", "Mobile", "Referral"])

        st.divider()

        # --- ROW 3: Usage Metrics ---
        st.subheader("Usage & Engagement Metrics")
        row3_1, row3_2, row3_3, row3_4 = st.columns(4)
        with row3_1:
            tenure_months = st.number_input("Tenure (Months)", 0)
        with row3_2:
            monthly_logins = st.number_input("Monthly Logins", 0)
        with row3_3:
            weekly_active_days = st.slider("Weekly Active Days", 0, 7, 0)
        with row3_4:
            avg_session_time = st.number_input("Avg Session Time (Min)", 0.0)

        row4_1, row4_2, row4_3, row4_4 = st.columns(4)
        with row4_1:
            features_used = st.number_input("Features Used", 0)
        with row4_2:
            usage_growth_rate = st.number_input("Usage Growth Rate", format="%.2f")
        with row4_3:
            last_login_days_ago = st.number_input("Last Login (Days Ago)", 0)
        with row4_4:
            referral_count = st.number_input("Referral Count", 0)

        st.divider()

        # --- ROW 5: Contract & Billing ---
        st.subheader("Financials & Billing")
        row5_1, row5_2, row5_3 = st.columns(3)
        with row5_1:
            contract_type = st.selectbox("Contract Type", ["Monthly", "Yearly", "Quarterly"])
        with row5_2:
            payment_method = st.selectbox("Payment Method", ["PayPal", "Card", "Bank Transfer"])
        with row5_3:
            payment_failures = st.number_input("Payment Failures", 0)

        row6_1, row6_2, row6_3, row6_4 = st.columns(4)
        with row6_1:
            monthly_fee = st.number_input("Monthly Fee", 0)
        with row6_2:
            total_revenue = st.number_input("Total Revenue", 0)
        with row6_3:
            discount_applied = st.selectbox("Discount Applied", ["Yes", "No"])
        with row6_4:
            price_increase_last_3m = st.selectbox("Price Increase (Last 3m)", ["Yes", "No"])

        st.divider()

        # --- ROW 7: Support & Satisfaction ---
        st.subheader("Support & Marketing")
        row7_1, row7_2, row7_3 = st.columns(3)
        with row7_1:
            support_tickets = st.number_input("Support Tickets", 0)
        with row7_2:
            avg_resolution_time = st.number_input("Avg Resolution Time (Hrs)", 0.0)
        with row7_3:
            complaint_type = st.selectbox("Complaint Type", ["Service", "Billing", "Technical", "None"])

        row8_1, row8_2, row8_3, row8_4, row8_5 = st.columns(5)
        with row8_1:
            csat_score = st.slider("CSAT Score", 1, 5, 3)
        with row8_2:
            escalations = st.number_input("Escalations", 0)
        with row8_3:
            email_open_rate = st.number_input("Email Open Rate", 0.0, 1.0)
        with row8_4:
            marketing_click_rate = st.number_input("Marketing Click Rate", 0.0, 1.0)
        with row8_5:
            nps_score = st.slider("NPS Score", -100, 100, 0)

        row9_1 = st.selectbox("Survey Response", ["Satisfied", "Neutral", "Unsatisfied"])

        # SUBMIT BUTTON
        submit_clicked = st.form_submit_button("Add Record to Dataset")

    # 4. Processing the Submission
    if submit_clicked:
        # Create dictionary of inputs
        new_row_data = {
            "customer_id": customer_id, "gender": gender, "age": age, "country": country,
            "city": city, "customer_segment": customer_segment, "tenure_months": tenure_months,
            "signup_channel": signup_channel, "contract_type": contract_type, "monthly_logins": monthly_logins,
            "weekly_active_days": weekly_active_days, "avg_session_time": avg_session_time,
            "features_used": features_used, "usage_growth_rate": usage_growth_rate,
            "last_login_days_ago": last_login_days_ago, "monthly_fee": monthly_fee,
            "total_revenue": total_revenue, "payment_method": payment_method,
            "payment_failures": payment_failures, "discount_applied": discount_applied,
            "price_increase_last_3m": price_increase_last_3m, "support_tickets": support_tickets,
            "avg_resolution_time": avg_resolution_time, "complaint_type": complaint_type,
            "csat_score": csat_score, "escalations": escalations, "email_open_rate": email_open_rate,
            "marketing_click_rate": marketing_click_rate, "nps_score": nps_score,
            "survey_response": row9_1, "referral_count": referral_count
        }

        # Create DataFrame for the new row
        new_entry_df = pd.DataFrame([new_row_data])

        # Append to master dataframe using pd.concat
        updated_df = pd.concat([df_master, new_entry_df], ignore_index=True)

        # 5. Save back to CSV
        updated_df.to_csv(file_path, index=False)
        
        st.success(f"Successfully added record for {customer_id}!")
        st.balloons()
        st.write("Preview of updated dataset (Last 5 rows):")
        st.dataframe(updated_df.tail())

if __name__ == "__main__":
    main()