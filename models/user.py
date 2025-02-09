from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from utils.encryptor import PasswordEncryptor

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    master_key = db.Column(db.String(500), nullable=False)
    
    # Relación con las contraseñas
    passwords = db.relationship('Password', backref='owner', lazy=True)

    @staticmethod
    def create(username, password):
        """Crea un nuevo usuario"""
        # Generar clave maestra para encriptación
        encryptor = PasswordEncryptor()
        master_key, salt = PasswordEncryptor.generate_key_from_master(password)
        
        try:
            user = User(
                username=username,
                master_key=master_key.decode()
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating user: {str(e)}")
            return None

    def set_password(self, password):
        """Establece la contraseña del usuario"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña del usuario"""
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get(user_id):
        """Obtiene un usuario por su ID"""
        return User.query.get(int(user_id))

    @staticmethod
    def get_by_username(username):
        """Obtiene un usuario por su nombre de usuario"""
        return User.query.filter_by(username=username).first()
    
    def get_passwords(self):
        """Obtiene todas las contraseñas del usuario"""
        # Desencriptar las contraseñas
        encryptor = PasswordEncryptor(self.master_key.encode())
        return [{
            'id': pw.id,
            'name': pw.name,
            'url': pw.url,
            'username': pw.username,
            'password': encryptor.decrypt(pw.password), # Desencriptar la contraseña
            'created_at': pw.created_at
        } for pw in self.passwords]
    
    def add_password(self, name, url, username, password):
        """Añade una nueva contraseña para el usuario"""
        # Encriptar la contraseña
        encryptor = PasswordEncryptor(self.master_key.encode())
        encrypted_password = encryptor.encrypt(password)
        
        try:
            pw = Password(
                name=name,
                url=url,
                username=username,
                password=encrypted_password,
                owner=self
            )
            db.session.add(pw)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    
    def update_password(self, password_id, name=None, url=None, username=None, password=None):
        """Actualiza una contraseña existente"""
        pw = Password.query.get(password_id)
        if pw is None or pw.owner != self:
            return False
        
        # Construir la consulta de actualización
        if name is not None:
            pw.name = name
        if url is not None:
            pw.url = url
        if username is not None:
            pw.username = username
        if password is not None:
            encryptor = PasswordEncryptor(self.master_key.encode())
            pw.password = encryptor.encrypt(password)
            
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
    
    def delete_password(self, password_id):
        """Elimina una contraseña"""
        pw = Password.query.get(password_id)
        if pw is None or pw.owner != self:
            return False
        
        try:
            db.session.delete(pw)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False