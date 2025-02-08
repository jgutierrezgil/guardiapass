from flask import Blueprint, request, jsonify, session
from flask_login import login_required, current_user
from models.password import Password
from utils.password_generator import PasswordGenerator
from utils.ai_handler import AIHandler

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
    """Endpoint para crear una nueva contraseña"""
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

        password.update(
            name=data.get('name'),
            url=data.get('url'),
            username=data.get('username'),
            password=data.get('password'),
            comments=data.get('comments'),
            master_key=current_user.master_key
        )

        return jsonify(password.to_dict(include_password=True, master_key=current_user.master_key))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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
            'password': password,
            'strength': strength_info
        })
    except Exception as e:
        print(f"Error al generar contraseña: {str(e)}")
        return jsonify({'error': str(e)}), 500

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

@api.route('/ai/analyze', methods=['POST'])
@login_required
def analyze_passwords():
    """Endpoint para analizar contraseñas con IA"""
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': 'Se requiere API key'}), 400
            
        ai_handler = AIHandler(api_key)
        
        # Obtener las contraseñas del usuario sin exponer las contraseñas reales
        passwords = Password.get_all_for_user(current_user.id)
        password_info = [
            {
                'name': p.name,
                'url': p.url,
                'username': p.username,
                'created_at': p.created_at,
                'strength': PasswordGenerator().measure_strength(
                    p.get_decrypted_password(current_user.master_key)
                )
            }
            for p in passwords
        ]
        
        analysis = ai_handler.analyze_passwords(password_info)
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/ai/suggest', methods=['POST'])
@login_required
def get_ai_suggestions():
    """Endpoint para obtener sugerencias de la IA"""
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        url = data.get('url')
        context = data.get('context', {})
        
        if not api_key or not url:
            return jsonify({'error': 'Se requieren API key y URL'}), 400
            
        ai_handler = AIHandler(api_key)
        suggestions = ai_handler.get_password_suggestions(url, context)
        
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/search', methods=['GET'])
@login_required
def search_passwords():
    """Endpoint para buscar contraseñas"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Se requiere un término de búsqueda'}), 400
            
        passwords = Password.search_by_name(current_user.id, query)
        return jsonify([
            p.to_dict(include_password=False)
            for p in passwords
        ])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Endpoint para obtener estadísticas de las contraseñas"""
    try:
        passwords = Password.get_all_for_user(current_user.id)
        
        # Análisis de fortaleza
        strength_stats = {
            'weak': 0,
            'moderate': 0,
            'strong': 0,
            'very_strong': 0
        }
        
        generator = PasswordGenerator()
        for password in passwords:
            decrypted = password.get_decrypted_password(current_user.master_key)
            strength = generator.measure_strength(decrypted)
            
            if strength['score'] < 4:
                strength_stats['weak'] += 1
            elif strength['score'] < 6:
                strength_stats['moderate'] += 1
            elif strength['score'] < 8:
                strength_stats['strong'] += 1
            else:
                strength_stats['very_strong'] += 1
        
        return jsonify({
            'total_passwords': len(passwords),
            'strength_distribution': strength_stats,
            'needs_update': strength_stats['weak'] + strength_stats['moderate']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Recurso no encontrado'}), 404

@api.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500