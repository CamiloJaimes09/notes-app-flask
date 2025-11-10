# 📝 Notes App 

Una aplicación web moderna para gestionar notas, con autenticación de usuarios y diseño responsive.

## 🚀 Características Principales

- **🔐 Autenticación segura** - Registro, login y logout
- **📒 CRUD de notas** - Crear, leer, editar y eliminar notas
- **👤 Notas personales** - Cada usuario ve solo sus notas
- **🎨 Interfaz moderna** - Diseño con Tailwind CSS
- **🛡️ Rutas protegidas** - Seguridad con Flask-Login

## 🛠️ Tecnologías

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Base de datos**: SQLite

## ⚡ Instalación Rápida

```bash
# 1. Clonar y entrar al proyecto
git clone https://github.com/TU_USUARIO/notes-app-flask.git
cd notes-app-flask

# 2. Entorno virtual y dependencias
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Base de datos
flask db upgrade

# 4. Ejecutar
flask run
