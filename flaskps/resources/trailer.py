from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.configuracion import Configuracion
from flaskps.models.book import Book
from flaskps.models.autor import Autor
from flaskps.models.editorial import Editorial
from flaskps.models.genero import Genero
from flaskps.models.comentario import Comentario
from flaskps.models.trailer import Trailer

from werkzeug.utils import secure_filename

import datetime as dt
import os


def new():
    user_id= session['usuario_id']
    return render_template("trailers/new.html", user_id=user_id)


def render_trailer():
    set_db()
    titulos = list(map(lambda metadato: metadato['titulo'],Trailer.allMeta()))
    isbns = list(map(lambda metadato: metadato['isbn'], Trailer.allMeta()))
    user_id= session['usuario_id']
    return render_template('trailers/new.html', titulos = titulos, isbns = isbns, user_id=user_id)



def edit_trailer(tID):
    set_db()
    info = Trailer.getTrailerByID(tID)
    user_id= session['usuario_id']
    return render_template('trailers/editTrailer.html', t = info, id= tID, user_id=user_id)


def load_edit(tID):
    set_db()
    if request.method == "POST":
        if request.form['titulo']:
            cambiado = 1
            Trailer.updateTitle(tID, request.form['titulo'])
            flash("Titulo modificado exitosamente.")
        if request.files:
            cambiado = 1
            archivo = request.files['archivo']
            filename = secure_filename(archivo.filename)
            if filename:
                if not os.path.exists('flaskps/static/uploads/'+ filename):
                    os.mkdir('flaskps/static/uploads/'+filename)
                archivo.save(os.path.join('flaskps/static/uploads/'+filename, filename))        
                Trailer.updateFilename(filename,tID)
                flash("Archivo modificado exitosamente.")
    return redirect(url_for("book_menu"))



def load_trailer():
    set_db()
    if request.files:
        titulo = request.form['titulo']
        archivo = request.files['archivo']
        filename = secure_filename(archivo.filename)
        if not os.path.exists('flaskps/static/uploads/'+titulo):
            os.mkdir('flaskps/static/uploads/'+titulo)            
        archivo.save(os.path.join('flaskps/static/uploads/'+titulo,filename))
        Trailer.setTrailer(request.form, filename)
        flash("Trailer cargado")
        return redirect(url_for("book_menu"))




def open_trailer(tID):
    print("abro")
    set_db()
    titulo = Trailer.tituloById(tID)['titulo']
    nombre = Trailer.filenameById(tID)['archivo']
    user_id= session['usuario_id']
    return render_template('trailers/abrirTrailer.html',titulo=titulo, nombre=nombre, user_id=user_id)



def open_trailer_asociado(isbn):
    print("abro")
    set_db()
    titulo = Trailer.tituloByIsbn(isbn)['titulo']
    nombre = Trailer.filenameByIsbn(isbn)['archivo']
    user_id= session['usuario_id']
    return render_template('trailers/abrirAsociado.html',titulo=titulo, nombre=nombre, user_id=user_id)



def remove_view(tID):
    set_db()
    user_id= session['usuario_id']
    return render_template('trailers/eliminarTrailer.html',id =tID, user_id=user_id)


def remove_done(tID):
    set_db()
    Trailer.deleteTrailer(tID)
    flash('Trailer eliminado exitosamente')
    return redirect(url_for("book_menu"))




def new_asociado(isbn):
    set_db()
    libro = Book.find_meta_by_isbn(isbn)
    user_id= session['usuario_id']
    return render_template('trailers/newAsociado.html', libro=libro, isbn=isbn, user_id=user_id)



def load_asociado(isbn):
    set_db()
    if request.files:
        titulo = request.form['titulo']
        archivo = request.files['archivo']
        filename = secure_filename(archivo.filename)
        if not os.path.exists('flaskps/static/uploads/'+titulo):
            os.mkdir('flaskps/static/uploads/'+titulo)            
        archivo.save(os.path.join('flaskps/static/uploads/'+titulo,filename))
        Trailer.setTrailerAsociado(request.form, filename, isbn)
        flash("Trailer cargado")
        return redirect(url_for("book_menu"))



def set_db():
    Trailer.db = get_db()
