from . import db
from datetime import datetime
from utils.encryptor import PasswordEncryptor

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200))
    username = db.Column(db.String(100), nullable=False)
    encrypted_password = db.Column(db.String(500), nullable=False)
    comments = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def create(user_id, name, url, username, password, master_key, comments=None):
        """Crea una nueva contraseña"""
        try:
            encryptor = PasswordEncryptor(master_key.encode())
            encrypted_password = encryptor.encrypt(password)
            
            new_password = Password(
                user_id=user_id,
                name=name,
                url=url,
                username=username,
                encrypted_password=encrypted_password,
                comments=comments
            )
            
            db.session.add(new_password)
            db.session.commit()
            return new_password
        except Exception as e:
            db.session.rollback()
            print(f"Error creating password: {str(e)}")
            return None

    @staticmethod
    def get(password_id):
        """Obtiene una contraseña por su ID"""
        return Password.query.get(password_id)

    @staticmethod
    def get_all_for_user(user_id):
        """Obtiene todas las contraseñas de un usuario"""
        return Password.query.filter_by(user_id=user_id).order_by(Password.created_at.desc()).all()

    def update(self, name=None, url=None, username=None, password=None, comments=None, master_key=None):
        """Actualiza los datos de la contraseña"""
        try:
            if name is not None:
                self.name = name
            if url is not None:
                self.url = url
            if username is not None:
                self.username = username
            if password is not None and master_key is not None:
                encryptor = PasswordEncryptor(master_key.encode())
                self.encrypted_password = encryptor.encrypt(password)
            if comments is not None:
                self.comments = comments
                
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error updating password: {str(e)}")
            return False

    def delete(self):
        """Elimina la contraseña"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting password: {str(e)}")
            return False

    def to_dict(self, include_password=False, master_key=None):
        """Convierte la contraseña a un diccionario"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'url': self.url,
            'username': self.username,
            'comments': self.comments,
            'created_at': self.created_at
        }
        
        if include_password and master_key:
            try:
                decryptor = PasswordEncryptor(master_key.encode())
                data['password'] = decryptor.decrypt(self.encrypted_password)
            except Exception:
                data['password'] = None
                
        return data