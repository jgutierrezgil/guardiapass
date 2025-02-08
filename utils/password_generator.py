import string
import secrets
import re
import unicodedata

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        self.extended_chars = "ñçáéíóúàèìòùâêîôûäëïöüÑÇÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÄËÏÖÜ"
    
    def generate_password(self, length=12, use_lower=True, use_upper=True, 
                         use_digits=True, use_special=True, use_extended=False):
        """
        Genera una contraseña segura basada en los criterios especificados.
        
        Args:
            length (int): Longitud de la contraseña (12-60)
            use_lower (bool): Incluir minúsculas
            use_upper (bool): Incluir mayúsculas
            use_digits (bool): Incluir números
            use_special (bool): Incluir caracteres especiales
            use_extended (bool): Incluir caracteres extendidos (ñ, ç, etc.)
            
        Returns:
            str: Contraseña generada
        """
        # Validar longitud
        if not 12 <= length <= 60:
            raise ValueError("La longitud debe estar entre 12 y 60 caracteres")
            
        # Crear el conjunto de caracteres según las opciones seleccionadas
        charset = ""
        if use_lower:
            charset += self.lowercase
        if use_upper:
            charset += self.uppercase
        if use_digits:
            charset += self.digits
        if use_special:
            charset += self.special
        if use_extended:
            charset += self.extended_chars
        
        if not charset:
            charset = self.lowercase  # Conjunto por defecto si no se selecciona ninguno
        
        # Asegurar que la contraseña contiene al menos un carácter de cada tipo seleccionado
        password = []
        if use_lower:
            password.append(secrets.choice(self.lowercase))
        if use_upper:
            password.append(secrets.choice(self.uppercase))
        if use_digits:
            password.append(secrets.choice(self.digits))
        if use_special:
            password.append(secrets.choice(self.special))
        if use_extended:
            password.append(secrets.choice(self.extended_chars))
            
        # Completar el resto de la contraseña
        while len(password) < length:
            password.append(secrets.choice(charset))
            
        # Mezclar la contraseña
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def measure_strength(self, password):
        """
        Mide la fortaleza de una contraseña.
        
        Args:
            password (str): Contraseña a evaluar
            
        Returns:
            tuple: (score, str) Puntuación numérica y descripción de la fortaleza
        """
        score = 0
        feedback = []
        
        # Criterios básicos
        checks = {
            'length': len(password) >= 12,
            'uppercase': bool(re.search(r'[A-Z]', password)),
            'lowercase': bool(re.search(r'[a-z]', password)),
            'digits': bool(re.search(r'\d', password)),
            'special': bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password)),
            'extended': bool(re.search(r'[ñçáéíóúàèìòùâêîôûäëïöüÑÇÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÄËÏÖÜ]', password))
        }
        
        # Puntuación y feedback
        if checks['length']:
            score += 2
            feedback.append("Longitud adecuada")
        else:
            feedback.append("La contraseña debería tener al menos 12 caracteres")
            
        if checks['uppercase']:
            score += 1
            feedback.append("Contiene mayúsculas")
        if checks['lowercase']:
            score += 1
            feedback.append("Contiene minúsculas")
        if checks['digits']:
            score += 1
            feedback.append("Contiene números")
        if checks['special']:
            score += 2
            feedback.append("Contiene caracteres especiales")
        if checks['extended']:
            score += 1
            feedback.append("Contiene caracteres extendidos")
            
        # Bonus por longitud extra
        score += len(password) // 8
        
        # Penalizaciones
        # Patrones repetitivos
        if re.search(r'(.)\1{2,}', password):
            score -= 1
            feedback.append("Evita caracteres repetitivos")
            
        # Secuencias comunes
        common_sequences = ['123', 'abc', 'qwerty']
        if any(seq in password.lower() for seq in common_sequences):
            score -= 1
            feedback.append("Evita secuencias comunes")
        
        # Categorización final
        if score >= 8:
            strength = "Muy fuerte"
        elif score >= 6:
            strength = "Fuerte"
        elif score >= 4:
            strength = "Moderada"
        else:
            strength = "Débil"
            
        return {
            'score': score,
            'strength': strength,
            'feedback': feedback
        }
    
    def validate_password(self, password):
        """
        Valida si una contraseña cumple con los requisitos mínimos.
        
        Args:
            password (str): Contraseña a validar
            
        Returns:
            tuple: (bool, list) True si es válida, False si no, y lista de errores
        """
        errors = []
        
        if len(password) < 12:
            errors.append("La contraseña debe tener al menos 12 caracteres")
        if len(password) > 60:
            errors.append("La contraseña no puede tener más de 60 caracteres")
        if not re.search(r'[A-Z]', password):
            errors.append("Debe contener al menos una mayúscula")
        if not re.search(r'[a-z]', password):
            errors.append("Debe contener al menos una minúscula")
        if not re.search(r'\d', password):
            errors.append("Debe contener al menos un número")
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
            errors.append("Debe contener al menos un carácter especial")
            
        return len(errors) == 0, errors