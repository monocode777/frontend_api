from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import requests
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'clave-secreta-frontend'

# Configuración de la API principal
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:5000')

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def set_token(self, token):
        """Configurar token JWT para las peticiones"""
        self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    def clear_token(self):
        """Limpiar token JWT"""
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
    
    def login(self, email, password):
        """Iniciar sesión en la API"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={'email': email, 'password': password}
            )
            return response
        except requests.exceptions.ConnectionError:
            return None
    
    def register(self, email, password):
        """Registrar usuario en la API"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json={'email': email, 'password': password}
            )
            return response
        except requests.exceptions.ConnectionError:
            return None
    
    def get_videojuegos(self):
        """Obtener lista de videojuegos"""
        try:
            response = self.session.get(f"{self.base_url}/api/videojuegos")
            return response
        except requests.exceptions.ConnectionError:
            return None
    
    def get_profile(self):
        """Obtener perfil del usuario"""
        try:
            response = self.session.get(f"{self.base_url}/api/auth/profile")
            return response
        except requests.exceptions.ConnectionError:
            return None

# Instancia del cliente API
api_client = APIClient(API_BASE_URL)

# Rutas del frontend
@app.route('/')
def index():
    """Página principal"""
    if 'access_token' in session:
        api_client.set_token(session['access_token'])
        profile_response = api_client.get_profile()
        if profile_response and profile_response.status_code == 200:
            user_data = profile_response.json()
            return render_template('index.html', user=user_data)
    
    return render_template('index.html', user=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        response = api_client.login(email, password)
        
        if response is None:
            flash('Error de conexión con la API', 'error')
            return render_template('login.html')
        
        if response.status_code == 200:
            data = response.json()
            session['access_token'] = data['access_token']
            session['user_email'] = email
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            error_msg = response.json().get('msg', 'Error en el login')
            flash(error_msg, 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        response = api_client.register(email, password)
        
        if response is None:
            flash('Error de conexión con la API', 'error')
            return render_template('register.html')
        
        if response.status_code == 201:
            flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        else:
            error_msg = response.json().get('msg', 'Error en el registro')
            flash(error_msg, 'error')
    
    return render_template('register.html')

@app.route('/videojuegos')
def videojuegos():
    """Página de videojuegos"""
    if 'access_token' not in session:
        flash('Debes iniciar sesión para ver los videojuegos', 'error')
        return redirect(url_for('login'))
    
    api_client.set_token(session['access_token'])
    response = api_client.get_videojuegos()
    
    if response is None:
        flash('Error de conexión con la API', 'error')
        return render_template('videojuegos.html', videojuegos=[])
    
    if response.status_code == 200:
        videojuegos_data = response.json()
        return render_template('videojuegos.html', videojuegos=videojuegos_data)
    else:
        flash('Error al obtener los videojuegos', 'error')
        return render_template('videojuegos.html', videojuegos=[])

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    api_client.clear_token()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/api/health')
def health_check():
    """Verificar estado de la conexión con la API"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/health")
        return jsonify({
            'frontend_status': 'healthy',
            'api_status': 'connected' if response.status_code == 200 else 'error',
            'api_response': response.json() if response.status_code == 200 else None
        })
    except requests.exceptions.ConnectionError:
        return jsonify({
            'frontend_status': 'healthy',
            'api_status': 'disconnected',
            'api_response': None
        }), 503

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    host = '0.0.0.0'
    
    print(f"Frontend iniciado en http://{host}:{port}")
    print(f"Conectado a API: {API_BASE_URL}")
    
    app.run(host=host, port=port, debug=True)