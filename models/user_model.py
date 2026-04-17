from database import Database
import hashlib

class UserModel:

    def __init__(self):
        self.db = Database()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create(self, username, email, password, role='client'):
        hashed_password = self.hash_password(password)
        query = "INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)"
        params = (username, email, hashed_password, role)
        return self.db.execute_query(query, params, commit=True)

    def get_by_username(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        return self.db.fetch_one(query, (username,))

    def authenticate(self, username, password):
        user = self.get_by_username(username)
        if user and user['password'] == self.hash_password(password):
            return user
        return None

    def username_exists(self, username):
        query = "SELECT COUNT(*) as count FROM users WHERE username = %s"
        result = self.db.fetch_one(query, (username,))
        return result['count'] > 0 if result else False

    def email_exists(self, email):
        query = "SELECT COUNT(*) as count FROM users WHERE email = %s"
        result = self.db.fetch_one(query, (email,))
        return result['count'] > 0 if result else False
