import json
import os
from datetime import datetime

# Database file path
DB_FILE = "patients.json"



# Load database if exists, else create an empty one
def load_database():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as file:
            return json.load(file)
    return {}

# Save the database to a JSON file
def save_database(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)
        

def add_patient_record(admin_auth, patient_id, name, age, condition=None, doctor_id=None, doctor_name=None):
    """Only admins can create or update patient records."""
    if not admin_auth:
        return "Unauthorized: Only admin can add new patients."

    db = load_database()
    
    if patient_id not in db:
        db[patient_id] = {
            "name": name,
            "age": age,
            "medical_history": {
                "conditions": [],
                "medications": [],
                "doctors": []
            }
        }

    today = datetime.today().strftime("%Y-%m-%d")

    # 🔹 Add condition (only if it's valid and not already present, case-insensitive)
    if condition and condition != "-":
        condition_lower = condition.lower()
        if not any(c["condition"].lower() == condition_lower for c in db[patient_id]["medical_history"]["conditions"]):
            db[patient_id]["medical_history"]["conditions"].append({"condition": condition, "date": today})

    # 🔹 Add doctor info (only if provided and unique, case-insensitive)
    if doctor_id and doctor_name:
    # Normalize doctor_id to lowercase for case-insensitive comparison
        doctor_lower = doctor_id.strip().lower()
    
    # Check if doctor_id already exists (case-insensitive)
        if not any(d["doctor_id"].strip().lower() == doctor_lower for d in db[patient_id]["medical_history"]["doctors"]):
            new_doctor = {
                "doctor_id": doctor_id.strip(),
                "doctor_name": doctor_name.strip(),
                "date": today
            }
            db[patient_id]["medical_history"]["doctors"].append(new_doctor)
        
        
    # 🔹 Remove invalid conditions (strings like "-")
    db[patient_id]["medical_history"]["conditions"] = [
        condition for condition in db[patient_id]["medical_history"]["conditions"]
        if isinstance(condition, dict) and condition["condition"] != "-"
    ]

    # 🔹 Remove invalid doctors (strings like "-")
    db[patient_id]["medical_history"]["doctors"] = [
        doctor for doctor in db[patient_id]["medical_history"]["doctors"]
        if isinstance(doctor, dict) and doctor["doctor_id"] != "-"
    ]

    # 🔹 Sort conditions and doctors by date
    db[patient_id]["medical_history"]["conditions"].sort(key=lambda x: x["date"])
    db[patient_id]["medical_history"]["doctors"].sort(key=lambda x: x["date"])

    save_database(db)
    return f"Patient {name} (ID: {patient_id}) record updated successfully."


# Retrieve patient details
def get_patient_record(patient_id):
    """Retrieve patient details by ID."""
    db = load_database()
    return db.get(patient_id, "No record found for this patient.")

# Doctor updates patient medical records
def update_patient_record(doctor_auth, patient_id, field, value, doctor_id, doctor_name):
    """Only doctors can update patient records."""
    if not doctor_auth:
        return "Unauthorized: Only doctors can modify patient records."

    db = load_database()
    
    if patient_id not in db:
        return "Error: Patient record not found."

    today = datetime.now().strftime("%Y-%m-%d")

    if field == "condition":
        value_lower = value.lower()
        if not any(c["condition"].lower() == value_lower for c in db[patient_id]["medical_history"]["conditions"]):
            db[patient_id]["medical_history"]["conditions"].append({"condition": value, "date": today})
    elif field == "medication":
     new_medication = {
        "medicine": value.strip().lower(),  # Normalize for case-insensitive comparison
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    # Ensure no duplicate medication entries (case-insensitive check)
    if all(existing["medicine"].strip().lower() != new_medication["medicine"] 
           for existing in db[patient_id]["medical_history"]["medications"]):
        db[patient_id]["medical_history"]["medications"].append(new_medication)
        return f"Medication '{value}' added successfully."
    else:
        return f"Medication '{value}' already exists for patient {patient_id}."

    # Remove invalid conditions (strings like "-")
    db[patient_id]["medical_history"]["conditions"] = [
        condition for condition in db[patient_id]["medical_history"]["conditions"]
        if isinstance(condition, dict) and condition["condition"] != "-"
    ]

    save_database(db)
    return f"{field.capitalize()} updated for patient {patient_id}."

# Example usage
if __name__ == "__main__":
    user_id = "P001"
    print(chatbot_response(user_id, "Prescribing Ibuprofen."))

