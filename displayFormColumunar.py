import streamlit as st
import pandas as pd

# --- a) Configuration: Required Columns ---
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
    st.set_page_config(page_title="ADM Customer Portal", layout="wide")
    st.title("📂 ADM Customer Data Management")

    # --- b) File Upload ---
    uploaded_file = st.file_uploader("Upload Master Excel/CSV File", type=['csv', 'xlsx'])

    if uploaded_file:
        # --- c-i) Load Data into Dataframe ---
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
                
                # --- d) Format Churn Column ---
                # Create the display version of the churn column
                df['Likely to Churn'] = df['churn'].map({0: 'No', 1: 'Yes'})
                
                st.session_state.df = df
                st.session_state.index = 0
            except Exception as e:
                st.error(f"Error: {e}")
                return

        df = st.session_state.df

        # --- c-iii) Navigation Logic ---
        st.header("📄 Individual Record View (Columnar)")
        
        col_nav1, col_nav2, col_nav3, col_nav4 = st.columns(4)
        
        if col_nav1.button("⏮ First Record"):
            st.session_state.index = 0
        if col_nav2.button("⬅️ Previous") and st.session_state.index > 0:
            st.session_state.index -= 1
        if col_nav3.button("Next ➡️") and st.session_state.index < len(df) - 1:
            st.session_state.index += 1
        if col_nav4.button("Last Record ⏭"):
            st.session_state.index = len(df) - 1

        # Display Current Record in Columnar Form
        current_record = df.iloc[st.session_state.index]
        
        # Split into 2 columns for better readability in Columnar form
        disp_col1, disp_col2 = st.columns(2)
        items = list(current_record.items())
        mid = len(items) // 2
        
        with disp_col1:
            for key, val in items[:mid]:
                st.text_input(label=key, value=val, key=f"v1_{key}", disabled=True)
        
        with disp_col2:
            for key, val in items[mid:]:
                st.text_input(label=key, value=val, key=f"v2_{key}", disabled=True)

        st.divider()

        # --- c-iii) Find Record Logic ---
        st.header("🔍 Find Record")
        search_col, search_val, search_btn, clear_btn = st.columns([2, 2, 1, 1])
        
        with search_col:
            field_to_search = st.selectbox("Select Field to Search", REQUIRED_COLUMNS)
        with search_val:
            query = st.text_input("Enter search text")
        
        if search_btn.button("Find"):
            # Filter logic (handles strings and numbers)
            results = df[df[field_to_search].astype(str).str.contains(query, case=False, na=False)]
            st.session_state.search_results = results
        
        if clear_btn.button("Clear Grid"):
            st.session_state.search_results = None

        # Display Results Grid
        if "search_results" in st.session_state and st.session_state.search_results is not None:
            st.subheader(f"Results Found: {len(st.session_state.search_results)}")
            # Show dataframe with "Likely to Churn" column as requested
            st.dataframe(st.session_state.search_results)

if __name__ == "__main__":
    main()