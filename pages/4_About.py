import streamlit as st
from PIL import Image
st.set_page_config(
    page_title="About the Parkinson's Detection App",
    page_icon="🧠",
    layout="wide"
)

## ye file apne hisab se customize kar liyo jaise tuze chaiyewaise easy hai kar lenga tu 
st.markdown("""
<script src="https://kit.fontawesome.com/3264c9342c.js" crossorigin="anonymous"></script>
""", unsafe_allow_html=True)

st.title("About the Parkinson's Disease Detection Project")
st.write("---")
st.markdown("""
This application is a proof-of-concept tool designed to assist in the early detection of Parkinson's disease using modern machine learning techniques. It leverages a Convolutional Neural Network (CNN) to analyze MRI scans, providing a probabilistic assessment that can aid healthcare professionals in their diagnostic process.
""")

st.header("Our Mission")
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/2868/2868582.png", width=80)
with col2:
    st.write("""
    Our mission is to harness the power of artificial intelligence to create accessible, reliable, and non-invasive tools for early-stage disease detection. We believe that technology can bridge the gap in healthcare, providing crucial insights that empower both patients and doctors to make informed decisions sooner.
    """)

st.header("Technology Stack")
st.markdown("""
The application is built entirely in Python, leveraging a suite of powerful libraries:
- **Streamlit:** For creating the interactive and user-friendly web interface.
- **TensorFlow/Keras:** For building and running the deep learning model for MRI analysis.
- **Scikit-learn:** For the supplementary machine learning models (e.g., SVM for drawings).
- **OpenCV & Pillow:** For robust image processing and manipulation.
- **SQLAlchemy:** For database management and persistent user data storage.

""")

st.header("Important Disclaimer")
st.warning("""
**This is not a medical device.** The predictions made by this application are for informational purposes only and should not be considered a substitute for a professional medical diagnosis. All results must be reviewed and interpreted by a qualified healthcare provider. The developers assume no liability for any decisions made based on the information provided by this tool.
""")

st.header("Frequently Asked Questions (FAQ)")
with st.expander("Is my data safe and private?"):
    st.write("""
    Yes. We take data privacy seriously. All user accounts are password-protected, and prediction histories are linked to individual accounts. We do not share your data with any third parties. The application is designed to be a private tool for your personal use.
    """)
with st.expander("How accurate is the prediction model?"):
    st.write("""
    The model was trained on a curated dataset of MRI scans and achieved high accuracy on our test sets. However, its performance in real-world scenarios can vary. It is a decision-support tool, not an infallible diagnostic oracle. Factors like image quality and scan parameters can influence the result.
    """)
with st.expander("Who should use this application?"):
    st.write("""
    This application is intended for two main groups:
    1.  **Individuals** who wish to get a preliminary, non-invasive assessment based on their MRI scans, which they can then discuss with their doctor.
    2.  **Healthcare professionals and researchers** who can use it as a supplementary tool to aid in their analysis and research.
    """)

st.write("---")
st.header("Connect with Us")
st.write("We welcome feedback, questions, and collaboration opportunities.")
contact_col1, contact_col2, contact_col3 = st.columns([1, 1, 1])
with contact_col1:
    st.markdown("""
    <div style="text-align: center;">
        <a href="mailto:your.email@example.com" style="text-decoration: none; color: inherit;">
            <i class="fas fa-envelope fa-3x"></i>
            <p>Email Us</p>
        </a>
    </div>
    """, unsafe_allow_html=True)

with contact_col2:
    st.markdown("""
    <div style="text-align: center;">
        <a href="#" target="_blank" style="text-decoration: none; color: inherit;">
            <i class="fab fa-linkedin fa-3x"></i>
            <p>LinkedIn</p>
        </a>
    </div>
    """, unsafe_allow_html=True)

with contact_col3:
    st.markdown("""
    <div style="text-align: center;">
        <a href="#" target="_blank" style="text-decoration: none; color: inherit;">
            <i class="fab fa-twitter-square fa-3x"></i>
            <p>Twitter / X</p>
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; font-size: 0.9em;">
    © 2025 Parkinson's Detection Project | Built with ❤️ using Streamlit
</div>
""", unsafe_allow_html=True)