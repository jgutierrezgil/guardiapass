from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from models.password import Password
from utils.password_generator import PasswordGenerator

api = Blueprint('api', __name__)

@api.route('/passwords', methods=['GET'])
@login_required
def get_passwords():
    """Endpoint para obtener todas las contraseñas del usuario"""
    try:
        passwords = Password.get_all_for_user(current_user.id)
        return jsonify([p.to_dict(include_password=True, master_key=current_user.master_key) for p in passwords])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/passwords', methods=['POST'])
@login_required
def create_password():
    """Endpoint para almacenar una nueva contraseña en la base de datos"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        required_fields = ['name', 'username', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'El campo {field} es requerido'}), 400

        # Obtener el master_key de la sesión
        master_key = session.get('master_key')
        if not master_key:
            return jsonify({'error': 'No se encontró la clave maestra'}), 401

        password = Password.create(
            user_id=current_user.id,
            name=data['name'],
            url=data.get('url', ''),
            username=data['username'],
            password=data['password'],
            master_key=master_key,
            comments=data.get('comments', '')
        )

        if password is None:
            return jsonify({'error': 'Error al crear la contraseña en la base de datos'}), 500

        return jsonify(password.to_dict(include_password=True, master_key=master_key)), 201
    except Exception as e:
        print(f"Error al crear contraseña: {str(e)}")  # Para debugging
        return jsonify({'error': f'Error al crear la contraseña: {str(e)}'}), 500

@api.route('/passwords/<int:password_id>', methods=['GET'])
@login_required
def get_password(password_id):
    """Endpoint para obtener una contraseña específica"""
    try:
        password = Password.get(password_id, current_user.id, current_user.master_key)
        if not password:
            return jsonify({'error': 'Contraseña no encontrada'}), 404
            
        return jsonify(password.to_dict(
            include_password=True,
            master_key=current_user.master_key
        ))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/passwords/<int:password_id>', methods=['PUT'])
@login_required
def update_password(password_id):
    """Endpoint para actualizar una contraseña existente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400

        password = Password.get(password_id)
        if not password or password.user_id != current_user.id:
            return jsonify({'error': 'Contraseña no encontrada'}), 404

        # Obtener master_key de la sesión
        master_key = session.get('master_key')
        if not master_key:
            return jsonify({'error': 'No se encontró la clave maestra'}), 401

        success = password.update(
            name=data.get('name'),
            url=data.get('url'),
            username=data.get('username'),
            password=data.get('password'),
            comments=data.get('comments'),
            master_key=master_key
        )

        if not success:
            return jsonify({
                'success': False,
                'error': 'Error al actualizar la contraseña'
            }), 500

        return jsonify({
            'success': True,
            'message': 'Contraseña actualizada correctamente',
            'password': password.to_dict(include_password=True, master_key=master_key)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/passwords/<int:password_id>', methods=['DELETE'])
@login_required
def delete_password(password_id):
    """Endpoint para eliminar una contraseña"""
    try:
        password = Password.get(password_id)
        if not password or password.user_id != current_user.id:
            return jsonify({'error': 'Contraseña no encontrada'}), 404

        password.delete()
        return jsonify({'message': 'Contraseña eliminada exitosamente'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/passwords/generate', methods=['POST'])
@login_required
def generate_password():
    """Endpoint para generar una nueva contraseña"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No se recibieron datos'}), 400
            
        generator = PasswordGenerator()
        
        try:
            length = int(data.get('length', 16))
        except ValueError:
            return jsonify({'error': 'La longitud debe ser un número'}), 400
            
        if not (12 <= length <= 60):
            return jsonify({'error': 'La longitud debe estar entre 12 y 60'}), 400
        
        password = generator.generate_password(
            length=length,
            use_lower=data.get('use_lower', True),
            use_upper=data.get('use_upper', True),
            use_digits=data.get('use_digits', True),
            use_special=data.get('use_special', True),
            use_extended=data.get('use_extended', False)
        )

        print(f"Contraseña generada: {password}")
        
        strength_info = generator.measure_strength(password)
        
        return jsonify({
            'success': True,
            'password': password,
            'strength': strength_info
        })
    except Exception as e:
        print(f"Error al generar contraseña: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@api.route('/passwords/check-strength', methods=['POST'])
@login_required
def check_password_strength():
    """Endpoint para verificar la fortaleza de una contraseña"""
    try:
        data = request.get_json()
        password = data.get('password')
        
        if not password:
            return jsonify({'error': 'Se requiere una contraseña'}), 400
            
        generator = PasswordGenerator()
        strength_info = generator.measure_strength(password)
        
        return jsonify(strength_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@api.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500