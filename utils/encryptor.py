from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class PasswordEncryptor:
    def __init__(self, key=None):
        """
        Inicializa el encriptador con una clave opcional.
        Si no se proporciona clave, se genera una nueva.
        """
        if key is None:
            key = Fernet.generate_key()
        self.fernet = Fernet(key)
        self._key = key
    
    @property
    def key(self):
        """Retorna la clave de encriptación actual"""
        return self._key
    
    def encrypt(self, password):
        """
        Encripta una contraseña.
        
        Args:
            password (str): Contraseña a encriptar
            
        Returns:
            str: Contraseña encriptada en formato base64
        """
        return self.fernet.encrypt(password.encode()).decode()
    
    def decrypt(self, encrypted_password):
        """
        Desencripta una contraseña.
        
        Args:
            encrypted_password (str): Contraseña encriptada
            
        Returns:
            str: Contraseña original
        """
        return self.fernet.decrypt(encrypted_password.encode()).decode()
    
    @staticmethod
    def generate_key_from_master(master_password, salt=None):
        """
        Genera una clave de encriptación a partir de una contraseña maestra.
        
        Args:
            master_password (str): Contraseña maestra
            salt (bytes, optional): Salt para la derivación de la clave
            
        Returns:
            bytes: Clave derivada en formato compatible con Fernet
        """
        if salt is None:
            salt = os.urandom(16)
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key, salt
    
    @staticmethod
    def verify_key(key):
        """
        Verifica si una clave es válida para Fernet.
        
        Args:
            key (bytes): Clave a verificar
            
        Returns:
            bool: True si la clave es válida
        """
        try:
            Fernet(key)
            return True
        except Exception:
            return False
