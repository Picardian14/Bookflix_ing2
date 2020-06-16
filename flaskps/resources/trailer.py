import os
from flask import Flask, redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.configuracion import Configuracion
from flaskps.models.trailer import Trailer
from werkzeug.utils import secure_filename

def new():
    set_db()
    return render_template("trailers/new.html")

def create():
    set_db()
    if request.files:
        titulo = request.files['titulo']
        archivo = request.files['archivo']
        if not os.path.exists('flaskps/static/uploads/'+titulo):
            os.mkdir('flaskps/static/uploads/'+titulo)
        archivo.save(os.path.join('flaskps/static/uploads'+titulo, titulo+"_full.mp4"))
    #Trailer.setTrailer(request.form,titulo+"_full.mp4")
    flash ("trailer cargado")
    Trailer.create(request.form, titulo+"_full.mp4")
    return redirect(url_for("trailer_menu"))


def render_trailer():
    set_db()
    trailers = Trailer.getTrailers()    
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag >= len(trailers)):
        i = i - 1
    adm = "configuracion_usarInhabilitado" in session['permisos'] #Permiso que solo tiene un administrador
    return render_template('trailers/new_trailer.html', trailers=trailers, i=i, pag=pag, adm=adm)


def load_trailer():
    set_db()
    if request.method=="POST":
        titulo = request.form['titulo']
        archivo = request.files['archivo']
        filename = secure_filename(archivo.filename)
        if not os.path.exists('flaskps/static/uploads/'+titulo):
            os.mkdir('flaskps/static/uploads/'+titulo)
        archivo.save(os.path.join('flaskps/static/uploads',filename))
        flash ("El trailer fue cargado exitosamente")
        Trailer.create(request.form, filename)    
        return redirect(url_for("trailer_menu"))

#funca
def render_menu():
    set_db()    
    trailers = Trailer.getTrailers()    
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag >= len(trailers)):
        i = i - 1
    adm = "configuracion_usarInhabilitado" in session['permisos'] #Permiso que solo tiene un administrador
    return render_template('trailers/menu.html', trailers=trailers, i=i, pag=pag, adm=adm)

#funca
def remove_trailer(id):
    set_db()
    Trailer.deleteTrailer(id)
    flash('El trailer fue borrado exitosamente')
    return redirect(url_for("trailer_menu"))




#funca
def edit_trailer(id):
    set_db()
    trailer = Trailer.getTrailerByID(id)
    return render_template('trailers/edit_trailer.html', trailer = trailer, id = id)

def load_edit(id):
    set_db()
    trailer = Trailer.getTrailerByID(id)
    if request.method == "POST":
        titulo = request.form['titulo']
        Trailer.updateTrailer(titulo,id)
        return redirect(url_for("trailer_menu"))


#funca
def set_db():
    Trailer.db = get_db()
