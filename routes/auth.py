from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from utils.password_generator import PasswordGenerator

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.get_by_username(username)
        
        if not user or not user.check_password(password):
            flash('Por favor verifica tus credenciales e intenta nuevamente.', 'error')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=remember)
        
        # Configurar la sesión
        session.permanent = True
        session['user_id'] = user.id
        session['master_key'] = user.master_key
        
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('main.dashboard'))
        
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('master_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones
        if User.get_by_username(username):
            flash('El nombre de usuario ya está en uso.', 'error')
            return redirect(url_for('auth.register'))
            
        if password != confirm_password:
            flash('Las contraseñas no coinciden.', 'error')
            return redirect(url_for('auth.register'))
            
        # Validar fortaleza de la contraseña
        password_generator = PasswordGenerator()
        is_valid, errors = password_generator.validate_password(password)
        if not is_valid:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('auth.register'))
            
        # Crear nuevo usuario
        user = User.create(username, password)
        if not user:
            flash('Ocurrió un error al crear el usuario.', 'error')
            return redirect(url_for('auth.register'))
            
        flash('Registro exitoso. Por favor inicia sesión.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    # Limpiar la clave maestra de la sesión
    session.pop('master_key', None)
    session.pop('user_id', None)
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Cambio de contraseña
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_user.verify_password(current_password):
            flash('La contraseña actual es incorrecta.', 'error')
            return redirect(url_for('auth.profile'))
            
        if new_password != confirm_password:
            flash('Las contraseñas nuevas no coinciden.', 'error')
            return redirect(url_for('auth.profile'))
            
        # Validar fortaleza de la nueva contraseña
        password_generator = PasswordGenerator()
        is_valid, errors = password_generator.validate_password(new_password)
        if not is_valid:
            for error in errors:
                flash(error, 'error')
            return redirect(url_for('auth.profile'))
            
        # Actualizar contraseña
        try:
            current_user.update_password(new_password)
            flash('Contraseña actualizada exitosamente.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Error al actualizar la contraseña.', 'error')
            return redirect(url_for('auth.profile'))
            
    return render_template('profile.html')

@auth.route('/check-password-strength', methods=['POST'])
def check_password_strength():
    password = request.json.get('password', '')
    password_generator = PasswordGenerator()
    strength_info = password_generator.measure_strength(password)
    return jsonify(strength_info)

@auth.route('/api/passwords', methods=['GET'])
@login_required
def get_all_passwords():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No autorizado'}), 401

    passwords = Password.get_all_for_user(user_id)
    return jsonify(passwords)