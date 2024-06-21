from app import create_app
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, abort)
from app import mongo
from datetime import datetime
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from functools import wraps
from bson import ObjectId
import re
import initialize_db 

app = create_app()

#Database
mongo = MongoClient("mongodb+srv://despoinaskourtanioti:12345@cluster0.3vktqb6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

#Collections
users = mongo.HospitalDB.users # Role Tracking
doctors = mongo.HospitalDB.doctors
patients = mongo.HospitalDB.patients
appointments = mongo.HospitalDB.appointments

# Role Based Access Control
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    user = users.find_one({'username': username})
    if user:
        return User(username=user['username'], role=user['role'])
    return None

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or "admin" not in current_user.role:
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or "doctor" not in current_user.role:
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def patient_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or "patient" not in current_user.role:
            flash('Access denied', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

######################################## Routes ########################################

# Home
@app.route('/')
def home():
    return render_template('home.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
    
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        amka = request.form.get('amka')
        date_of_birth = request.form.get('date_of_birth')

        # Check if the username already exists
        existing_username = patients.find_one({"username": username})
        if existing_username:
            flash("This username already exists in the database.", "error")
            return redirect(url_for("register"))

        # Check if the email already exists
        existing_email = patients.find_one({"email": email})
        if existing_email:
            flash("This email already exists in the database.", "error")
            return redirect(url_for("register"))
        
        # Validate AMKA
        if not re.match(r'^\d{11}$', amka):
            flash("AMKA must be exactly 11 digits.", "error")
            return redirect(url_for("register"))


        # Insert into patients and users collection
        patients.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'password': password,
            'amka': amka,
            'date_of_birth': date_of_birth
        })

        users.insert_one({
            'username': username,
            'role': 'patient'
        })

        user_obj = User(username=username, role='patient')
        login_user(user_obj) # Session

        flash("You have been Successfully Registered")
        return redirect(url_for("patient"))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users.find_one({"username": username})

        # Admin login
        if username == 'admin' and password == '@dm1n':
            user_obj = User(username=user['username'], role=user['role'])
            login_user(user_obj) # Session
            
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin'))


        # Patient login
        if user and user['role'] == 'patient':

            patient = patients.find_one({"username": username})

            if patient and patient['password'] == password:
                user_obj = User(username=user['username'], role=user['role'])
                login_user(user_obj)
            
                flash('Login successful!', 'success')            
                return redirect(url_for('patient'))
            else:
                flash('Wrong password.', 'error')

        # Doctor login   
        elif user and user['role'] == 'doctor':

            doctor = doctors.find_one({"username": username})

            if doctor and doctor['password']== password:  
                user_obj = User(username=user['username'], role=user['role'])
                login_user(user_obj) # Session           

                flash('Login successful!', 'success')
            
                return redirect(url_for('doctor'))
            else:
                flash('Wrong password.', 'error')
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

#Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Dashboards
@app.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/doctor')
@login_required
@doctor_required
def doctor():
    return render_template('doctor.html')

@app.route('/patient')
@login_required
@patient_required
def patient():
    return render_template('patient.html')

######################################## Admin ########################################

# New Doctor
@app.route('/admin/new_doctor', methods=['GET', 'POST'])
@login_required
@admin_required
def new_doctor():
    if request.method == 'POST':
        
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        cost = request.form.get('cost')
        specialty = request.form.get('specialty')

        # Check if the username already exists
        existing_username = doctors.find_one({"username": username})
        if existing_username:
            flash("This username already exists in the database.", "error")
            return redirect(url_for("new_doctor"))

        # Check if the email already exists
        existing_email = doctors.find_one({"email": email})
        if existing_email:
            flash("This email already exists in the database.", "error")
            return redirect(url_for("new_doctor"))

        # Insert into users and doctors collections
        users.insert_one({
            'username': username,
            'role': 'doctor'
        })


        doctors.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'password': password,
            'cost': cost,
            'specialty': specialty
        })

        flash('Doctor added successfully!', 'success')
        return redirect(url_for("admin"))


    return render_template('/admin/new_doctor.html')

# Change Dr's Password
@app.route('/admin/change_doctor_password', methods=['GET', 'POST'])
@login_required
@admin_required
def change_doctor_password():
    if request.method == 'POST':
        
        doctor_username = request.form.get('doctor_username')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        doctor = doctors.find_one({'username': doctor_username})

        # Doctor does not exist in the database
        if not doctor:
            flash('That doctor does not exist in the database.', 'error')
        # Confirm password
        elif new_password != confirm_password:
            flash('Passwords do not match.', 'error')
        else:
            # Update password
            doctors.update_one({'username': doctor_username}, {'$set': {'password': new_password}})
            flash('Password updated successfully.', 'success')
            return redirect(url_for('admin'))

    return render_template('/admin/change_doctor_password.html')

# Delete Dr
@app.route('/admin/delete_doctor', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_doctor():
    if request.method == 'POST':
        
        doctor_username = request.form.get('doctor_username')

        doctor = doctors.find_one({'username': doctor_username})

        if not doctor:
            flash('That doctor does not exist in the database.', 'error')
        else:
            # Delete doctor from doctors and users collections and their appointments
            doctors.delete_one({'username': doctor_username})
            users.delete_one({'username': doctor_username})
            appointments.delete_many({'doctor_username': doctor_username})

            flash('Doctor deleted successfully!', 'success')
            return redirect(url_for('admin'))

    return render_template('/admin/delete_doctor.html')

# Delete Patient
@app.route('/admin/delete_patient', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_patient():
    if request.method == 'POST':
        
        patient_username = request.form.get('patient_username')

        patient = patients.find_one({'username': patient_username})

        if not patient:
            flash('That patient does not exist in the database.', 'error')
        else:
            # Delete patient from patient and users collections and their appointments
            patients.delete_one({'username': patient_username})
            users.delete_one({'username': patient_username})
            appointments.delete_many({'patient_username': patient_username})

            flash('Patient deleted successfully!', 'success')
            return redirect(url_for('admin'))
        
    return render_template('/admin/delete_patient.html')

######################################## Doctor ########################################

# Change Password
@app.route('/doctor/change_password', methods=['GET', 'POST'])
@login_required
@doctor_required
def change_password():
    if request.method == 'POST':
        
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        doctor = doctors.find_one({'username': current_user.username})

        if not doctor or not doctor['password'] == current_password: # The old password must be correct
            flash('Invalid current password. Please try again.', 'error')
        elif new_password != confirm_password: # Confirm password
            flash('Passwords do not match.', 'error') 
        else:
            # Update password
            doctors.update_one({'username': current_user.username}, {'$set': {'password': new_password}})
            flash('Password updated successfully.', 'success')
            return redirect(url_for('doctor'))

    return render_template('/doctor/change_password.html')

# Change Cost
@app.route('/doctor/change_cost', methods=['GET', 'POST'])
@login_required
@doctor_required
def change_cost():
    if request.method == 'POST':
        
        new_cost = request.form.get('new_cost')

        # Update cost
        doctors.update_one({'username': current_user.username}, {'$set': {'cost': new_cost}})
        flash('Cost updated successfully.', 'success')
        return redirect(url_for('doctor'))

    return render_template('/doctor/change_cost.html')

# View Appointments
@app.route('/doctor/view_doctor_appointments', methods=['GET'])
@login_required
@doctor_required
def view_doctor_appointments():
    view_doctor_appointments = list(appointments.find({
        "doctor_username": current_user.username,
        "date": {"$gte": datetime.now().strftime('%Y-%m-%d')}
    }))
    return render_template('doctor/view_doctor_appointments.html', appointments=view_doctor_appointments)

######################################## Patient ########################################

# Appointment
@app.route('/patient/appointment')
@login_required
@patient_required
def appointment():
    return render_template('patient/appointment.html')

# Search
@app.route('/patient/search_appointments', methods=['GET', 'POST'])
@login_required
@patient_required
def search_appointments():
    date = request.form.get('date')
    time = request.form.get('time')
    specialty = request.form.get('specialty')
    reason = request.form.get('reason')

    # Doctors based on specialty
    available_doctors = doctors.find({"specialty": specialty})
    
    # Filter out doctors who have existing appointments at the specified date and time
    booked_doctors = appointments.find({"date": date, "time": time}, {"doctor_username": 1})
    booked_doctor_usernames = {doc['doctor_username'] for doc in booked_doctors}
    
    # Filter available doctors
    filtered_doctors = [doctor for doctor in available_doctors if doctor['username'] not in booked_doctor_usernames]

    return render_template('patient/search_results.html', doctors=filtered_doctors, date=date, time=time, reason=reason)

# Book Appointment
@app.route('/patient/book_appointment', methods=['GET', 'POST'])
@login_required
@patient_required
def book_appointment():
    if request.method == 'POST':
        patient_username = current_user.username
        patient = patients.find_one({"username": patient_username})

        patient_first_name = patient['first_name']
        patient_last_name = patient['last_name']
        doctor_first_name = request.form.get('doctor_first_name')
        doctor_last_name = request.form.get('doctor_last_name')
        date = request.form.get('date')
        time = request.form.get('time')

        doctor_username = request.form.get('doctor_username')

        doctor = doctors.find_one({"username": doctor_username})
        cost = doctor['cost']
        specialty = request.form.get('specialty')
    
        reason = request.form.get('reason')
    
        # Add new appointment
        appointments.insert_one({
            'patient_first_name': patient_first_name,
            'patient_last_name': patient_last_name,
            'doctor_first_name': doctor_first_name,
            'doctor_last_name': doctor_last_name,
            'date': date,
            'time': time,
            'cost': cost,
            'reason': reason,
            'specialty': specialty,
            'patient_username': patient_username,
            'doctor_username': doctor_username
        })

        flash('Appointment added successfully!', 'success')
    
        return redirect(url_for('patient'))
    else:
        doctor_username = request.form.get('doctor_username')
        doctor_first_name = request.form.get('doctor_first_name')
        doctor_last_name = request.form.get('doctor_last_name')
        date = request.form.get('date')
        time = request.form.get('time')
        specialty = request.form.get('specialty')
        reason = request.form.get('reason')
        
        return render_template('patient/book_appointment.html', 
                               doctor_username=doctor_username,
                               doctor_first_name=doctor_first_name,
                               doctor_last_name=doctor_last_name,
                               date=date,
                               time=time,
                               specialty=specialty,
                               reason=reason)

#View Appointments
@app.route('/patient/view_appointments', methods=['GET'])
@login_required
@patient_required
def view_appointments():
    view_appointments = list(appointments.find({
        "patient_username": current_user.username,
        "date": {"$gte": datetime.now().strftime('%Y-%m-%d')}
    }))
    return render_template('patient/view_appointments.html', appointments=view_appointments)

# Appointment Info
@app.route('/patient/appointment_info/<appointment_id>', methods=['GET'])
@login_required
@patient_required
def appointment_info(appointment_id):
    appointment = appointments.find_one({"_id": ObjectId(appointment_id), "patient_username": current_user.username})

    # The cost can always be changed by doctor/admin
    doctor_username = appointment['doctor_username']
    doctor = doctors.find_one({"username": doctor_username})
    cost = doctor['cost']
    return render_template('patient/appointment_info.html', appointment=appointment, cost=cost)

# Cancel Appointment
@app.route('/patient/cancel_appointment/<appointment_id>', methods=['POST'])
@login_required
@patient_required
def cancel_appointment(appointment_id):
    # Delete appointment from db
    appointments.delete_one({'_id': ObjectId(appointment_id)})
    flash('Appointment canceled successfully!', 'success')

    return redirect(url_for('view_appointments'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
