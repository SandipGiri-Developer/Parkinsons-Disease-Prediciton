import tensorflow as tf
import os

OLD_MODEL_PATH = os.path.join('models', 'MRI.h5')
NEW_MODEL_PATH = os.path.join('models', 'MRI.keras')

def convert_model():
    print(f"TensorFlow Version: {tf.__version__}") 
    if not os.path.exists(OLD_MODEL_PATH):
        print(f"Error: The model file was not found at '{OLD_MODEL_PATH}'")
        print("Please make sure your model is in the 'models' subfolder and the name is correct.")
        return
    print(f"Loading model from: {OLD_MODEL_PATH}")
    try:
        model = tf.keras.models.load_model(OLD_MODEL_PATH, compile=False)
        print("Model loaded successfully.")
        model.summary()
        model.save(NEW_MODEL_PATH)
        print("-" * 50)
        print(f"SUCCESS: Model has been converted and saved to: {NEW_MODEL_PATH}")
        print("-" * 50)  
    except Exception as e:
        print(f"\nAn error occurred during the conversion process: {e}")
        print("This might be due to a significant version mismatch or a corrupted model file.")

if __name__ == "__main__":
    convert_model()