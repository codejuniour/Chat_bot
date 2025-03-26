import json
import os
import hashlib

# Authentication database file
AUTH_FILE = "auth.json"

# Load authentication data
def load_auth_data():
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r") as file:
            return json.load(file)
    return {"admin": {}, "doctors": {}}  # Separate storage for admin & doctors

def save_auth_data(data):
    with open(AUTH_FILE, "w") as file:
        json.dump(data, file, indent=4)

def hash_password(password):
    """Encrypts password for security."""
    return hashlib.sha256(password.encode()).hexdigest()

# Admin Functions
def create_doctor_account(admin_username, admin_password, doctor_id, doctor_name, doctor_password):
    """Only admin can create doctor accounts."""
    auth_data = load_auth_data()

    # Verify admin credentials
    if admin_username not in auth_data["admin"] or auth_data["admin"][admin_username] != hash_password(admin_password):
        return "Unauthorized: Only admin can create doctor accounts."

    # Check if doctor ID already exists
    if doctor_id in auth_data["doctors"]:
        return "Doctor ID already exists."

    # Create new doctor account
    auth_data["doctors"][doctor_id] = {
        "name": doctor_name,
        "password": hash_password(doctor_password)
    }

    save_auth_data(auth_data)
    return f"Doctor {doctor_name} added successfully."

# Doctor Login
def doctor_login(doctor_id, password):
    """Allows doctors to log in."""
    auth_data = load_auth_data()

    if doctor_id in auth_data["doctors"] and auth_data["doctors"][doctor_id]["password"] == hash_password(password):
        return f"Login successful. Welcome Dr. {auth_data['doctors'][doctor_id]['name']}!"
    
    return "Invalid credentials."

# Admin Setup (Run Once)
def setup_admin_account(admin_username, admin_password):
    """Creates the admin account (Run only once)."""
    auth_data = load_auth_data()

    if "admin" in auth_data and auth_data["admin"]:
        return "Admin account already exists."

    auth_data["admin"][admin_username] = hash_password(admin_password)
    save_auth_data(auth_data)
    return "Admin account created successfully."

# Example Usage
if __name__ == "__main__":
    print(setup_admin_account("admin", "admin123"))  # Run once to create admin
    print(create_doctor_account("admin", "admin123", "D001", "Dr. Smith", "docpass123"))  # Admin adds doctor
    print(doctor_login("D001", "docpass123"))  # Doctor logs in
