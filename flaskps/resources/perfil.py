from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.user_model import Usuario
from flaskps.models.perfil import Perfil

def render_menu():
    set_db()
    perfiles = Perfil.all_with_id(session['usuario_id'])
    plan = Usuario.find_by_id(session['usuario_id'])['subscription']
    print(plan)
    esPremium = plan == 'premium'     
    print(esPremium)
    return render_template("perfil/menu.html", perfiles=perfiles, esPremium=esPremium)

def select(id):
    session['perfil'] = id
    return redirect(url_for("book_menu"))

def new():    
    return render_template("perfil/new.html")

def create():
    set_db()
    perfiles = Perfil.all_with_id(session['usuario_id'])
    plan = Usuario.find_by_id(session['usuario_id'])['subscription']
    print(plan)
    print(len(perfiles))
    if plan == 'basic' and len(perfiles)==2: # es una mierda este codigo, lo se
        flash("Su plan no permite más perfiles")
        return redirect(url_for("perfil_menu"))
    if plan == 'premium' and len(perfiles)==4:
        flash("No se puede tener más de 4 perfiles")
        return redirect(url_for("perfil_menu"))    
    if validate_perfil(request.form.get("nombre"), perfiles):
        Perfil.create(request.form.get("nombre"), session['usuario_id'])
    else:
        flash("Ya existe un perfil con ese nombre")
        redirect(url_for("perfil_new"))
    return redirect(url_for("perfil_menu"))

def delete(id):
    set_db()
    perfiles = Perfil.all_with_id(session['usuario_id'])
    if len(perfiles)>1:
        Perfil.delete(id)
    else:
        flash("No puede borrar el único perfil")
    return redirect(url_for("perfil_menu"))


def to_premium():    
    set_db()
    Usuario.toPremium(session['usuario_id'])
    return redirect(url_for("perfil_menu"))

def to_basic():    
    set_db()
    perfiles = Perfil.all_with_id(session['usuario_id'])
    plan = Usuario.find_by_id(session['usuario_id'])['subscription']    
    if plan == 'premium' and len(perfiles)>2: # es una mierda este codigo, lo se
        flash("No puede tener mas de 2 perfiles si pasa a basico. Elimine los necesarioss")
        return redirect(url_for("perfil_menu"))
    Usuario.toPremium(session['usuario_id'])
    return redirect(url_for("perfil_menu"))
    
    

def validate_perfil(perfil, perfiles):
    for p in perfiles:
        if p['nombre'] == perfil:
            return False
    return True
def set_db():
    Perfil.db = get_db()
    Usuario.db = get_db()    
    return None