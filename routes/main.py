from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from flask_login import login_required, current_user
from models.password import Password
from utils.password_generator import PasswordGenerator
from datetime import datetime, timezone
from urllib.parse import urlparse

main = Blueprint('main', __name__)

# Añadir función now() al contexto de la plantilla
@main.context_processor
def utility_processor():
    return dict(
        now=lambda: datetime.now(timezone.utc),
        timezone=timezone
    )

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

@main.route('/profile')
@login_required
def profile():
    # Obtener todas las contraseñas del usuario
    passwords = Password.get_all_for_user(current_user.id)
    
    # Estadísticas básicas
    last_update = passwords[0].created_at if passwords else None
    
    # Obtener dominios únicos (extraer dominio de las URLs)
    unique_domains = len(set(urlparse(p.url).netloc for p in passwords if p.url))
    
    # Contraseñas antiguas (>90 días)
    old_passwords = sum(1 for p in passwords if (datetime.utcnow() - p.created_at).days > 90)
    
    # Actividad reciente (últimas 5 contraseñas)
    recent_activities = [
        {'date': p.created_at, 'site': p.name, 'action': 'Creada'}
        for p in sorted(passwords, key=lambda x: x.created_at, reverse=True)[:5]
    ]
    
    # Calcular estadísticas de fortaleza usando el generador existente
    password_generator = PasswordGenerator()
    weak_count = medium_count = strong_count = 0
    
    for pwd in passwords:
        # Obtener contraseña descifrada usando to_dict
        pwd_data = pwd.to_dict(include_password=True, master_key=session.get('master_key'))
        if not pwd_data.get('password'):
            continue
            
        is_valid, _ = password_generator.validate_password(pwd_data['password'])
        strength = len(pwd_data['password']) + sum(1 for c in pwd_data['password'] if c.isupper()) + \
                  sum(1 for c in pwd_data['password'] if c.isdigit()) + \
                  sum(1 for c in pwd_data['password'] if not c.isalnum())
        
        if strength < 10:
            weak_count += 1
        elif strength < 15:
            medium_count += 1
        else:
            strong_count += 1
    
    total = len(passwords)
    if total > 0:
        weak_percent = (weak_count / total) * 100
        medium_percent = (medium_count / total) * 100
        strong_percent = (strong_count / total) * 100
    else:
        weak_percent = medium_percent = strong_percent = 0
    
    return render_template('profile.html',
                         passwords=passwords,
                         last_update=last_update,
                         unique_domains=unique_domains,
                         old_passwords=old_passwords,
                         recent_activities=recent_activities,
                         weak_count=weak_count,
                         medium_count=medium_count,
                         strong_count=strong_count,
                         weak_percent=weak_percent,
                         medium_percent=medium_percent,
                         strong_percent=strong_percent)
