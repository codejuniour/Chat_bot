import pickle

# Load words.pkl
with open("words.pkl", "rb") as file:
    words = pickle.load(file)

# Load classes.pkl
with open("classes.pkl", "rb") as file:
    classes = pickle.load(file)

# Print contents to verify
print("Words:", words[:10])  # Print first 10 words
print("Classes:", classes)  # Print all class labels
