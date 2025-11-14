from flask import Flask, render_template, request, redirect, url_for, session, flash
import requests
import os
import json

app = Flask(__name__)
app.secret_key = 'clave-secreta-frontend'

# Configuración - LOCALHOST para desarrollo
API_BASE_URL = "http://localhost:5000"
print(f"🔗 Conectando a: {API_BASE_URL}")

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
    
    def login(self, email, password):
        try:
            print(f"🔐 Intentando login para: {email}")
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json={'email': email, 'password': password},
                timeout=5
            )
            print(f"📡 Respuesta login - Status: {response.status_code}")
            print(f"📡 Respuesta login - Body: {response.text}")
            return response
        except Exception as e:
            print(f"❌ Error de conexión en login: {e}")
            return None
    
    def register(self, email, password):
        try:
            print(f"📝 Intentando registro para: {email}")
            response = self.session.post(
                f"{self.base_url}/api/auth/register",
                json={'email': email, 'password': password},
                timeout=5
            )
            print(f"📡 Respuesta registro - Status: {response.status_code}")
            print(f"📡 Respuesta registro - Body: {response.text}")
            return response
        except Exception as e:
            print(f"❌ Error de conexión en registro: {e}")
            return None
    
    def get_videojuegos(self):
        try:
            response = self.session.get(f"{self.base_url}/api/videojuegos", timeout=5)
            return response
        except:
            return None

api_client = APIClient(API_BASE_URL)

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        print(f"🔄 Procesando login para: {email}")
        response = api_client.login(email, password)
        
        if response and response.status_code == 200:
            session['user_email'] = email
            flash('¡Login exitoso!', 'success')
            return redirect('/videojuegos')
        else:
            error_msg = 'Error en el login'
            if response:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('msg', error_msg)
                except:
                    error_msg = f"Error {response.status_code}"
            flash(error_msg, 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        print(f"🔄 Procesando registro para: {email}")
        response = api_client.register(email, password)
        
        if response and response.status_code == 201:
            flash('¡Registro exitoso! Ahora puedes iniciar sesión.', 'success')
            return redirect('/login')
        else:
            error_msg = 'Error en el registro'
            if response:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('msg', error_msg)
                    print(f"❌ Error específico: {error_msg}")
                except:
                    error_msg = f"Error {response.status_code}: {response.text}"
                    print(f"❌ Error sin JSON: {error_msg}")
            flash(error_msg, 'error')
    
    return render_template('register.html')

@app.route('/videojuegos')
def videojuegos():
    if 'user_email' not in session:
        flash('Debes iniciar sesión primero', 'error')
        return redirect('/login')
    
    response = api_client.get_videojuegos()
    videojuegos = response.json() if response and response.status_code == 200 else []
    
    return render_template('videojuegos.html', 
                         videojuegos=videojuegos, 
                         user_email=session['user_email'])

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'success')
    return redirect('/')

if __name__ == '__main__':
    print("🚀 Frontend iniciado en http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True)