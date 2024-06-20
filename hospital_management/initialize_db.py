from pymongo import MongoClient
from werkzeug.security import generate_password_hash

#DataBase
mongo = MongoClient("mongodb+srv://despoinaskourtanioti:12345@cluster0.3vktqb6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

#Collection
users = mongo.HospitalDB.users

# Admin credentials
admin_username = 'admin'
admin_role = 'admin'

# Check if admin already exists
existing_admin = users.find_one({"username": admin_username})
if not existing_admin:
    admin_user = {
        "username": admin_username,
        "role": admin_role
    }
    # Insert admin user into the database
    users.insert_one(admin_user)
