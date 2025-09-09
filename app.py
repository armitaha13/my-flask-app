# app.py (Final Version with Hardcoded Admin Login & CRUD)

from flask import Flask, request, jsonify
from functools import wraps
import jwt
import datetime
# Make sure you are using the database_manager.py updated for PyMySQL
from database_manager import DatabaseManager

# --- App Initialization ---
app = Flask(__name__)

# IMPORTANT: This secret key is for signing the JWTs. Change it to a long, random string!
app.config['SECRET_KEY'] = 'a-very-long-and-random-secret-key-for-security'

# --- Hardcoded Admin Credentials (Not Recommended for Production) ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"  # You can change this password

# --- Database Connection ---
# Make sure to use the correct password you found earlier (it might be "")
db_manager = DatabaseManager(
    host="localhost",
    user="root",
    password="4142431234",  # <--- رمز عبور صحیح دیتابیس خود را اینجا وارد کنید
    database="dental_clinic"
)
db_manager.connect()


# --- DECORATOR for Token Authentication ---
# This function checks for a valid token before allowing access to a route
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            # The token is expected in the format: "Bearer <token>"
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Bearer token malformed!'}), 401

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # Decode the token using our secret key
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['username']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        # If token is valid, execute the original function
        return f(current_user, *args, **kwargs)
    return decorated


# --- PUBLIC ROUTES (No login required) ---

@app.route('/api/services', methods=['GET'])
def get_services():
    """Public endpoint to get all services."""
    services = db_manager.fetch_all("SELECT * FROM services;")
    return jsonify(services)

@app.route('/api/appointments', methods=['GET'])
def get_all_appointments():
    """Public endpoint to get all appointments."""
    query = """
        SELECT a.*, s.name AS service_name
        FROM appointments a JOIN services s ON a.service_id = s.id
        ORDER BY a.appointment_date, a.appointment_time;
    """
    appointments = db_manager.fetch_all(query)
    return jsonify(appointments)


# --- ADMIN LOGIN ROUTE ---

@app.route('/api/login', methods=['POST'])
def login():
    """Admin login endpoint using hardcoded credentials."""
    auth = request.get_json()
    if not auth or not auth.get('username') or not auth.get('password'):
        return jsonify({'message': 'Username or password missing'}), 401

    # Check against the hardcoded credentials
    if auth['username'] == ADMIN_USERNAME and auth['password'] == ADMIN_PASSWORD:
        # If correct, generate a token that expires in 24 hours
        token = jwt.encode({
            'username': ADMIN_USERNAME,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        return jsonify({'token': token})

    return jsonify({'message': 'Wrong username or password'}), 401


# --- ADMIN-PROTECTED ROUTES (Login required) ---

@app.route('/api/appointments', methods=['POST'])
@token_required
def add_appointment(current_user):
    """(Admin Only) Adds a new appointment."""
    data = request.get_json()
    required_fields = ['patient_name', 'patient_phone', 'patient_nationalCode', 'appointment_date', 'appointment_time', 'service_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    query = """
        INSERT INTO appointments (patient_name, patient_phone, patient_nationalCode, appointment_date, appointment_time, service_id)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    params = (data['patient_name'], data['patient_phone'], data['patient_nationalCode'], data['appointment_date'], data['appointment_time'], data['service_id'])

    if db_manager.execute_query(query, params):
        return jsonify({"message": "Appointment added successfully!"}), 201
    else:
        return jsonify({"error": "Failed to add appointment"}), 500


@app.route('/api/appointments/<int:appointment_id>', methods=['PUT'])
@token_required
def update_appointment(current_user, appointment_id):
    """(Admin Only) Edits an existing appointment."""
    data = request.get_json()
    required_fields = ['patient_name', 'patient_phone', 'patient_nationalCode', 'appointment_date', 'appointment_time', 'service_id']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    query = """
        UPDATE appointments SET 
        patient_name = %s, patient_phone = %s, patient_nationalCode = %s, 
        appointment_date = %s, appointment_time = %s, service_id = %s
        WHERE id = %s;
    """
    params = (data['patient_name'], data['patient_phone'], data['patient_nationalCode'], data['appointment_date'], data['appointment_time'], data['service_id'], appointment_id)
    
    if db_manager.execute_query(query, params):
        return jsonify({"message": f"Appointment {appointment_id} updated successfully!"})
    else:
        return jsonify({"error": "Failed to update appointment"}), 500


@app.route('/api/appointments/<int:appointment_id>', methods=['DELETE'])
@token_required
def delete_appointment(current_user, appointment_id):
    """(Admin Only) Deletes an appointment."""
    query = "DELETE FROM appointments WHERE id = %s;"
    
    if db_manager.execute_query(query, (appointment_id,)):
        return jsonify({"message": f"Appointment {appointment_id} deleted successfully!"})
    else:
        return jsonify({"error": "Failed to delete appointment"}), 500


# --- Run the App ---
if __name__ == '__main__':
    # Make sure you are using the updated database_manager.py that uses PyMySQL!
    app.run(debug=True)
