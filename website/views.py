from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
  if request.method == 'POST':
    note = request.form.get('note')

    if len(note) < 1:
      flash('A nota é pequena demais', category='error')
    else:
      new_note = Note(text=note, user_id=current_user.id)
      db.session.add(new_note)
      db.session.commit()
      flash('Nota adicionada!', category='success')
      print (new_note.text)

  return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
  note = json.loads(request.data)
  noteId = note['noteId']
  note = Note.query.get(noteId)
  if note:
    if note.user_id == current_user.id:
      db.session.delete(note)
      db.session.commit()
    flash('Nota removida!', category='success')

  return note.user_id