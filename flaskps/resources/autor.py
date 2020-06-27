from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.configuracion import Configuracion
from flaskps.models.autor import Autor

def new():
    return render_template('autor/new.html')

def create():
    set_db()
    if validate(request.form.get('nombre')):
        Autor.create(request.form)
        flash("Autor cargado")
    return redirect(url_for("book_menu", type='all'))

def set_db():
    Autor.db = get_db()

def validate(name): 
    validate = True
    autores = Autor.all()
    for user in autores:
        if user.get('nombre').lower() == name.lower():                                           
            validate = False
            break
    return validate