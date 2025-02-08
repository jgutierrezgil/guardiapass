import os
from flask import Flask, render_template
from dotenv import load_dotenv
from config.config import config
from flask_login import LoginManager
from models.user import User
from models import init_app
import logging
from logging.handlers import RotatingFileHandler

# Inicializar el gestor de login
login_manager = LoginManager()

def create_app(config_name='default'):
    # Cargar variables de entorno
    load_dotenv()
    
    # Crear la aplicación Flask
    app = Flask(__name__)
    
    # Cargar la configuración
    app.config.from_object(config[config_name])
    
    # Inicializar el login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # Configurar logging
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/guardiapass.log', 
                                         maxBytes=10240, 
                                         backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('GuardiaPass startup')
    
    # Registrar blueprints
    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Inicializar SQLAlchemy
    init_app(app)
    
    # Manejar errores personalizados
    register_error_handlers(app)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV') or 'default')
    port = int(os.getenv('PORT', 5000))
    app.run(host='127.0.0.1', port=port)