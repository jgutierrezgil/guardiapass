import anthropic
from typing import List, Dict, Any

class AIHandler:
    def __init__(self, api_key: str):
        self.client = anthropic.Client(api_key)
    
    def analyze_passwords(self, password_info: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analiza un conjunto de contraseñas usando IA.
        No se pasan las contraseñas reales, solo metadata.
        """
        try:
            # Crear un prompt para el análisis
            prompt = f"""Analiza la siguiente información de contraseñas y proporciona recomendaciones de seguridad:
            
            Información de contraseñas:
            {password_info}
            
            Por favor, proporciona:
            1. Patrones de riesgo identificados
            2. Recomendaciones específicas de mejora
            3. Evaluación general de la seguridad
            """
            
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                'analysis': response.content[0].text,
                'success': True
            }
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }
    
    def get_password_suggestions(self, url: str, context: Dict = None) -> Dict[str, Any]:
        """
        Obtiene sugerencias para la gestión de contraseñas de un sitio específico.
        """
        try:
            # Crear un prompt para sugerencias
            prompt = f"""Para el sitio web {url}, proporciona recomendaciones de seguridad:
            
            Contexto adicional:
            {context if context else 'No se proporcionó contexto adicional'}
            
            Por favor, proporciona:
            1. Requisitos típicos de contraseña para este tipo de sitio
            2. Mejores prácticas de seguridad
            3. Consideraciones especiales si las hay
            """
            
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                'suggestions': response.content[0].text,
                'success': True
            }
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }
    
    def audit_security_practices(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza una auditoría de las prácticas de seguridad del usuario.
        """
        try:
            prompt = f"""Analiza las siguientes prácticas de seguridad y proporciona una auditoría:
            
            Datos del usuario:
            {user_data}
            
            Por favor, proporciona:
            1. Evaluación de las prácticas actuales
            2. Áreas de mejora identificadas
            3. Recomendaciones prácticas
            4. Puntuación de seguridad general
            """
            
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return {
                'audit': response.content[0].text,
                'success': True
            }
        except Exception as e:
            return {
                'error': str(e),
                'success': False
            }