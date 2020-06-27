from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db

from flaskps.models.configuracion import Configuracion
from flaskps.models.book import Book
from flaskps.models.autor import Autor
from flaskps.models.editorial import Editorial
from flaskps.models.genero import Genero

from flaskps.helpers.mergepdf import merger
import datetime as dt
import os

def search_by():
    def filter_by(criteria, name, book):
        return name in book[criteria].lower()
    
    set_db()
    books = Book.allMeta()
    criteria = request.form.get('busqueda')
    name = request.form.get('nombre').lower()
    selected = list(filter(lambda book: filter_by(criteria, name, book), books))

    return selected

def history():
    return Book.get_last_read(session['usuario']) #ACA SERIA session['perfil']

def render_menu():
    set_db()    
    book_for={}
    book_type = request.args.get('type','all')    
    book_for['all'] = Book.allMeta
    book_for['search_by'] = search_by if request.form.get('nombre') is not None else Book.allMeta
    book_for['history'] = history
    books = book_for[book_type]()
    venc = list(map(lambda meta: validate_date(meta['isbn']), books))
    hasChapters = list(map(lambda meta: Book.allChapter(meta['isbn'])!=(), books))
    print("Lista de tiene capitulos")
    print(hasChapters)

    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag >= len(books)):
        i = i - 1
    adm = "configuracion_usarInhabilitado" in session['permisos'] #Permiso que solo tiene un administrador
    return render_template('books/menu.html', books=books, i=i, pag=pag, adm=adm, canReadBook=venc, hasChapters=hasChapters)

def search():
    def filter_by(criteria, name, book):
        return name in book[criteria].lower()

    set_db()
    books = Book.allMeta()
    criteria = request.form.get('busqueda')
    name = request.form.get('nombre').lower()
    print(name)
    selected = list(filter(lambda book: filter_by(criteria, name, book), books))
    print(selected)
    venc = list(map(lambda meta: validate_date(meta['isbn']), selected))
    hasChapters = list(map(lambda meta: Book.allChapter(meta['isbn'])!=(), selected))
    i = int(request.args.get('i',0))
    Configuracion.db = get_db()
    pag=Configuracion.get_page_size()
    if (i == -1):
        i=0
    elif (i*pag >= len(books)):
        i = i - 1
    adm = "configuracion_usarInhabilitado" in session['permisos'] #Permiso que solo tiene un administrador
    return render_template('books/menu.html', books=selected, i=i, pag=pag, adm=adm, canReadBook=venc, hasChapters=hasChapters)

#creacion de libros
def new(isbn):
    set_db()
    if validate_book_isbn(isbn):
        caps = Book.allChapter(isbn)
        if(caps==()):
            titulo = Book.find_meta_by_isbn(isbn)['titulo']
            today = dt.datetime.now().strftime("%Y-%m-%d")
            return render_template('books/new.html', isbn=isbn, titulo=titulo, today=today)
        else:
            flash("Ya se han cargado capitulos")
    else:
        flash("Ya hay un libro cargado")
    return redirect(url_for("book_menu"))
    

def create(isbn): #Crea / Guarda un archivo de libro
    set_db()
    if validate_book_isbn(isbn) and not Book.is_complete(isbn):    
        if request.files: 
            archivo = request.files['archivo']
            book_name = Book.find_meta_by_isbn(isbn)['titulo']  
            if not os.path.exists('flaskps/static/uploads/'+book_name):          
                os.mkdir('flaskps/static/uploads/'+book_name)        
            archivo.save(os.path.join('flaskps/static/uploads/'+book_name, book_name+"_Full.pdf"))
        Book.create(request.form, book_name+"_Full.pdf",isbn)
        Book.mark_complete(isbn)
        print(Book.is_complete(isbn))
        flash("Libro cargado")
    else:
        flash("Ya existe un libro con el mismo ISBN")
    return redirect(url_for("book_menu"))

#Creacion de capitulo
def new_chapter(isbn):
    set_db()
    if not Book.is_complete(isbn):
        titulo = Book.find_meta_by_isbn(isbn)['titulo']
        today = dt.datetime.now().strftime("%Y-%m-%d")
        return render_template('books/new_chapter.html', isbn=isbn, titulo=titulo, today=today)
    else:
        if validate_book_isbn(isbn):
            flash("Ya se cargaron todos los capitulos")
        else:
            flash("Ya se cargó el libro")
    return redirect(url_for("book_menu"))
    

def create_chapter(isbn):
    set_db()
    print("Crea cap")
    if not Book.is_complete(isbn):    
        if request.files: 
            archivo = request.files['archivo']
            book_name = Book.find_meta_by_isbn(isbn)['titulo']
            chapter_name = book_name + "_cap_"+str(request.form['num'])+".pdf"
            if not os.path.exists('flaskps/static/uploads/'+book_name):
                os.mkdir('flaskps/static/uploads/'+book_name)            
            if validate_chapter_isbn(isbn, request.form['num']):
                archivo.save(os.path.join('flaskps/static/uploads/'+book_name, chapter_name))
                Book.create_chapter(request.form, chapter_name,isbn)
            else:
                flash("El capitulo  ya fue cargado")#+str(request.form['num']+
                return redirect(url_for("book_new_chapter", isbn=isbn))
        
        if request.form['completo']=="True":            
            Book.mark_complete(isbn)
            merger(book_name)
        
        flash("Capitulo cargado")
    else:
        flash("Ya se cargo todo el libro")
    print("Hizo todo")
    return redirect(url_for("book_menu"))



#crud de metadatos
def render_meta():
    set_db()
    autores = list(map(lambda autor: autor['nombre'],Autor.all()))
    editoriales = list(map(lambda editorial: editorial['nombre'],Editorial.all()))
    generos = list(map(lambda genero: genero['nombre'],Genero.all()))
    return render_template('books/new_meta.html', autores=autores, editoriales=editoriales, generos=generos)

def load_meta():
    set_db()
    
    autor = Autor.find_by_name(request.form['autor'])
    if autor == None:
        new_autor =request.form['autor']
        Autor.create({'nombre':new_autor})
        autor_id = Autor.find_by_name(new_autor)['id']
    else:
        autor_id = autor['id']

    editorial = Editorial.find_by_name(request.form['editorial'])

    if editorial == None:
        new_Editorial =request.form['editorial']
        Editorial.create({'nombre':new_Editorial})
        Editorial_id = Editorial.find_by_name(new_Editorial)['id']
    else:
        Editorial_id = editorial['id']

    genero = Genero.find_by_name(request.form['genero'])
    if genero == None:
        new_Genero =request.form['genero']
        Genero.create({'nombre':new_Genero})
        Genero_id = Genero.find_by_name(new_Genero)['id']
    else:
        Genero_id = genero['id']    
    if validate_meta_isbn(request.form['isbn']):
        
        Book.loadMeta(request.form, autor_id, Editorial_id, Genero_id)
        flash("Metadatos cargados")
    else:
        flash("Ya existe un libro con el mismo ISBN")
        return redirect(url_for("book_meta"))
    
    
    return redirect(url_for("book_menu"))

def edit_meta(isbn):
    set_db()
    autores = Autor.all()
    editoriales = Editorial.all()
    generos = Genero.all()
    book=Book.find_meta_by_isbn(isbn)    
    book['autor'] = Autor.find_by_id(book['autor_id'])['nombre']
    book['editorial'] = Editorial.find_by_id(book['editorial_id'])['nombre']
    book['genero'] = Genero.find_by_id(book['genero_id'])['nombre']
    print(book)
    return render_template('books/edit_meta.html',book=book, isbn=isbn, autores=autores, editoriales=editoriales, generos=generos)

def load_edit_meta(isbn):
    set_db()
    
    book = Book.find_meta_by_isbn(isbn)
    
    book_data = {}
    
    book_data['titulo'] = request.form.get('titulo') if (request.form.get('titulo') != '') else book['titulo']
    book_data['sinopsis'] = request.form.get('sinopsis') if (request.form.get('sinopsis') != '') else book['sinopsis']
    if request.form.get('autor') != '':
        print("se carga lo ingresado")
        autor = Autor.find_by_name(request.form['autor'])
        if autor == None:
            new_autor =request.form['autor']
            Autor.create({'nombre':new_autor})
            autor_id = Autor.find_by_name(new_autor)['id']
        else:
            autor_id = autor['id']
    else:
        print("Se carga lo previo")
        autor_id = book['autor_id']

    if request.form.get('editorial') != '':
        print("se carga lo ingresado")
        editorial = Editorial.find_by_name(request.form['editorial'])
        if editorial == None:
            new_Editorial =request.form['editorial']
            Editorial.create({'nombre':new_Editorial})
            Editorial_id = Editorial.find_by_name(new_Editorial)['id']
        else:
            Editorial_id = editorial['id']
    else:
        print("Se carga lo previo")
        Editorial_id = book['editorial_id']

    if request.form.get('genero') != '':
        print("se carga lo previo")
        genero = Genero.find_by_name(request.form['genero'])
        if genero == None:
            new_Genero =request.form['genero']
            Genero.create({'nombre':new_Genero})
            Genero_id = Genero.find_by_name(new_Genero)['id']
        else:            
            Genero_id = genero['id']
    else:
        print("Se carga lo previo")
        Genero_id = book['genero_id']    
    modified = False
    for key in request.form.keys():
        if (request.form.get(key) != ''):
            modified = True
            break    
    if request.form['completo']=="True":    
            if Book.find_by_isbn(isbn) is None:
                Book.mark_complete(isbn)
                merger(book_data['titulo'])
    Book.updateMeta(book_data, isbn, autor_id, Editorial_id, Genero_id)
    if modified:
        flash("Datos modificados correctamente")
    else: 
        flash("No se Ingresó ningún dato, no se modifcó el metadato")
    
    return redirect(url_for("book_menu"))
    


def remove_meta(isbn):
    set_db()
    Book.deleteMeta(isbn)
    return redirect(url_for("book_menu"))

def date_menu(isbn):
    set_db()
    capitulos = Book.allChapter(isbn)
    libro = Book.find_by_isbn(isbn)
    print(capitulos)
    print(libro)
    return render_template('books/modificar_menu.html', isbn=isbn, capitulos=capitulos, libro=libro)

def date_render_book(isbn):
    print("cambiar fecha de todo")
    Book.db = get_db()
    book = Book.find_by_isbn(isbn)
    if book is not None:
        available_from = book['available_from'].strftime("%Y-%m-%d")
        available_to = book['available_to'].strftime("%Y-%m-%d") if book['available_to'] is not None else ''
    else:
        available_from = ''
        available_to = ''
    print(available_from)
    print(available_to)
    adm = "configuracion_usarInhabilitado" in session['permisos'] #Permiso que solo tiene un administrador
    return render_template('books/modificar_total.html',adm=adm, isbn=isbn, available_from=available_from, available_to=available_to)

def date_render_chap(isbn, num):
    print("cambiar fecha de capitulo")
    Book.db = get_db()
    book = Book.find_chapter_by_isbn(isbn, num)
    available_from = book['available_from'].strftime("%Y-%m-%d")
    available_to = book['available_to'].strftime("%Y-%m-%d") if book['available_to'] is not None else ''
    
    adm = "configuracion_usarInhabilitado" in session['permisos'] #Permiso que solo tiene un administrador
    return render_template('books/modificar_chap.html', adm=adm, isbn=isbn, num=num,available_from=available_from, available_to=available_to)

def date_book(isbn):
    set_db()
    if (Book.find_by_isbn(isbn) is None):
        Book.updateDate_allChap(isbn, request.form)
    else: 
        Book.updateDate_book(isbn, request.form)
    return redirect(url_for("book_menu"))

def date_chap(isbn, num):
    set_db()
    Book.updateDate_oneChap(isbn, num, request.form)
    return redirect(url_for("book_menu"))
#Muestra de libros



def open_book(isbn): #aca abre el libro guardado
    print("abro")
    set_db()
    historial = Book.get_last_read(session['usuario']) #ACA SERIA session['perfil']
    print(historial)
    titulo = Book.find_meta_by_isbn(isbn)['titulo']
    nombre = titulo+"_Full"
    print(nombre)
    Book.record_open(nombre, session['usuario'], dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) #ACA SERIA session['perfil']
    return render_template('books/abrirlibro.html', titulo=titulo, nombre=nombre)

def open_cap_menu(isbn):
    set_db()
    capitulos = Book.allChapter(isbn)
    today = dt.datetime.now()
    noDisponibles = list(map(lambda cap: cap['available_from'] > today, capitulos))
    vencidos = list(map(lambda cap: ((cap['available_to'] is not None) and cap['available_to'] < today), capitulos))
    titulo = Book.find_meta_by_isbn(isbn)['titulo']
    return render_template('books/abrir_cap_menu.html',isbn=isbn, capitulos=capitulos, noDisponibles=noDisponibles, vencidos=vencidos, titulo=titulo)

def open_cap(isbn, num):
    print("abro capitulo")
    set_db()
    historial = Book.get_last_read(session['usuario']) #ACA SERIA session['perfil']
    titulo = Book.find_meta_by_isbn(isbn)['titulo']
    nombre = titulo+"_cap_"+str(num)
    Book.record_open(nombre, session['usuario'], dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) #ACA SERIA session['perfil']
    return render_template('books/abrirlibro.html', titulo=titulo, nombre=nombre)

def validate_meta_isbn(isbn):
    book = Book.find_meta_by_isbn(isbn)
    return book == None

def validate_book_isbn(isbn):
    book = Book.find_by_isbn(isbn)
    return book == None

def validate_chapter_isbn(isbn, num):
    book = Book.find_chapter_by_isbn(isbn, num)
    return book == None

def validate_date(isbn):
    set_db()
    complete = Book.is_complete(isbn)
    if complete:
        book = Book.find_by_isbn(isbn)
        today = dt.datetime.now()#.strfstrftime("%Y-%m-%d")
        if book is None:
            caps = Book.allChapter(isbn)            
            for cap in caps:
                if cap['available_to'] is not None and today > cap['available_to']:
                    print("Se encontro un capitulo vencido")
                    return False
                if cap['available_from'] is not None and today < cap['available_from']:
                    print("Se encontro un capitulo no disponible")
                    return False
            print("Ningun Capitulo se vencio")
            return True
        else:
            if book['available_to'] is not None and today > book['available_to']:
                print("El libro esta vencido")
                return False
            if book['available_from'] is not None and today < book['available_from']:
                print("El libro aun no esta disponible")
                return False
            else:
                print("El libro no esta vencido")
                return True                                
    else:
        print("Aun no se cargo el libro")
        return False


def set_db():
    Book.db = get_db()
    Autor.db = get_db()
    Editorial.db = get_db()
    Genero.db = get_db()