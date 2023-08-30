import sqlite3
import os
from dotenv import load_dotenv
from flask_login import UserMixin

load_dotenv()
db_path = os.path.join(os.getcwd(), os.getenv("DB"))

class User(UserMixin):
    def __init__(self, id, password = None):
        self.id = id
        self.password = password
        self.authenticated = False

    def get_id(self):
        return self.id

    def get_pass(self):
        return self.password

    def is_exist(self):
        return True if find_user(self.id)!=None else False
    
    def is_authenticated(self):
        return self.authenticated

    def can_login(self, password_input):
        return True if find_user(self.id).get_pass() == password_input else False

def find_user(user_id):
    conn = sqlite3.connect(db_path)
    curs = conn.cursor()
    curs.execute("SELECT * from login where user_id = (?)",[user_id])
    lu = curs.fetchone()
    if lu is None:
        return None
    else:
        return User(lu[0], lu[1])