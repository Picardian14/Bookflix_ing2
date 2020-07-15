from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db
import datetime as dt

from flaskps.models.novedad import Novedad
from flaskps.models.configuracion import Configuracion



def new():
    today = dt.datetime.now()
    return render_template("novedad/new.html", today=today)
 
def create():
    set_db()    
    Configuracion.db = get_db()
    Novedad.create(request.form)
    flash("Novedad cargada")
    return redirect(url_for("novedad_index"))

def index():
    set_db()
    novedades = Novedad.all()
    admPermit = "configuracion_usarInhabilitado" in session['permisos']
    user_id=session['usuario_id']
    return render_template("novedad/menu.html", novedades=novedades, adm=admPermit, user_id=user_id)


def list():
    set_db()
    novedades = Novedad.all()
    # Paginacion
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
           i=0
    elif (i*pag >= len(novedades)):
        i = i - 1
    admPermit = "configuracion_usarInhabilitado" in session['permisos']
    user_id= session['usuario_id']
    return render_template("novedad/list.html", novedades=novedades, adm=admPermit, i=i,pag=pag, user_id=user_id)



def renderEdit_novedad(id):
    set_db()
    nov = Novedad.find_novedad_by_id(id)
    user_id=session['usuario_id']
    return render_template("novedad/edit.html", nov=nov, user_id=user_id)


def edit_novedad(id):
    set_db()
    if request.method == "POST":
        if request.form['titulo']:
            titulo = request.form['titulo']
            Novedad.editTitulo(titulo,id)
            flash("Cambios realizados exitosamente.")
        if request.form['descripcion']:
            descripcion = request.form['descripcion']
            Novedad.editDetalle(descripcion,id)
            flash("Cambios realizados exitosamente.")
    return redirect(url_for("novedad_list"))


def remove_novedad(id):
    set_db()
    Novedad.deleteNovedad(id)
    flash('Novedad borrada exitosamente.')
    return redirect(url_for("novedad_list"))


def set_db():
    Novedad.db = get_db()