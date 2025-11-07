import streamlit as st 
import google.generativeai as genai
import os
from dotenv import load_dotenv
from database import get_db, get_user_by_email, get_predictions_by_user_id

load_dotenv() # gemini api key ke liye load the .env file

def get_patient_history_from_db(user_email): # patient history ke liye  
    db_session = next(get_db())
    try:
        user = get_user_by_email(db_session, user_email)
        if not user:
            return "Could not identify the user."
        predictions = get_predictions_by_user_id(db_session, user.id)
        if not predictions:
            return "No patient history is available in the database yet. The user has not performed any analysis."
        # Format the history into a string
        context = "Here is the patient's medical history, with the most recent checkup first:\n\n"
        for i, record in enumerate(predictions): # sorted hua hua data hai history 
            context += f"--- Checkup Record {i+1} ---\n"
            context += f"Date of Analysis: {record.date}\n"
            context += f"Model Prediction Confidence (Probability of Parkinson's): {record.probability*100:.2f}%\n"
            context += f"Model's Interpretation: \"{record.result_text}\"\n\n"
        
        return context
    finally:
        db_session.close()

st.set_page_config(layout="wide")

if not st.session_state.get('logged_in', False):
    st.error("You must be logged in to use the chatbot.")
    st.stop()
st.title("Personalized Health Chatbot 💬")
st.write("This chatbot uses your permanent health history to answer questions.")

api_key = os.getenv("GEMINI_API_KEY") # teri wali gemini api key dal diyo .env me
model = None

if api_key:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Failed to configure Google AI. Error: {e}")
        st.stop()
else:
    st.error("GEMINI_API_KEY not found in .env file.")
    st.stop()


if "chat_session" not in st.session_state: # initialize chat session
    if model:
        st.session_state.chat_session = model.start_chat(history=[])

if "chat_session" in st.session_state: # display chat history
    for message in st.session_state.chat_session.history:
        role = "assistant" if message.role == 'model' else message.role
        with st.chat_message(role):
            st.markdown(message.parts[0].text)

if prompt := st.chat_input("Ask a question about your health records..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    patient_context = get_patient_history_from_db(st.session_state['user_email'])
    # prompt apnne hisab se fine tune kar liyo
    augmented_prompt = f"""
    **System Instructions:**
    You are an expert AI medical assistant. Your task is to answer the user's questions based  on the provided medical history context. Do not invent information or provide general medical advice.. Be empathetic and clear in your responses.
    Act as a professional healthcare assistant. if patient have disease or may have then advise them to consult a healthcare professional for accurate diagnosis and treatment.
    and you can also answer general health and wellness questions.
    **Provided Medical History Context:**
    {patient_context}

    **User's Question:**
    "{prompt}"

    **Your Response:**
    """

    with st.chat_message("assistant"):
        with st.spinner("Analyzing your permanent records and thinking..."):
            try:
                response = st.session_state.chat_session.send_message(augmented_prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")