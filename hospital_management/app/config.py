import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://despoinaskourtanioti:12345@cluster0.3vktqb6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
