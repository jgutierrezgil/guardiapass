import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    
    # Configuración de la base de datos
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'passwords.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de la contraseña
    PASSWORD_MIN_LENGTH = 12
    PASSWORD_MAX_LENGTH = 60
    
    # Configuración de seguridad
    PBKDF2_ITERATIONS = 100000  # Número de iteraciones para la derivación de claves
    SALT_LENGTH = 32  # Longitud del salt en bytes
    
    # Configuración de la sesión
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutos en segundos
    SESSION_COOKIE_HTTPONLY = True  # No permitir acceso JS a la cookie

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False  # Permitir cookies en HTTP para desarrollo

class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True  # Requerir HTTPS en producción
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # configuraciones adicionales específicas de producción
        pass

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Usar base de datos en memoria para tests

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}