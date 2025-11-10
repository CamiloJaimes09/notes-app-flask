from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.models import User, db
from flask_login import login_user, logout_user, login_required  # ✅ Solo lo necesario

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/registro", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verificaciones
        if User.query.filter_by(username=username).first():
            flash("Usuario ya existe", "error")
            return redirect(url_for("auth.register"))
        
        if User.query.filter_by(email=email).first():
            flash("El correo ya esta en uso", "error")
            return redirect(url_for("auth.register"))
        
        # Crear usuario
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash("Usuario creado exitosamente", "success")
        return redirect(url_for("auth.login"))  # ✅ Sin código 201
    
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Login Exitoso", "success")
            return redirect(url_for("notes.home"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
    
    return render_template("auth/login.html")

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('auth.login'))