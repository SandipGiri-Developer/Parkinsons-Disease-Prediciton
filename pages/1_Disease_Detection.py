import streamlit as st
from PIL import Image
from datetime import datetime
from model_loader import predict_mri
from database import get_db, get_user_details_by_email, add_prediction

st.set_page_config(layout="wide")

# Verify user session
if not st.session_state.get('logged_in', False):
    st.error("You must be logged in to use this feature.")
    st.stop()

# Maintain session state for prediction
if 'last_prediction' not in st.session_state:
    st.session_state['last_prediction'] = None

st.title("MRI Scan Analysis for Parkinson's Disease")
st.write("Upload an MRI scan to analyze it for potential signs of Parkinson's disease.")

# Layout for Upload and Results
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload MRI Scan")
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded MRI Scan", use_container_width=True)

with col2:
    st.subheader("Prediction Results")
    if uploaded_file is not None:
        if st.button("Run Analysis"):
            st.session_state['last_prediction'] = None
            with st.spinner("Analyzing the MRI scan... Please wait."):
                probability, _ = predict_mri(image) 
            if probability is not None:
                st.success("Analysis complete!")
                # Interpret model output
                if probability > 0.5:
                    result_text = (
                        "The MRI scan analysis indicates a potential presence of Parkinson's disease."
                    )
                else:
                    result_text = (
                        "The MRI scan analysis indicates a low probability of Parkinson's disease."
                    )

                # Save result in session
                st.session_state['last_prediction'] = {
                    "probability": probability,
                    "result_text": result_text,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "image": image,
                }
                # Save to database
                try:
                    db_session = next(get_db())
                    user = get_user_details_by_email(db_session, st.session_state["user_email"])
                    if user:
                        add_prediction(
                            db_session=db_session,
                            user_id=user.id,
                            date=st.session_state["last_prediction"]["date"],
                            probability=probability,
                            result_text=result_text,
                        )
                        st.success("Results saved to your Patient History.")
                finally:
                    db_session.close()
            else:
                st.error("Model analysis failed. Please try again.")

    # Display analysis summary if available
    if st.session_state["last_prediction"]:
        last_pred = st.session_state["last_prediction"]

        st.metric("Model Prediction (Confidence)", f"{last_pred['probability'] * 100:.2f}%")
        if last_pred["probability"] > 0.5:
            st.warning(last_pred["result_text"])
        else:
            st.success(last_pred["result_text"])

        st.write("---")
        st.subheader("Detailed Analysis Summary")
        st.write(f"**Date:** {last_pred['date']}")
        st.write(f"**Confidence Level:** {last_pred['probability'] * 100:.2f}%")
        st.write(f"**Result:** {last_pred['result_text']}")
        st.image(last_pred["image"], caption="Analyzed MRI Scan", use_container_width=True)
