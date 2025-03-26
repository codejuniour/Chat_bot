# spell_checker.py
from rapidfuzz import process

known_terms = ["Bangalore", "Hospitals", "Hospital", "Medical Center"]

def correct_spelling(text):
    match, score, _ = process.extractOne(text, known_terms)
    if score > 80:  # Adjust threshold as needed
        return match
    return text
