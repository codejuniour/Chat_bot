import json
import pickle
import numpy as np
import random
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()
nltk.download("punkt")

# Load intents.json
with open("intents.json", "r") as file:
    intents = json.load(file)

# Extract words and classes
words = []
classes = []
documents = []
ignore_words = ["?", "!", ".", ","]

# Process intents
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        if intent["tag"] not in classes:
            classes.append(intent["tag"])

# Lemmatize words and remove duplicates
words = sorted(set(lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words))
classes = sorted(set(classes))

# Save words and classes
with open("words.pkl", "wb") as file:
    pickle.dump(words, file)

with open("classes.pkl", "wb") as file:
    pickle.dump(classes, file)

# Training data preparation
training = []
output_empty = [0] * len(classes)

for word_list, tag in documents:
    bag = [1 if w in [lemmatizer.lemmatize(w.lower()) for w in word_list] else 0 for w in words]
    output_row = list(output_empty)
    output_row[classes.index(tag)] = 1
    training.append([bag, output_row])

# Shuffle & convert to numpy arrays
random.shuffle(training)
train_x = np.array([x[0] for x in training])
train_y = np.array([x[1] for x in training])

# Build the model
model = Sequential([
    Dense(128, input_shape=(len(train_x[0]),), activation="relu"),
    Dropout(0.5),
    Dense(64, activation="relu"),
    Dropout(0.5),
    Dense(len(train_y[0]), activation="softmax")
])

# Compile the model
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

# Train the model
model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save the trained model
model.save("chatbot_model.h5")
print("✅ Chatbot model trained and saved as chatbot_model.h5!")
