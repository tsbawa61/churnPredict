import streamlit as st
import pandas as pd
import joblib
import os

# a) Define the required column schema
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

#Create Age Bands
def create_tenure_bands(df):
  import pandas as pd

  df['tenure_months'] = pd.to_numeric(df['tenure_months'], errors='coerce')
  df = df.dropna(subset=['tenure_months'])
  bins_tenure = [0, 12, 25, 37,df['tenure_months'].max() + 2]
  labels_tenure = ['tenure_LT12M', 'tenure_13_24M', 'tenure_25_36M', 'tenure_37+']
  df['tenure_band'] = pd.cut(df['tenure_months'], bins=bins_tenure, labels=labels_tenure, right=False)

  print("Tenure Bands created successfully.")
  print(df[['tenure_months', 'tenure_band']].head())
  print(df['tenure_band'].value_counts())
  return df

#Create Age Bands
def create_age_bands(df):
  import pandas as pd
  bins = [0, 18, 26, 36, 51, df['age'].max() + 1]
  labels = ['genZalpha', 'genZ', 'Millennials', 'genX', 'boomers+']
  df['age_band'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

  print("Age Bands created successfully.")
  print(df[['age', 'age_band']].head())
  return df

# Function to change original data to the form in which data was trained
def reform_data_for_model(df_sample):
    y_sample=df_sample['churn']
    df_sample=df_sample.drop(['churn'], axis=1)
    
    df_sample = create_age_bands(df_sample)
    df_sample = create_tenure_bands(df_sample)
    
    categorical_cols_sample = df_sample.select_dtypes(include=['object', 'category']).columns.tolist()
    categorical_cols_sample=categorical_cols_sample[1:]
    

    df_encoded_sample = pd.get_dummies(df_sample, columns=categorical_cols_sample , drop_first=True, dtype=int)

    df_encoded_sample = df_encoded_sample.drop(['tenure_months', 'age'], axis=1)
    
    X_sample=df_encoded_sample.drop(['customer_id'], axis=1)

    cols_dropped_after_variance_test  = ['country_Bangladesh', 'country_Canada', 'country_Germany', 'country_India', 'country_UK', 'country_USA', 'city_Delhi', 'city_Dhaka', 'city_London', 'city_New York', 'city_Sydney', 'city_Toronto', 'email_open_rate', 'usage_growth_rate', 'marketing_click_rate']

    Final_X_sample = X_sample.drop(cols_dropped_after_variance_test , axis=1)

    cols_dropped_after_VIF_test=  ['age_band_boomers+', 'csat_score', 'total_revenue', 'avg_resolution_time', 'customer_segment_Individual', 'features_used', 'avg_session_time']

    Final_X_sample = Final_X_sample.drop(cols_dropped_after_VIF_test , axis=1)
    
    cols_used_for_training = ['monthly_logins',
    'weekly_active_days',
    'last_login_days_ago',
    'monthly_fee',
    'payment_failures',
    'support_tickets',
    'escalations',
    'nps_score',
    'referral_count',
    'gender_Male',
    'customer_segment_SME',
    'signup_channel_Referral',
    'signup_channel_Web',
    'contract_type_Quarterly',
    'contract_type_Yearly',
    'payment_method_Card',
    'payment_method_PayPal',
    'discount_applied_Yes',
    'price_increase_last_3m_Yes',
    'complaint_type_Service',
    'complaint_type_Technical',
    'survey_response_Satisfied',
    'survey_response_Unsatisfied',
    'tenure_band_tenure_13_24M',
    'tenure_band_tenure_25_36M',
    'tenure_band_tenure_37+',
    'age_band_genZ',
    'age_band_Millennials',
    'age_band_genX']

    # Note: The following step ensures that our model was trained on these exact column names/order.
    Final_X_sample=Final_X_sample[cols_used_for_training]
    
    return Final_X_sample


# d) Function to load model and predict
def is_churned(Final_X_sample):
    """
    Loads a joblib model and predicts churn.
    Note: Ensure your model was trained on these exact column names/order.
    """
    # # 1. Load the saved objects
    import joblib
    import numpy as np


    # # 1. Load the scaler, if requied and the ML Model
    #loaded_scaler = joblib.load(folder_Modelling_data+'/standard_scaler.joblib')
    loaded_scaler = joblib.load('standard_scaler.joblib')
    loaded_model = joblib.load('model_with_scaling.joblib')


    # # 2. New incoming data (raw features)
    # new_data = np.array([[22, 7.25, 1, 0, 0, 1]]) # Example raw features
    # Our new incoming data is Final_X_sample

    # # # 3. Apply the SAME scaling that was used during training phase, which is in the variable loaded_scaler
    X_sample_scaled = loaded_scaler.transform(Final_X_sample)

      # # # 4. Predict!
    prediction = loaded_model.predict(X_sample_scaled)
    print(f"Churn Prediction: {prediction}")

    # path = '/content/drive/MyDrive/Colab Notebooks/My Projects/Subscription Churn/Modelling/input/Sample_From_Customer_Churn_business_dataset.xlsx'

    # df_sample2 = pd.read_excel(path)
    # y_sample=df_sample2['churn']
    # df_sample2['churn'] = prediction
    # df_sample2.head()
    # modelPerformance(y_sample, prediction)
    # In case prediction is poor give error message



    return prediction

def main():
    st.set_page_config(page_title="Churn Prediction Portal", layout="wide")
    st.title("📊 Customer Churn Prediction Dashboard")

    # b) File Upload Section (Supports local disk/Drive/OneDrive via browser)
    st.sidebar.header("Upload Settings")
    uploaded_file = st.sidebar.file_uploader("Upload Excel or CSV file", type=['csv', 'xlsx'])

    if uploaded_file is not None:
        try:
            # c-i) Store data in a dataframe
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)

            # c-ii) Schema Validation
            # Trim whitespace from columns to prevent matching errors
            df.columns = [col.strip() for col in df.columns]
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]

            if missing_cols:
                st.error(f"❌ Column Mismatch! Missing columns: {', '.join(missing_cols)}")
            else:
                st.success("✅ File uploaded and validated successfully!")

                # e) Run prediction and add 'churn' column
                # We only pass the required columns to the model to avoid errors with extra columns
                input_data = df[REQUIRED_COLUMNS]
                
                with st.spinner('Running Churn Prediction Model...'):
                    Final_X_sample=reform_data_for_model(input_data)
                    predictions = is_churned(Final_X_sample)
                    
                if predictions is not None:
                    df['churn'] = predictions

                    # f) Display dataframe with formatted churn
                    st.subheader("Inference Results")
                    
                    # Create a display-ready dataframe
                    display_df = df.copy()
                    display_df['Likely to Churn'] = display_df['churn'].map({0: 'No', 1: 'Yes'})
                    
                    # Optional: Drop the original numeric churn column for the final display
                    cols_to_show = [c for c in display_df.columns if c != 'churn']
                    st.dataframe(display_df[cols_to_show])

                    # Download Button for the results
                    csv = display_df.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Download Predictions", csv, "churn_predictions.csv", "text/csv")

        except Exception as e:
            st.error(f"An error occurred while processing: {e}")

if __name__ == "__main__":
    main()