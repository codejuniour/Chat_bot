from tensorflow.keras.models import load_model

# Load the trained chatbot model
model = load_model("chatbot_model.h5")

# Verify model structure
model.summary()
print("✅ Model loaded successfully!")
