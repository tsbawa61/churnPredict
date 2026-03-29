import streamlit as st

# Set page config
st.set_page_config(page_title="Bawa Tech Solutions", layout="wide")

# Navigation Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", 
    ["Home", "About The Company", "Churn Problem", "Documentation", "Dataset", "Feedback", "Contact"]
)

# Home Page
if page == "Home":
    st.title("Bawa Tech Solutions")
    st.subheader("AI-Powered Solutions for Smarter Business Decisions")
    st.markdown("### Explore Our Churn AI Solution")
    st.write("Welcome to Bawa Tech Consultants. We specialize in AI-driven solutions for real-world business challenges.")
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=200)  # Example icon

# About The Company
elif page == "About The Company":
    st.header("About The Company")
    st.write("""
    Bawa Tech Consultants is dedicated to building AI-driven solutions that solve real-world business challenges.
    Our mission is to empower organizations with predictive insights, automation, and intelligent tools.
    We specialize in customer retention, operational efficiency, and scalable AI applications.
    """)

# Churn Problem
elif page == "Churn Problem":
    st.header("What a Churn Problem is")
    st.write("""
    Customer churn refers to the loss of clients or subscribers over time.
    - High churn rates reduce revenue
    - Increase acquisition costs
    
    **Our Solution:** Predict churn before it happens, enabling proactive retention strategies.
    """)

# Documentation
elif page == "Documentation":
    st.header("Documentation of the Solution")
    st.write("""
    Our AI solution for churn prediction includes:
    - **Data Preprocessing:** Cleaning and preparing customer data
    - **Model Training:** Machine learning algorithms to identify churn patterns
    - **Prediction:** Early warnings for at-risk customers
    - **Benefits:** Improved retention, reduced costs, actionable insights
    """)

# Dataset
elif page == "Dataset":
    st.header("Our Dataset")
    st.write("""
    We use the **Customer Churn Prediction Business Dataset**.
    Features include customer demographics, usage patterns, and service history.
    """)
    st.markdown("[View Dataset on Kaggle](https://www.kaggle.com/datasets/miadul/customer-churn-prediction-business-dataset)")

# Feedback
elif page == "Feedback":
    st.header("Feedback")
    name = st.text_input("Name")
    email = st.text_input("Email")
    comments = st.text_area("Comments")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")

# Contact
elif page == "Contact":
    st.header("Contact")
    st.write("📍 **Address:** E803, Victoria Heights, PeerMuchalla, Zirakpur")
    st.write("📞 Get in Touch: WhatsApp Chat Link (to be integrated)")
    st.map({"lat": 30.6568, "lon": 76.8562})  # Example map for Victoria Heights
