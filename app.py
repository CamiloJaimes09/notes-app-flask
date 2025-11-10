from flask import Flask, request, redirect, url_for
from config import Config
from models.models import db, User
from blueprints.notes.routes import notes_bp
from blueprints.auth.routes import auth_bp
from flask_migrate import Migrate
from flask_login import LoginManager, current_user

app = Flask(__name__)

# Configuración de la aplicación
app.config.from_object(Config)
db.init_app(app)

# Registrar Blueprints
app.register_blueprint(notes_bp)
app.register_blueprint(auth_bp)

# Configurar Flask-Migrate
migrate = Migrate(app, db)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Ruta de login
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
login_manager.login_message_category = 'error'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Ruta principal - Redirigir a home de notas si está autenticado, sino a login
@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('notes.home'))
    else:
        return redirect(url_for('auth.login'))

@app.route("/acerca-de")
def about():
    return "Esto es una app de notas"

@app.route("/contacto", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return "Formulario enviado correctamente", 201
    return "Página de contacto"

# Context processor para hacer current_user disponible en todos los templates
@app.context_processor
def inject_user():
    return dict(current_user=current_user)

# Manejo de errores básico
@app.errorhandler(404)
def not_found_error(error):
    return "Página no encontrada", 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return "Error interno del servidor", 500

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)