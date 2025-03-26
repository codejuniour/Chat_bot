# Medical Assistant Chatbot

## Overview
A simple chatbot designed to assist with medical queries and manage patient records. It uses NLP techniques to understand user input and respond accordingly.

## Features
- Basic chatbot functionality with predefined intents.
- Simple JSON-based data storage for patient records.
- A GUI interface for easy interaction.
- Basic spelling correction for user inputs.
- Machine learning model for intent classification.

## How It Works
1. The user interacts with the chatbot via the GUI.
2. The chatbot processes input using NLP and a trained model.
3. It retrieves or stores patient data when needed.
4. Responses are generated based on predefined intents.
5. Basic authentication ensures role-based access.

## Setup
1. Install dependencies:
   ```bash
   pip install numpy tensorflow nltk customtkinter pyttsx3 rapidfuzz
   ```
2. Train the chatbot model:
   ```bash
   python train_model.py
   ```
3. Run the chatbot GUI:
   ```bash
   python guichat.py
   ```

## Limitations
- Not a fully intelligent system; responses are based on predefined intents.
- Limited ability to understand complex medical queries.
- Data storage is local and not scalable.

## Future Improvements
- Add voice assistant features.
- Improve intent recognition with a more advanced model.
- Implement cloud-based data storage.

## Contributors
Developed by with help Ai and dears friends. Open to improvements and modifications.

