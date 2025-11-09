from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime,date
import os

app = Flask(__name__)

DB_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "notes.sqlite"
)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Corrección del typo

db = SQLAlchemy(app)
migrate = Migrate(app, db) 

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"

# @app.route("/home")
# def home():
#     role = "admin" #podemos definir roles o niveles de administracion
#     now = date.today()
#     notes = [
#         {"title":"Nota 1", "content":"Descripcion de la nota 1", "date":now},
#         {"title":"Nota 2", "content":"Descripcion de la nota 2", "date":now},
#         {"title":"Nota 3", "content":"Descripcion de la nota 3", "date":now},
#         {"title":"Nota 4", "content":"Descripcion de la nota 4", "date":now}
    
#     ]
#     return render_template("index.html", role = role, notes = notes)

@app.route("/")
@app.route("/home")
def home():
    now = date.today()
    notes = Note.query.all()
    return render_template("index.html", notes = notes)


#Vamos a definir una ruta en la que utilizaremos un metodo post, teniendo en cuenta que todas las rutas por defecto tienen el metodo get
@app.route("/contact", methods=['GET', 'POST']) #indicamos el metodo a usar
def contact():
    #Validamos el tipo de metodo que estamos recibiendo
    if request.method == "POST":
        return "FORMULARIO DILIGENCIADO O ENVIADO CORRECTAMENTE",201 #Enviamos un mensaje de confimración y un codigo 201 "creado"
    #--> Untruco para hacer una peticion HTTP de prueba por consola, es con "curl" curl.exe -i -X POST http://127.0.0.1:5000/contacto
    return "Pagina de contacto"

@app.route("/contact/delete", methods=['GET','DELETE'])
def delete():
    if request.method == "DELETE":
        return "FORMULARIO ELIMINADO CORRECTAMENTE"
    return "PAGINA DE INICIO"

# @app.route("/confirmacion")
# def confirmation():
#     note = request.args.get("new_note","No se encontró tu nota 😨")
#     return render_template("confirmation.html", note=note)

@app.route("/crear-notas", methods=['GET','POST'])
def create_note():
    if request.method == "POST":
        title = request.form.get("title","")
        content = request.form.get("content","")

        new_note = Note(
            title=title, content=content
        )

        db.session.add(new_note)
        db.session.commit()
        return redirect(
            url_for("home")
        )
    return render_template("note_form.html")

@app.route("/editar-nota/<int:note_id>", methods=['GET', 'POST']) #La variable que pasaremos como argumento, debe coincidir con el nombre del parametro en la funcion
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if request.method == "POST":   
        #Guardamos en variables las nuevos variables
        title = request.form.get("title","")
        content = request.form.get("content","")

        #y las pasamos a la base de datos
        note.title = title
        note.content = content

        #guardamos
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit_note.html", note=note)

@app.route("/eliminar-nota/<int:note_id>", methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if not note:
        return redirect(url_for("home"))
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("home"))


#Flask nos permite el formateo, o envio de respuestas al cliente en formato json
@app.route("/api/info")
def api_info():
    data = {
        "name":"Notes App",
        "version": "1.1.1"
    }
    return jsonify(data), 200

# #Para poder que la palicación corra, debemos ejecutar el metodo "run"
# if __name__ == "__main__": #Verifica que estemos ejecutando el main "app.py"
#     app.run(debug=True)
#Para ahorrar estas lineas y evitar conflictos con github o servidores externos utlizamos:
#flask run para levantar el servidor y flask run --debug para activar el debugger



