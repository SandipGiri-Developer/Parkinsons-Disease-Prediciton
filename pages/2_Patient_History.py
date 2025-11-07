import streamlit as st
from database import get_db, get_user_by_email, get_predictions_by_user_id

st.set_page_config(layout="wide")

if not st.session_state.get('logged_in', False):
    st.error("You must be logged in to view your history.")
    st.stop()

st.title("Patient History")
st.write("Review your past checkups and prediction results saved to your account.")

db_session = next(get_db())
try:
    # Get the user's ID
    user = get_user_by_email(db_session, st.session_state['user_email'])
    if user:
        # Fetch all predictions for that user
        history_records = get_predictions_by_user_id(db_session, user.id)

        if history_records:
            st.write("---")
            # loop karke sab history 
            for record in history_records:
                with st.expander(f"Checkup on {record.date} - {record.result_text}"):
                    st.write("**Analysis Details**")
                    st.metric("Confidence Score", f"{record.probability*100:.2f}%")
                    st.write("**Model Interpretation:**")
                    st.write(record.result_text)
        else:
            st.info("No history found for your account. Perform a new analysis on the 'Disease Detection' page.")
            st.link_button("Go to Disease Detection", "/Disease_Detection")
    else:
        st.error("Could not retrieve user data.")
finally:
    db_session.close()
