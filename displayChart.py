import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math
import random
from random import randint
import traceback

# --- a) Required Column Schema ---
REQUIRED_COLUMNS = [
    "customer_id", "gender", "age", "country", "city", "customer_segment", 
    "tenure_months", "signup_channel", "contract_type", "monthly_logins", 
    "weekly_active_days", "avg_session_time", "features_used", "usage_growth_rate", 
    "last_login_days_ago", "monthly_fee", "total_revenue", "payment_method", 
    "payment_failures", "discount_applied", "price_increase_last_3m", 
    "support_tickets", "avg_resolution_time", "complaint_type", "csat_score", 
    "escalations", "email_open_rate", "marketing_click_rate", "nps_score", 
    "survey_response", "referral_count"
]

# Identify categorical fields for the dropdown analysis
CATEGORICAL_FIELDS = [
    "gender", "country", "city", "customer_segment", "signup_channel", 
    "contract_type", "payment_method", "discount_applied", 
    "price_increase_last_3m", "complaint_type", "survey_response"
]

def main():
    st.set_page_config(page_title="Data Grid & Analysis Portal", layout="wide")
    st.title("📊 Customer Data Explorer & Visualizer")

    # --- b) File Upload ---
    uploaded_file = st.file_uploader("Upload Excel or CSV File", type=['csv', 'xlsx'])

    if uploaded_file:
        # Initialize session state for data and navigation
        if "df" not in st.session_state:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                
                # --- c-ii) Column Validation ---
                df.columns = [c.strip() for c in df.columns]
                missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
                
                if missing:
                    st.error(f"❌ Column Mismatch! Missing: {', '.join(missing)}")
                    return
                
                # --- d) Transform Churn for display ---
                if 'churn' in REQUIRED_COLUMNS:
                    df['Likely to Churn'] = df['churn'].map({0: 'No', 1: 'Yes'})
                
                st.session_state.df = df
                st.session_state.page_index = 0
                st.session_state.show_chart = False
            except Exception as e:
                st.error(f"Error: {e}")
                # 1. Display a user-friendly error message
                st.error(f"⚠️ An unexpected error occurred in the application: {e}")

                # 2. Extract the full traceback as a string
                error_details = traceback.format_exc()

                # 3. Use an expander to hide the technical details
                with st.expander("See full error details (Traceback)"):
                    st.code(error_details, language="python")
                return

        df = st.session_state.df
        page_size = 5
        total_pages = math.ceil(len(df) / page_size)

        # --- c-i & c-iii) Grid Display & Navigation ---
        st.header("📋 Data Grid (5 Rows Per Page)")
        
        col1, col2, col3, col4 = st.columns(4)
        if col1.button("⏮ First Set"):
            st.session_state.page_index = 0
        if col2.button("⬅️ Previous Set") and st.session_state.page_index > 0:
            st.session_state.page_index -= 1
        if col3.button("Next Set ➡️") and st.session_state.page_index < total_pages - 1:
            st.session_state.page_index += 1
        if col4.button("Last Set ⏭"):
            st.session_state.page_index = total_pages - 1

        # Calculate current slice
        start_idx = st.session_state.page_index * page_size
        end_idx = start_idx + page_size
        
        st.markdown(f"**Showing records {start_idx} to {min(end_idx, len(df))} of {len(df)}**")
        st.table(df.iloc[start_idx:end_idx])

        st.divider()

        # --- c-iv & c-v) Categorical Analysis & Charting ---
        st.header("📈 Categorical Frequency Distribution")
        
        analysis_col, btn_col = st.columns([3, 1])
        
        with analysis_col:
            selected_field = st.selectbox("Select Categorical Field to Analyze", CATEGORICAL_FIELDS)
        
        with btn_col:
            st.write("##") # Spacing
            if st.button("Generate Chart"):
                st.session_state.show_chart = True
            if st.button("Clear Chart"):
                st.session_state.show_chart = False

        if st.session_state.show_chart:
            # Generate the plot
            fig, ax = plt.subplots(figsize=(10, 6))
            counts = df[selected_field].value_counts()
            
            # Generates a random number from 0 to 16,777,215 (FFFFFF in hex)
            colour = "#%06x" % random.randint(0, 0xFFFFFF)
            # Create the bars
            bars = ax.bar(counts.index, counts.values, color=colour, edgecolor='black') #'skyblue'
            
            # --- NEW: Add labels/values on top of bars ---
            ax.bar_label(bars, padding=3, fontsize=10, fontweight='bold')
            
            ax.set_title(f"Frequency Distribution: {selected_field}", fontsize=14)
            ax.set_xlabel(selected_field, fontsize=12)
            ax.set_ylabel("Number of Customers", fontsize=12)
            plt.xticks(rotation=45)
            
            # Adjust y-axis limit to give space for labels
            ax.set_ylim(0, counts.max() * 1.1)
            plt.tight_layout()
            st.pyplot(fig)

if __name__ == "__main__":
    main()