from flask import (
    redirect, render_template, 
    request, url_for,
    Blueprint, flash
)
from models.models import Note, db
from flask_login import login_required, current_user
import logging  # ✅ Para logging profesional

notes_bp = Blueprint("notes", __name__)

@notes_bp.route("/")
@notes_bp.route("/home")
@login_required
def home():
    notes = Note.query.filter_by(user_id=current_user.id)\
                     .order_by(Note.created_at.desc())\
                     .all() 
    return render_template("index.html", notes=notes)

@notes_bp.route("/crear-notas", methods=['GET','POST'])
@login_required
def create_note():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Título y contenido son requeridos", "error")
            return render_template("note_form.html")

        new_note = Note(
            title=title, 
            content=content,
            user_id=current_user.id
        )

        try:
            db.session.add(new_note)
            db.session.commit()
            flash("Nota creada exitosamente", "success")
            return redirect(url_for("notes.home"))
        except Exception as e:  # ✅ AHORA SÍ USAMOS 'e'
            db.session.rollback()
            # Logging para desarrollo/producción
            logging.error(f"Error creando nota - User: {current_user.id}, Error: {e}")
            flash(" Error al crear la nota", "error")
    
    return render_template("note_form.html")

@notes_bp.route("/editar-nota/<int:note_id>", methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    
    if request.method == "POST":   
        title = request.form.get("title", "").strip()
        content = request.form.get("content", "").strip()

        if not title or not content:
            flash("Título y contenido son requeridos", "error")
            return render_template("edit_note.html", note=note)

        note.title = title
        note.content = content

        try:
            db.session.commit()
            flash(" Nota actualizada exitosamente", "success")
            return redirect(url_for("notes.home"))
        except Exception as e:  # USAMOS 'e'
            db.session.rollback()
            logging.error(f"Error editando nota {note_id} - User: {current_user.id}, Error: {e}")
            flash(" Error al actualizar la nota", "error")
    
    return render_template("edit_note.html", note=note)

@notes_bp.route("/eliminar-nota/<int:note_id>", methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(note)
        db.session.commit()
        flash(" Nota eliminada exitosamente", "success")
    except Exception as e:  # USAMOS 'e'
        db.session.rollback()
        logging.error(f"Error eliminando nota {note_id} - User: {current_user.id}, Error: {e}")
        flash(" Error al eliminar la nota", "error")
    
    return redirect(url_for("notes.home"))