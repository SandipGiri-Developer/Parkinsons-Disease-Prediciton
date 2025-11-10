import streamlit as st
import tensorflow as tf
import cv2
import numpy as np
import joblib
from PIL import Image

@st.cache_resource
def load_h5_model():
    """Loads the pre-trained H5 model for MRI scans."""
    try:
        model = tf.keras.models.load_model('models/MRI.keras')
        print("H5 Model loaded successfully.")
        return model
    except Exception as e:
        st.error(f"Error loading H5 model: {e}")
        return None

@st.cache_resource
def load_pkl_model():
    """Loads the pre-trained PKL model for Spiral/Wave drawings."""
    try:
        model = joblib.load('models/WAVE.pkl')
        print("PKL Model loaded successfully.")
        return model
    except Exception as e:
        st.error(f"Error loading PKL model: {e}")
        return None
# yaha prediction karta model ke liye
def predict_mri(image: Image.Image):
    """
    Takes a PIL image of an MRI, preprocesses it, and predicts the probability.
    Heatmap functionality is temporarily REMOVED.
    """
    model = load_h5_model()
    if model is None:
        return None, None

    image_size = (128, 128)
    image_cv = np.array(image.convert('RGB')) 
    image_gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
    image_resized = cv2.resize(image_gray, image_size)
    image_normalized = image_resized / 255.0
    image_expanded = np.expand_dims(image_normalized, axis=-1)
    image_expanded = np.expand_dims(image_expanded, axis=0)

    prediction = model.predict(image_expanded)
    probability = float(prediction[0][0])

    return probability, None
