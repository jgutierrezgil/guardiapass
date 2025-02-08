from flask import Flask, session
from flask_login import LoginManager
from models.user import User
from models import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'  # Cambiar en producción
    
    # Inicializar Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)
    
    # Registrar blueprints
    from routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Inicializar la base de datos
    init_db()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)