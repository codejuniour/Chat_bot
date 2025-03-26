import os

# List of required files
required_files = ["words.pkl", "classes.pkl", "chatbot_model.h5"]

# Check if each file exists
missing_files = [file for file in required_files if not os.path.exists(file)]

if not missing_files:
    print("✅ All required files are present. You can run the chatbot!")
else:
    print("❌ Missing files:", missing_files)
    print("⚠️ Please generate them before running the chatbot.")
