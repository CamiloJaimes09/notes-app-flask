from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
from flask_login import UserMixin

db = SQLAlchemy()


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_note_user_id'), nullable=False) 

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"   

  # ✅ Añadir este import

class User(UserMixin, db.Model):  # ✅ Heredar de UserMixin
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)  # ✅ Campo opcional pero recomendado

    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Email debe contener @"
        return email
    
    @validates('username')
    def validate_username(self, key, username):
        assert len(username) >= 3, "Username debe tener al menos 3 caracteres"
        return username