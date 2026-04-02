import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Bawa Tech Solutions",
    page_icon="🤖",
    layout="wide"
)

# 2. Company Branding & Header
st.title("Bawa Tech Solutions")
st.subheader("Bawa Tech Consultants: Leading AI-Driven Churn Solutions")

# 3. Sidebar Navigation
st.sidebar.title("Navigation")
selection = st.sidebar.radio(
    "Select a Service:",
    [
        "Customer Input Form", 
        "Display Data (Grid)", 
        "Display Data (Columnar)", 
        "Churn Prediction (Upload Excel)"
    ]
)

# 4. Routing Logic
# This section imports and runs the code from your 'src' folder based on selection
try:
    if selection == "Customer Input Form":
        from src import CustomerInputForm
        CustomerInputForm.main() # Assumes your files have a main() function

    elif selection == "Display Data (Grid)":
        from src import displayFormGrid
        displayFormGrid.main()

    elif selection == "Display Data (Columnar)":
        from src import displayFormColumunar
        displayFormColumunar.main()

    elif selection == "Churn Prediction (Upload Excel)":
        from src import uploadExcelFile
        uploadExcelFile.main()

except ImportError as e:
    st.error(f"Error: Could not find the source file in the 'src' folder. {e}")
except AttributeError:
    st.warning("Note: Please ensure each file in the 'src' folder has a 'def main():' function wrapping the code.")

# 5. Footer
st.sidebar.markdown("---")
st.sidebar.info("© 2026 Bawa Tech Consultants")