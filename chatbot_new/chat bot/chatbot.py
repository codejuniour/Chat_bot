import json
import random
import re  
import nltk
import logging
import numpy as np
import pickle
from keras.models import load_model
from database import add_patient_record, get_patient_record
from auth_system import doctor_login
from spell_checker import correct_spelling  

# ✅ Load Model
model = load_model("chatbot_model.h5")

# ✅ Load Intents
with open("intents.json", "r") as file:
    intents = json.load(file)

# ✅ Initialize NLP Tools
nltk.download("punkt")
lemmatizer = nltk.WordNetLemmatizer()

# ✅ Load Words & Classes
with open("words.pkl", "rb") as file:
    words = pickle.load(file)
with open("classes.pkl", "rb") as file:
    classes = pickle.load(file)

# ✅ Logging Configuration
logging.basicConfig(
    filename="chatbot_logs.txt",
    level=logging.INFO,
    format="%(asctime)s - User: %(message)s | Chatbot: %(response)s",
)

# ✅ Strict Greeting List
greeting_words = {"hi", "hello", "hey", "good morning", "good evening", "greetings"}

def clean_up_sentence(sentence):
    """
    Tokenizes and lemmatizes the input sentence.
    """
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def is_gibberish(word):
    """
    Detects if the input word is gibberish by checking:
    - Short non-dictionary words
    - Repeated random characters
    - Words with mostly consonants and no meaning
    """
    vowels = set("aeiou")
    if len(word) <= 3:
        return True  # Too short to be meaningful
    if not any(char in vowels for char in word):
        return True  # No vowels, likely gibberish
    if re.fullmatch(r"(.)\1{2,}", word):
        return True  # Repeated letters like "fffff"
    return False

def bag_of_words(sentence, words):
    """
    Converts a sentence into a bag-of-words numpy array.
    """
    sentence_words = clean_up_sentence(sentence)
    bag = [1 if w in sentence_words else 0 for w in words]

    # ✅ Ensure correct shape (Zero-padding if necessary)
    expected_length = model.input_shape[1]
    bag = bag[:expected_length] + [0] * (expected_length - len(bag))

    return np.array(bag)

def predict_intent(text, confidence_threshold=0.75):
    """
    Predicts the intent of the user input using the trained model.
    """
    bow = bag_of_words(text, words)
    res = model.predict(np.array([bow]))[0]
    index = np.argmax(res)
    confidence = res[index]
    predicted_intent = classes[index]

    print(f"🔍 DEBUG: Predicted Intent: {predicted_intent}, Confidence: {confidence:.2f}")

    return predicted_intent if confidence >= confidence_threshold else "unknown"

def chatbot_response(user_id, message):
    """
    Generates chatbot responses based on the predicted intent.
    """
    normalized_message = message.strip().lower()
    words_in_message = nltk.word_tokenize(normalized_message)

    # ✅ Exact Greeting Match
    if normalized_message in greeting_words:
        response = random.choice(["Hello! How can I assist you?", "Hi there! How can I help?", "Hey! What can I do for you?"])
        logging.info(f"User: {message} | Chatbot: {response}")
        return response

    # ✅ Reject Gibberish / Random Text
    if all(is_gibberish(word) for word in words_in_message):
        response = "I didn't understand that. Could you clarify?"
        logging.info(f"User: {message} | Chatbot: {response}")
        return response

    # ✅ Correct Spelling
    corrected_message = correct_spelling(message)

    # ✅ Predict Intent
    intent = predict_intent(corrected_message)

    if intent == "unknown":
        response = "I'm not sure what you mean. Could you provide more details?"
        logging.info(f"User: {message} | Chatbot: {response}")
        return response

    # ✅ Find Matching Response
    for i in intents["intents"]:
        if i["tag"] == intent:
            response = random.choice(i["responses"])
            add_patient_record(user_id, user_id, "-", corrected_message, "-")
            logging.info(f"User: {message} | Chatbot: {response}")
            return response

    # ✅ Fallback Response
    response = "I didn't understand that. Can you try again?"
    logging.info(f"User: {message} | Chatbot: {response}")
    return response

