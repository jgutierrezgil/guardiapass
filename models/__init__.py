import sqlite3
from flask import current_app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    """Inicializa los modelos con la aplicación"""
    db.init_app(app)
    
    # Importar modelos después de crear db para evitar importaciones circulares
    from .user import User
    from .password import Password
    
    # Crear todas las tablas
    with app.app_context():
        db.create_all()