import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents.json
with open("intents.json", "r") as file:
    intents = json.load(file)

# Initialize data structures
words = []
classes = []
documents = []
ignore_chars = ["?", "!", ".", ","]

# Process intents
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        word_list = nltk.word_tokenize(pattern)  # Tokenization
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Lemmatize words
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_chars]
words = sorted(set(words))

# Sort classes
classes = sorted(set(classes))

# Save words.pkl
with open("words.pkl", "wb") as file:
    pickle.dump(words, file)

# Save classes.pkl
with open("classes.pkl", "wb") as file:
    pickle.dump(classes, file)

print("✅ words.pkl & classes.pkl created successfully!")
