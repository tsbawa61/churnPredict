import streamlit as st
import pandas as pd
import math

# --- a) Required Column Configuration ---
REQUIRED_COLUMNS = [
    "customer_id", "gender", "age", "country", "city", "customer_segment", 
    "tenure_months", "signup_channel", "contract_type", "monthly_logins", 
    "weekly_active_days", "avg_session_time", "features_used", "usage_growth_rate", 
    "last_login_days_ago", "monthly_fee", "total_revenue", "payment_method", 
    "payment_failures", "discount_applied", "price_increase_last_3m", 
    "support_tickets", "avg_resolution_time", "complaint_type", "csat_score", 
    "escalations", "email_open_rate", "marketing_click_rate", "nps_score", 
    "survey_response", "referral_count", "churn"
]

def main():
    st.set_page_config(page_title="Customer Grid Portal", layout="wide")
    st.title("📊 Customer Data Grid Manager")

    # --- b) File Upload Section ---
    uploaded_file = st.file_uploader("Upload Master Dataset (CSV or Excel)", type=['csv', 'xlsx'])

    if uploaded_file:
        # Load Data into Session State to maintain state across reruns
        if "master_df" not in st.session_state:
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
                
                # --- d) Transform Churn Column ---
                df['Likely to Churn'] = df['churn'].map({0: 'No', 1: 'Yes'})
                
                st.session_state.master_df = df
                st.session_state.page_index = 0
            except Exception as e:
                st.error(f"File Error: {e}")
                return

        df = st.session_state.master_df
        page_size = 5
        total_pages = math.ceil(len(df) / page_size)

        # --- c-iii) Navigation Buttons (Grid Form) ---
        st.subheader(f"Grid View (Rows {st.session_state.page_index * 5} to {min((st.session_state.page_index + 1) * 5, len(df))})")
        
        btn_col1, btn_col2, btn_col3, btn_col4 = st.columns(4)
        
        if btn_col1.button("⏮ First Set"):
            st.session_state.page_index = 0
        
        if btn_col2.button("⬅️ Previous Set") and st.session_state.page_index > 0:
            st.session_state.page_index -= 1
            
        if btn_col3.button("Next Set ➡️") and st.session_state.page_index < total_pages - 1:
            st.session_state.page_index += 1
            
        if btn_col4.button("Last Set ⏭"):
            st.session_state.page_index = total_pages - 1

        # Display the 5-row Grid
        start_row = st.session_state.page_index * page_size
        end_row = start_row + page_size
        st.table(df.iloc[start_row:end_row])

        st.divider()

        # --- c-iii) Find Record Section ---
        st.header("🔍 Find Record")
        s_col1, s_col2, s_col3, s_col4 = st.columns([2, 2, 1, 1])
        
        with s_col1:
            field = st.selectbox("Search Field", REQUIRED_COLUMNS)
        with s_col2:
            search_text = st.text_input("Enter search value")
        
        if s_col3.button("Find Records"):
            # Filtering the dataframe
            filtered_df = df[df[field].astype(str).str.contains(search_text, case=False, na=False)]
            st.session_state.search_df = filtered_df
        
        if s_col4.button("Clear Search Grid"):
            st.session_state.search_df = None

        # Display Search Results
        if "search_df" in st.session_state and st.session_state.search_df is not None:
            st.write(f"Found {len(st.session_state.search_df)} matches:")
            st.dataframe(st.session_state.search_df)

if __name__ == "__main__":
    main()