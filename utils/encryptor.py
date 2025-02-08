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
    
    def rotate_key(self, new_key):
        """
        Cambia la clave de encriptación.
        
        Args:
            new_key (bytes): Nueva clave de encriptación
            
        Returns:
            bool: True si el cambio fue exitoso
        """
        try:
            new_fernet = Fernet(new_key)
            self.fernet = new_fernet
            self._key = new_key
            return True
        except Exception as e:
            print(f"Error al rotar la clave: {e}")
            return False
    
    def reencrypt(self, encrypted_data, new_key):
        """
        Reencripta datos con una nueva clave.
        
        Args:
            encrypted_data (str): Datos encriptados
            new_key (bytes): Nueva clave
            
        Returns:
            str: Datos reencriptados con la nueva clave
        """
        # Primero desencriptamos con la clave actual
        decrypted = self.decrypt(encrypted_data)
        
        # Creamos un nuevo Fernet con la nueva clave
        new_fernet = Fernet(new_key)
        
        # Encriptamos con la nueva clave
        return new_fernet.encrypt(decrypted.encode()).decode()
    
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

class AdvancedEncryptor(PasswordEncryptor):
    """
    Versión avanzada del encriptador que soporta más opciones de seguridad.
    Preparado para futura implementación de encriptación postcuántica.
    """
    
    def __init__(self, key=None, algorithm='AES'):
        super().__init__(key)
        self.algorithm = algorithm
        
    def encrypt_with_algorithm(self, data, algorithm=None):
        """
        Encripta datos usando un algoritmo específico.
        
        Args:
            data (str): Datos a encriptar
            algorithm (str, optional): Algoritmo a usar
            
        Returns:
            tuple: (encrypted_data, iv)
        """
        if algorithm is None:
            algorithm = self.algorithm
            
        if algorithm == 'AES':
            backend = default_backend()
            iv = os.urandom(16)
            cipher = Cipher(
                algorithms.AES(self._key[:32]),
                modes.CBC(iv),
                backend=backend
            )
            encryptor = cipher.encryptor()
            
            # Asegurar que los datos tienen una longitud múltiplo de 16
            padded_data = self._pad(data.encode())
            ct = encryptor.update(padded_data) + encryptor.finalize()
            
            return base64.b64encode(ct).decode(), base64.b64encode(iv).decode()
    
    def decrypt_with_algorithm(self, encrypted_data, iv, algorithm=None):
        """
        Desencripta datos usando un algoritmo específico.
        
        Args:
            encrypted_data (str): Datos encriptados
            iv (str): Vector de inicialización
            algorithm (str, optional): Algoritmo usado
            
        Returns:
            str: Datos desencriptados
        """
        if algorithm is None:
            algorithm = self.algorithm
            
        if algorithm == 'AES':
            backend = default_backend()
            cipher = Cipher(
                algorithms.AES(self._key[:32]),
                modes.CBC(base64.b64decode(iv)),
                backend=backend
            )
            decryptor = cipher.decryptor()
            padded_data = decryptor.update(base64.b64decode(encrypted_data))
            padded_data += decryptor.finalize()
            return self._unpad(padded_data).decode()
    
    @staticmethod
    def _pad(data):
        """Aplica padding a los datos para que sean múltiplo de 16"""
        padding_length = 16 - (len(data) % 16)
        padding = bytes([padding_length] * padding_length)
        return data + padding
    
    @staticmethod
    def _unpad(padded_data):
        """Elimina el padding de los datos"""
        padding_length = padded_data[-1]
        return padded_data[:-padding_length]