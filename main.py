# app.py - Main multi-page application
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sys
import openpyxl
from pathlib import Path
import plotly.express as px
from io import BytesIO

# Configure page settings
st.set_page_config(
    page_title="Startup Prediction & Analytics Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "login"
if 'df' not in st.session_state:
    st.session_state.df = None


# Cache the model loading
@st.cache_resource
def load_model():
    """Load the machine learning model with caching"""
    try:
        model_path = "startup_model.sav"
        if Path(model_path).exists():
            with open(model_path, 'rb') as file:
                return pickle.load(file)
        else:
            original_path = "D:\\Successed Project\\Startup-Company-Prediction-Machine-Learning\\startup_model.sav"
            with open(original_path, 'rb') as file:
                return pickle.load(file)
    except FileNotFoundError:
        st.error("Model file not found. Please ensure startup_model.sav is in the correct location.")
        return None
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None


# Cache user credentials loading
@st.cache_data(ttl=60)
def load_user_credentials():
    """Load user credentials with caching"""
    try:
        return pd.read_excel("user_credentials.xlsx")
    except FileNotFoundError:
        return pd.DataFrame(columns=['Username', 'Password', 'Name', 'Age', 'Sex', 'Working Status', 'Company Name'])
    except Exception as e:
        st.error(f"Error loading user credentials: {str(e)}")
        return pd.DataFrame(columns=['Username', 'Password', 'Name', 'Age', 'Sex', 'Working Status', 'Company Name'])


# Cache category mappings
@st.cache_data
def get_category_mappings():
    """Get all category mappings with caching"""

    categories_dict = {
        'Cloud Computing': 1, 'Market Research|Marketing|Crowdfunding': 2,
        'Analytics|Cloud Computing|Software Development': 3, 'Mobile|Analytics': 4,
        'Analytics|Marketing|Enterprise Software': 5, 'Food & Beverages|Hospitality': 6,
        'Analytics': 7, 'Cloud Computing|Network / Hosting / Infrastructure': 8,
        'Analytics|Mobile|Marketing': 9, 'Healthcare|Pharmaceuticals|Analytics': 10,
        'Analytics|Enterprise Software': 11, 'Media|Finance|Marketing': 12,
        'Music|Analytics': 13, 'E-Commerce|Gaming|Analytics': 14,
        'Healthcare|Analytics': 15, 'Marketing': 16, 'Advertising|Retail|Mobile': 17,
        'Mobile|Retail': 18, 'Analytics|Finance': 19, 'Software Development': 20,
        'Marketing|Software Development|Analytics': 21, 'Security': 22,
        'Advertising': 23, 'Marketing|Email': 24,
        'Analytics|Security|Network / Hosting / Infrastructure': 25,
        'Human Resources (HR)|Marketing|Career / Job Search': 26,
        'Cloud Computing|Healthcare|E-Commerce': 27,
        'Media|Analytics|Publishing|Mobile|Education': 28,
        'E-Commerce|Energy|Media': 29, 'Media|Analytics': 30,
        'Advertising|Marketing|Analytics': 31, 'E-Commerce|Analytics': 32,
        'E-Commerce|Advertising|Analytics': 33, 'Enterprise Software': 34,
        'Analytics|Advertising|Cloud Computing|Marketing': 35,
        'Analytics|Network / Hosting / Infrastructure': 36,
        'Finance': 37, 'E-Commerce|Marketing': 38, 'Education|E-Commerce|Mobile': 39,
        'E-Commerce|Retail|Marketing|Mobile|Advertising|Deals': 40,
        'Analytics|Market Research|Mobile': 41, 'Advertising|Mobile|Analytics': 42,
        'Media|Analytics|Entertainment': 43, 'Analytics|Retail|Mobile': 44,
        'Analytics|Cloud Computing': 45, 'Transportation|Analytics': 46,
        'Analytics|Publishing|Mobile': 47, 'Analytics|Mobile': 48,
        'Human Resources (HR)|Enterprise Software|Career / Job Search|Social Networking|Analytics': 49,
        'Analytics|Marketing': 50, 'Media|Marketing|Analytics': 51,
        'Analytics|Food & Beverages|Social Networking|Mobile': 52,
        'E-Commerce|Analytics|Advertising|Mobile': 53,
        'Media|Advertising|Analytics|Marketing': 54,
        'E-Commerce|Retail|Analytics': 55, 'Social Networking': 56,
        'Healthcare': 57, 'E-Commerce|Mobile': 58, 'Real Estate': 59,
        'E-Commerce': 60,
        'Mobile|Advertising|Social Networking|Marketing|E-Commerce|Analytics|Enterprise Software': 61,
        'Network / Hosting / Infrastructure|Food & Beverages|Analytics': 62,
        'Analytics|E-Commerce|Marketing': 63, 'Retail': 64, 'Market Research': 65,
        'Retail|Mobile': 66, 'Mobile|Marketing': 67,
        'Network / Hosting / Infrastructure': 68, 'Real Estate|Mobile|E-Commerce': 69,
        'Media|Entertainment|Analytics|Network / Hosting / Infrastructure|Publishing': 70,
        'E-Commerce|Email|Analytics|Marketing': 71,
        'Analytics|Crowdfunding|Search|Marketing': 72, 'Analytics|Healthcare': 73,
        'Network / Hosting / Infrastructure|Enterprise Software|Software Development|Analytics': 74,
        'Analytics|Telecommunications': 75, 'Marketing|Enterprise Software|Analytics': 76,
        'Media': 77, 'Mobile': 78, 'E-Commerce|Food & Beverages|Mobile': 79,
        'Education': 80, 'Social Networking|Mobile': 81,
        'Entertainment|Media|Mobile': 82, 'Search': 83,
        'Advertising|Gaming|Marketing': 84, 'Analytics|Insurance': 85,
        'E-Commerce|Retail|Mobile': 86, 'Gaming|CleanTech|Social Networking|Energy': 87,
        'Advertising|Media|Mobile|Marketing': 88,
        'Analytics|Software Development|Marketing': 89, 'Space Travel': 90,
        'Search|Enterprise Software|Mobile': 91,
        'Analytics|Marketing|Software Development': 92,
        'Analytics|Security|Enterprise Software': 93, 'Media|Publishing': 94,
        'Analytics|Social Networking|Email': 95, 'Media|Analytics|Marketing': 96,
        'E-Commerce|Finance': 97, 'Analytics|Energy': 98,
        'CleanTech|Analytics|Energy': 99, 'Marketing|Analytics': 100,
        'Retail|Analytics': 101,
        'Analytics|Enterprise Software|Cloud Computing|Software Development': 102,
        'Advertising|Market Research': 103, 'Enterprise Software|Software Development': 104,
        'Energy': 105, 'CleanTech|Analytics|Real Estate|Energy': 106,
        'Security|Cloud Computing': 107, 'CleanTech|Energy': 108,
        'E-Commerce|Enterprise Software|Analytics': 109,
        'E-Commerce|Analytics|Mobile|Retail': 110, 'Entertainment': 111,
        'Music': 112, 'Analytics|E-Commerce': 113,
        'Network / Hosting / Infrastructure|Analytics': 114,
        'E-Commerce|Publishing|Marketing': 115,
        'E-Commerce|Market Research|Analytics|Deals|Finance': 116,
        'Cloud Computing|Energy': 117,
        'Network / Hosting / Infrastructure|Enterprise Software': 118,
        'Career / Job Search': 119, 'Advertising|Analytics': 120,
        'Analytics|Retail|Mobile|Enterprise Software|Market Research': 121,
        'Cloud Computing|E-Commerce|Analytics': 122, 'Analytics|Retail': 123,
        'Search|Social Networking': 124, 'Telecommunications': 125,
        'Publishing': 126, 'Network / Hosting / Infrastructure|Publishing': 127,
        'Classifieds|Network / Hosting / Infrastructure': 128,
        'Media|Advertising|E-Commerce': 129, 'Search|Healthcare': 130,
        'Mobile|Telecommunications': 131, 'Cloud Computing|E-Commerce|Classifieds': 132,
        'Gaming|Entertainment': 133, 'Food & Beverages': 134,
        'Marketing|Mobile|E-Commerce': 135,
        'Mobile|Cloud Computing|Enterprise Software': 136,
        'Music|Media|Software Development': 137, 'Analytics|Advertising': 138,
        'E-Commerce|Analytics|Advertising|Enterprise Software': 139,
        'Cloud Computing|Analytics': 140
    }

    focus_functions_dict = {
        'marketing': 1, 'Marketing, sales': 2, 'operations': 3, 'Marketing & Sales': 4,
        'analytics': 5, 'Research': 6, 'Computing': 7, 'Marketing': 8,
        'Sales, marketing': 9, 'Marketing \nsales': 10, 'Technology': 11,
        'marketing, sales': 12, 'Data Management': 13, 'Solution providing': 14,
        'Social Media': 15, 'targeted marketing': 16, 'Community Betterment': 17,
        'Web Analytics': 18, 'Strategy': 19, 'Bug fix': 20, 'Data Integration': 21,
        'malware protection': 22, 'Analytics': 23, 'Social Media optimization': 24,
        'Database Management': 25, 'technology': 26, 'Operations': 27, 'Sales': 28,
        'Risk': 29, 'Marketing, Web Analytics': 30,
        'Strategy, Operations, Finacial Planning': 31, 'Data Collection': 32,
        'marketiing': 33, 'sales': 34, 'e-learning': 35, 'software service': 36,
        'mobile app': 37, 'application': 38, 'analytic': 39, 'software ': 40,
        'SOCIAL MEDIA': 41, 'SOCIAL MEDIA management': 42, 'OPERATIONS': 43,
        'MARKETING': 44, 'PERSONAL APPS': 45, 'consumer behaviour': 46,
        'customer servce': 47, 'CUSTOMER SERVICE': 48, 'APP REVENUE': 49,
        'intellectual property analysis and visualisation': 50, 'retail': 51,
        'data visualization': 52, 'service': 53, 'social media': 54,
        'security': 55, 'operation': 56, 'Marketing, Sales': 57,
        'operations, sales, marketing': 58, 'research': 59,
        'Marketing, Technology, Finance & Accounting, Customer service': 60,
        'Computing, training': 61, 'Operations, marketing': 62,
        'social advertising': 63, 'risk': 64, 'data collection ': 65,
        'development, marketing, and administration': 66, 'IT & Sales': 67,
        'social news': 68, 'web': 69, 'sale': 70, 'Sales & Marketing': 71,
        'social network': 72, 'consumer web': 73, 'writing blog': 74,
        'curated web': 75, 'Recommendation ': 76, 'Marketing,Sales,Risk,Operations': 77,
        'Development Tool': 78, 'Tool': 79, 'Customer Retention, Customer Feedback': 80,
        'Inventory management': 81, 'Energy saving': 82, 'Optimization, CRM, Pricing': 83,
        'games': 84, 'Marketing, customer targeting': 85, 'entertainment': 86,
        'Search EnginenOptimization': 87, 'Information management': 88, 'strategy': 89,
        'Social media analytics': 90, 'marketing, strategy': 91,
        'customer engagement': 92, 'Marketing, Procurement, Human Resources': 93,
        'CRM, Marketing, Human Resources': 94, 'CRM': 95, 'Merchandising, Marketing': 96,
        'Travel Planning': 97, 'Data Visualization, Content Marketing, Presentations': 98,
        'News': 99, 'analtics': 100, 'elearning': 101, 'PHONE INTELLIGENCE': 102,
        'social branding': 103, 'reporting': 104, 'DASHBOARDS': 105,
        'localized behaviour': 106, 'VIDEO STREAMING': 107, 'PAYMENT': 108,
        'software': 109, 'networking': 110, 'wireless': 111, 'advertising': 112,
        'game': 113, 'search': 114, 'conssumer web': 115, 'online music': 116,
        'media': 117, 'cloud computing': 118
    }

    yes_no_dict = {'No': 1, 'Yes': 2}
    product_service_dict = {'Service': 1, 'Product': 2, 'Both': 3, 'No Info': 4}
    platform_cloud_dict = {'Platform': 1, 'Cloud': 3, 'None': 4, 'Both': 5}
    business_model_dict = {'Linear': 1, 'Non-Linear': 2}
    education_dict = {'Masters': 1, 'Bachelors': 2, 'PhD': 3}
    experience_dict = {'Medium': 1, 'High': 2, 'Low': 3, 'None': 4}

    return {
        'categories': categories_dict,
        'focus_functions': focus_functions_dict,
        'yes_no': yes_no_dict,
        'product_service': product_service_dict,
        'platform_cloud': platform_cloud_dict,
        'business_model': business_model_dict,
        'education': education_dict,
        'experience': experience_dict
    }


# Cache file processing for dashboard
@st.cache_data
def process_uploaded_file(uploaded_file_content, file_name, file_type):
    """Process uploaded file with caching"""
    try:
        if file_type == 'csv':
            df = pd.read_csv(BytesIO(uploaded_file_content))
        else:  # xlsx
            df = pd.read_excel(BytesIO(uploaded_file_content))
        return df
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None


@st.cache_data
def analyze_columns(df):
    """Analyze DataFrame columns with caching"""
    try:
        numeric_columns = list(df.select_dtypes(['float', 'int']).columns)
        non_numeric_columns = list(df.select_dtypes(['object', 'category']).columns)
        non_numeric_columns.append(None)
        return numeric_columns, non_numeric_columns
    except Exception as e:
        st.error(f"Error analyzing columns: {str(e)}")
        return [], []


def save_user_credentials(df):
    """Save user credentials to Excel file"""
    try:
        df.to_excel("user_credentials.xlsx", index=False, engine='openpyxl')
        st.cache_data.clear()
        return True
    except Exception as e:
        st.error(f"Error saving credentials: {str(e)}")
        return False


def startup_prediction(data, model):
    """Optimized prediction function"""
    try:
        input_data = np.asarray(data, dtype=float)
        input_reshaped = input_data.reshape(1, -1)
        pred = model.predict(input_reshaped)
        return 'Startup will SUCCEED' if pred[0] == 1 else 'Startup will FAIL'
    except Exception as e:
        st.error(f"Prediction error: {str(e)}")
        return "Error in prediction"


# PAGE FUNCTIONS
def login_signup_page():
    """Login and signup page"""
    st.title("🚀 Startup Prediction & Analytics Platform")
    st.markdown("Please login or sign up to access the platform.")

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])

    with tab1:
        st.subheader("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

            if submitted:
                df = load_user_credentials()
                if username in df['Username'].values:
                    stored_password = str(df.loc[df['Username'] == username, 'Password'].values[0])
                    if password.strip() == stored_password.strip():
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.session_state.current_page = "prediction"
                        st.success(f"Welcome, {username}!")
                        st.rerun()
                    else:
                        st.error("Incorrect password.")
                else:
                    st.error("Username not found.")

    with tab2:
        st.subheader("Create Account")
        with st.form("signup_form"):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username*")
                password = st.text_input("Password*", type="password")
                name = st.text_input("Full Name*")
                age = st.number_input("Age", min_value=18, max_value=100, value=25)
            with col2:
                confirm_password = st.text_input("Confirm Password*", type="password")
                sex = st.selectbox("Gender", ["Male", "Female", "Other"])
                working_status = st.selectbox("Status", ["Employed", "Unemployed", "Student", "Entrepreneur"])
                company_name = st.text_input("Company/Organization")

            submitted = st.form_submit_button("Create Account", use_container_width=True)

            if submitted:
                if not all([username, password, name]):
                    st.error("Please fill in all required fields (marked with *)")
                elif password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    df = load_user_credentials()
                    if username in df['Username'].values:
                        st.error("Username already exists.")
                    else:
                        new_user = pd.DataFrame({
                            'Username': [username], 'Password': [password], 'Name': [name],
                            'Age': [age], 'Sex': [sex], 'Working Status': [working_status],
                            'Company Name': [company_name]
                        })
                        df = pd.concat([df, new_user], ignore_index=True)
                        if save_user_credentials(df):
                            st.success("Account created! Please login.")
                        else:
                            st.error("Failed to create account.")


def prediction_page():
    """Startup prediction page"""
    model = load_model()
    mappings = get_category_mappings()

    if model is None:
        st.error("Failed to load prediction model.")
        return

    st.title('🚀 Startup Success Prediction')
    st.markdown("Enter your company details to predict startup success probability.")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📊 Company Information")
            foundation_year = st.number_input('Foundation Year', min_value=1900, max_value=2024, value=2020)
            company_age = st.number_input('Company Age (years)', min_value=0, max_value=100, value=1)
            category = st.selectbox("Company Category", options=list(mappings['categories'].keys()))
            focus_function = st.selectbox("Focus Function", options=list(mappings['focus_functions'].keys()))
            employee_count = st.number_input("Employee Count", min_value=1, max_value=10000, value=5)
            team_grown = st.selectbox("Has Team Size Grown?", options=['No', 'Yes'])
            co_founders = st.number_input("Number of Co-founders", min_value=1, max_value=10, value=1)
            senior_leadership = st.number_input("Senior Leadership Team Size", min_value=1, max_value=50, value=2)
            total_employees = st.number_input("Total Employees", min_value=1, max_value=10000, value=5)

        with col2:
            st.subheader("👥 Team & Experience")
            top_companies = st.selectbox("Worked in Top Companies?", options=['No', 'Yes'])
            past_startups = st.selectbox("Experience in Past Startups?", options=['No', 'Yes'])
            successful_startups = st.selectbox("Successful Startups in Past?", options=['No', 'Yes'])
            product_service = st.selectbox("Product or Service Company?",
                                           options=list(mappings['product_service'].keys()))
            platform_cloud = st.selectbox("Cloud or Platform Based?", options=list(mappings['platform_cloud'].keys()))
            business_model = st.selectbox("Business Model Type", options=list(mappings['business_model'].keys()))
            education = st.selectbox("Highest Education", options=list(mappings['education'].keys()))
            education_years = st.number_input("Years of Education", min_value=10, max_value=25, value=16)
            experience_level = st.selectbox("Experience Level", options=list(mappings['experience'].keys()))

        submitted = st.form_submit_button("🔮 Predict Success", use_container_width=True, type="primary")

        if submitted:
            try:
                input_data = [
                    foundation_year, company_age, mappings['categories'][category],
                    mappings['focus_functions'][focus_function], employee_count,
                    mappings['yes_no'][team_grown], co_founders, senior_leadership,
                    total_employees, mappings['yes_no'][top_companies],
                    mappings['yes_no'][past_startups], mappings['yes_no'][successful_startups],
                    mappings['product_service'][product_service], mappings['platform_cloud'][platform_cloud],
                    mappings['business_model'][business_model], mappings['education'][education],
                    education_years, mappings['experience'][experience_level]
                ]

                result = startup_prediction(input_data, model)

                if "SUCCEED" in result:
                    st.success(f"🎉 {result}")
                    st.balloons()
                else:
                    st.warning(f"⚠️ {result}")

                with st.expander("📋 Input Summary", expanded=False):
                    summary_data = pd.DataFrame({
                        'Parameter': ['Foundation Year', 'Company Age', 'Category', 'Focus Function', 'Employee Count'],
                        'Value': [foundation_year, company_age, category, focus_function, employee_count]
                    })
                    st.dataframe(summary_data, use_container_width=True)

            except Exception as e:
                st.error(f"Prediction error: {str(e)}")


def dashboard_page():
    """Data visualization dashboard page"""
    st.title("📊 Data Analytics Dashboard")
    st.markdown("Upload your data and create interactive visualizations!")

    # File upload section
    uploaded_file = st.file_uploader(
        "📁 Upload CSV or Excel file",
        type=['csv', 'xlsx'],
        help="Upload your data file to create visualizations"
    )

    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_type = file_name.split('.')[-1].lower()
        file_content = uploaded_file.read()

        df = process_uploaded_file(file_content, file_name, file_type)

        if df is not None:
            st.session_state.df = df
            st.success(f"✅ Successfully loaded {file_name}")

            # Data overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Rows", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                st.metric("Numeric", len(df.select_dtypes(['float', 'int']).columns))
            with col4:
                st.metric("Text", len(df.select_dtypes(['object']).columns))

            # Preview data
            with st.expander("👀 Preview Data", expanded=True):
                st.dataframe(df.head(), use_container_width=True)

            # Visualization section
            st.subheader("📈 Create Visualizations")

            numeric_columns, non_numeric_columns = analyze_columns(df)

            chart_type = st.selectbox(
                "Select Visualization Type",
                ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Box Plot"]
            )

            col1, col2 = st.columns(2)

            if chart_type == "Scatter Plot" and len(numeric_columns) >= 2:
                with col1:
                    x_col = st.selectbox("X-axis", numeric_columns)
                    y_col = st.selectbox("Y-axis", numeric_columns)
                with col2:
                    color_col = st.selectbox("Color by", non_numeric_columns)
                    size_col = st.selectbox("Size by", [None] + numeric_columns)

                if st.button("Create Scatter Plot", use_container_width=True):
                    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col,
                                     title=f"{x_col} vs {y_col}")
                    st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Histogram" and len(numeric_columns) >= 1:
                with col1:
                    x_col = st.selectbox("Column", numeric_columns)
                    bins = st.slider("Bins", 5, 100, 30)
                with col2:
                    color_col = st.selectbox("Color by", non_numeric_columns)

                if st.button("Create Histogram", use_container_width=True):
                    fig = px.histogram(df, x=x_col, nbins=bins, color=color_col,
                                       title=f"Distribution of {x_col}")
                    st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Box Plot":
                with col1:
                    y_col = st.selectbox("Y-axis (numeric)", numeric_columns)
                with col2:
                    x_col = st.selectbox("X-axis (categorical)", non_numeric_columns[:-1])

                if st.button("Create Box Plot", use_container_width=True):
                    fig = px.box(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
                    st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("👆 Upload a data file to get started!")

        # Sample data option
        if st.button("🎲 Load Sample Data"):
            np.random.seed(42)
            sample_data = pd.DataFrame({
                'Sales': np.random.randint(100, 1000, 50),
                'Revenue': np.random.randint(1000, 10000, 50),
                'Customers': np.random.randint(10, 100, 50),
                'Region': np.random.choice(['North', 'South', 'East', 'West'], 50),
                'Product': np.random.choice(['A', 'B', 'C'], 50)
            })
            st.session_state.df = sample_data
            st.success("✅ Sample data loaded!")
            st.rerun()


def sidebar_navigation():
    """Sidebar navigation for authenticated users"""
    if st.session_state.authenticated:
        with st.sidebar:
            st.markdown(f"### 👋 Welcome, {st.session_state.username}!")

            # Navigation buttons
            if st.button("🚀 Startup Prediction", use_container_width=True):
                st.session_state.current_page = "prediction"
                st.rerun()

            if st.button("📊 Data Dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()

            st.divider()

            # Feedback section
            with st.expander("💬 Feedback"):
                rating = st.slider("Rate the app", 1, 5, 4)
                feedback = st.text_area("Your feedback")
                if st.button("Submit Feedback"):
                    st.success("Thank you for your feedback!")

            st.divider()

            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.username = ""
                st.session_state.current_page = "login"
                st.rerun()


def main():
    """Main application router"""
    # Show sidebar navigation for authenticated users
    sidebar_navigation()

    # Route to appropriate page
    if not st.session_state.authenticated:
        login_signup_page()
    elif st.session_state.current_page == "prediction":
        prediction_page()
    elif st.session_state.current_page == "dashboard":
        dashboard_page()
    else:
        prediction_page()  # Default page


if __name__ == '__main__':
    main()