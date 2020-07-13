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
    # Paginacion
    i = int(request.args.get('i',0))
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag >= len(novedades)):
        i = i - 1
    admPermit = "configuracion_usarInhabilitado" in session['permisos']
    return render_template("novedad/menu.html", novedades=novedades, adm=admPermit, i=i,pag=pag)


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
    return render_template("novedad/list.html", novedades=novedades, adm=admPermit, i=i,pag=pag)



def renderEdit_novedad(id):
    set_db()
    nov = Novedad.find_novedad_by_id(id)
    return render_template("novedad/edit.html", nov=nov)


def edit_novedad(id):
    set_db()
    Novedad.editNovedad(request.form, id)
    return redirect(url_for("novedad_list"))


def remove_novedad(id):
    set_db()
    Novedad.deleteNovedad(id)
    return redirect(url_for("novedad_list"))


def set_db():
    Novedad.db = get_db()

