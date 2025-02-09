from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from flask_login import login_required, current_user
from models.password import Password
from utils.password_generator import PasswordGenerator

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Obtener todas las contraseñas del usuario
    passwords = Password.get_all_for_user(current_user.id)
    return render_template('dashboard.html', passwords=passwords)

@main.route('/manage')
@login_required
def manage():
    return render_template('manage.html')

@main.route('/passwords', methods=['GET', 'POST'])
@login_required
def passwords():
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validar datos
        if not all([name, username, password]):
            flash('Todos los campos marcados son obligatorios.', 'error')
            return redirect(url_for('main.passwords'))
            
        # Crear nueva contraseña
        new_password = Password.create(
            user_id=current_user.id,
            name=name,
            url=url,
            username=username,
            password=password,
            master_key=session.get('master_key')
        )
        
        if new_password:
            flash('Contraseña guardada exitosamente.', 'success')
        else:
            flash('Error al guardar la contraseña.', 'error')
            
        return redirect(url_for('main.passwords'))
        
    # GET: Mostrar lista de contraseñas
    search = request.args.get('search', '')
    if search:
        passwords = Password.search_by_name(current_user.id, search)
    else:
        passwords = Password.get_all_for_user(current_user.id)
        
    return render_template('passwords.html', passwords=passwords, search=search)

@main.route('/passwords/<int:password_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def password(password_id):
    password_entry = Password.get(password_id, current_user.id, session.get('master_key'))
    
    if not password_entry:
        return jsonify({'error': 'Contraseña no encontrada'}), 404
        
    if request.method == 'GET':
        return jsonify(password_entry.to_dict(
            include_password=True,
            master_key=session.get('master_key')
        ))
        
    elif request.method == 'PUT':
        data = request.get_json()
        success = password_entry.update(
            name=data.get('name'),
            url=data.get('url'),
            username=data.get('username'),
            password=data.get('password'),
            master_key=session.get('master_key')
        )
        
        if success:
            return jsonify({'message': 'Contraseña actualizada exitosamente'})
        return jsonify({'error': 'Error al actualizar la contraseña'}), 400
        
    elif request.method == 'DELETE':
        if password_entry.delete():
            return jsonify({'message': 'Contraseña eliminada exitosamente'})
        return jsonify({'error': 'Error al eliminar la contraseña'}), 400

