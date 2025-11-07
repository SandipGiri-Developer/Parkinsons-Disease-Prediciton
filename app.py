import streamlit as st
from database import create_user, check_password, get_db, get_user_details_by_email, get_user_stats

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Parkinson's AI Detection",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed" # Collapse sidebar for the landing page
)

# --- SESSION STATE INITIALIZATION ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_email' not in st.session_state:
    st.session_state['user_email'] = None

# --- LANDING PAGE FOR LOGGED-OUT USERS ---
def render_landing_page():
    
    # Hero Section
    
    st.title("Welcome to the Future of Early Parkinson's Detection")
    st.subheader("Harnessing AI to provide early insights from MRI scans.")
    st.write("---")

    # Login & Signup Form Section
    col1, col2 = st.columns([1, 1])
    with col1:
        st.header("Get Started")
        st.markdown("Create an account or log in to access your secure dashboard, analyze scans, and track your history.")
        login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

        with login_tab:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            if st.button("Login", key="login_button", use_container_width=True, type="primary"):
                if check_password(email, password):
                    st.session_state['logged_in'] = True
                    st.session_state['user_email'] = email
                    st.success("Login successful! Redirecting to your dashboard...")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

        with signup_tab:
            new_name = st.text_input("Name", key="signup_name")
            new_email = st.text_input("Email", key="signup_email")
            new_age = st.number_input("Age", min_value=1, max_value=120, key="signup_age")
            new_gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="signup_gender")
            new_password = st.text_input("Password", type="password", key="signup_password")
            
            if st.button("Sign Up", key="signup_button", use_container_width=True):
                db_session = next(get_db())
                if get_user_details_by_email(db_session, new_email):
                    st.warning("Email already registered.")
                else:
                    create_user(db_session, new_name, new_email, new_age, new_gender, new_password)
                    st.success("Account created successfully! Please proceed to the Login tab.")
                db_session.close()

    with col2:
        st.header("How It Works")
        st.markdown("""
        Our platform simplifies the process of gaining AI-powered insights from medical imaging.
        
        **1. Create Your Secure Account:**
           Sign up for a free, private account to store your analysis history securely.

        **2. Upload Your MRI Scan:**
           Navigate to the detection page and upload a standard MRI scan image (PNG, JPG).

        **3. Receive Instant Analysis:**
           Our AI model analyzes the scan in seconds and provides a probability score.
           
        **4. Download a Detailed Report:**
           Generate a comprehensive PDF report of the analysis for your records or to share with a healthcare professional.
        """)

    st.write("---")
    st.header("Key Features")
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    with feature_col1:
        st.subheader("🤖 AI-Powered Analysis")
        st.write("Utilizes a state-of-the-art deep learning model to detect subtle patterns associated with Parkinson's disease.")
    with feature_col2:
        st.subheader("🔒 Secure & Private")
        st.write("Your data is your own. All scans and reports are tied to your personal account and are not shared.")
    with feature_col3:
        st.subheader("📄 Comprehensive Reports")
        st.write("Generate detailed, professional PDF reports for each analysis to facilitate discussions with medical experts.")

# --- DASHBOARD FOR LOGGED-IN USERS ---
def render_dashboard():
    st.set_page_config(initial_sidebar_state="expanded") # Show sidebar on the dashboard

    db_session = next(get_db())
    try:
        user = get_user_details_by_email(db_session, st.session_state['user_email'])
        if user:
            st.title(f"Welcome back, {user.name}!")
            st.subheader("Your Personal Health Dashboard")
            st.write("---")

            # Fetch user stats
            stats = get_user_stats(db_session, user.id)

            # Dashboard Metrics
            stat_col1, stat_col2 = st.columns(2)
            with stat_col1:
                st.metric("Total Analyses Performed", stats['total_analyses'])
            with stat_col2:
                st.metric("Last Analysis Date", stats['last_analysis_date'])

            
            st.info("Remember: This tool is for informational purposes and is not a substitute for professional medical advice.", icon="⚠️")
        else:
            st.error("Could not retrieve user data. Please try logging in again.")
            st.session_state['logged_in'] = False # Force logout
    finally:
        db_session.close()

    # Sidebar for logged-in users
    with st.sidebar:
        st.title("Navigation")
        st.info(f"Logged in as: **{st.session_state['user_email']}**")
        if st.button("Logout", width='stretch'):
            st.session_state['logged_in'] = False
            st.session_state['user_email'] = None
            st.rerun()

# --- MAIN APP ROUTER ---
if not st.session_state['logged_in']:
    render_landing_page()
else:
    # When logged in, the sidebar will be built by Streamlit based on files in /pages,
    # and the main area will show the dashboard.
    render_dashboard()