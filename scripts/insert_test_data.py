from datetime import datetime, timedelta
import sys
import os

# Añadir el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import create_app
from models import db
from models.user import User
from models.password import Password
from utils.encryptor import PasswordEncryptor

def insert_test_passwords():
    # Crear la aplicación con configuración de desarrollo
    app = create_app('development')
    
    with app.app_context():
        # Buscar al usuario joaquin
        user = User.query.filter_by(username='joaquin').first()
        if not user:
            print("Error: Usuario 'joaquin' no encontrado")
            return

        # Datos de prueba
        test_data = [
            {
                'name': 'Gmail 2020',
                'url': 'https://gmail.com',
                'username': 'joaquin.test@gmail.com',
                'password': 'TestPass2020!',
                'comments': 'Cuenta de correo de prueba',
                'created_at': datetime(2020, 3, 15)
            },
            {
                'name': 'GitHub 2020',
                'url': 'https://github.com',
                'username': 'joaquin-dev',
                'password': 'GitHubTest2020#',
                'comments': 'Cuenta de desarrollo',
                'created_at': datetime(2020, 6, 22)
            },
            {
                'name': 'AWS 2020',
                'url': 'https://aws.amazon.com',
                'username': 'joaquin.admin',
                'password': 'AwsSecret2020$',
                'comments': 'Cuenta de AWS',
                'created_at': datetime(2020, 8, 10)
            },
            {
                'name': 'LinkedIn 2020',
                'url': 'https://linkedin.com',
                'username': 'joaquin.professional',
                'password': 'LinkedIn2020@',
                'comments': 'Perfil profesional',
                'created_at': datetime(2020, 10, 5)
            },
            {
                'name': 'Netflix 2020',
                'url': 'https://netflix.com',
                'username': 'joaquin.entertainment',
                'password': 'Netflix2020!',
                'comments': 'Cuenta de streaming',
                'created_at': datetime(2020, 12, 25)
            }
        ]

        # Insertar cada contraseña
        for data in test_data:
            try:
                # Crear la contraseña usando el método del modelo que maneja la encriptación
                password = Password.create(
                    user_id=user.id,
                    name=data['name'],
                    url=data['url'],
                    username=data['username'],
                    password=data['password'],
                    master_key=user.master_key,
                    comments=data['comments']
                )
                
                # Actualizar la fecha de creación
                password.created_at = data['created_at']
                db.session.add(password)
                
            except Exception as e:
                print(f"Error al insertar {data['name']}: {str(e)}")
                db.session.rollback()
                continue

        # Guardar todos los cambios
        try:
            db.session.commit()
            print("Datos de prueba insertados correctamente")
        except Exception as e:
            print(f"Error al guardar los cambios: {str(e)}")
            db.session.rollback()

if __name__ == '__main__':
    insert_test_passwords()
