from os import path
from flaskps.db import get_db
from flask import Flask, render_template, g, redirect, url_for, session
from flaskps.helpers.auth import authenticated
from flaskps.resources import user_resource
from flaskps.resources import auth
from flaskps.resources import configuracion
from flaskps.resources import book
from flaskps.resources import autor
from flaskps.resources import editorial
from flaskps.resources import genero
from flaskps.resources import novedad
from flaskps.resources import trailer
from flaskps.resources import perfil

from flaskps.models.configuracion import Configuracion
from flaskps.config import Config
from flaskps.resources.api import calls


# Configuración inicial de la app
app = Flask(__name__)
app.config.from_object(Config)

# Autenticación
app.add_url_rule("/iniciar_sesion", 'auth_login', auth.login)
app.add_url_rule("/cerrar_sesion", 'auth_logout', auth.logout)
app.add_url_rule(
    "/autenticacion",
    'auth_authenticate',
    auth.authenticate,
    methods=['POST']
)



#Configuracion
app.add_url_rule("/configuracion", 'configuracion_config', configuracion.config)
app.add_url_rule("/configuration/toggle", 'configuracion_toggleActive', configuracion.toggleActive)
app.add_url_rule("/configuration/edit", 'configuracion_edit', configuracion.editarInformacion, methods=['POST'])
app.add_url_rule("/configuration/edit", 'configuracion_render_edit', configuracion.renderEditarInformacion)
app.add_url_rule("/config", 'configuracion_changePage', configuracion.changePage, methods=['POST'])
# Usuarios

#Metodos para mostrar tablas de usuarios
app.add_url_rule("/usuarios", 'user_resource_index', user_resource.index)
app.add_url_rule("/usuarios/search_by_username", 'user_resource_indexUser', user_resource.indexUser, methods=['POST'])
app.add_url_rule("/usuarios/index_by_active", 'user_resource_indexActive', user_resource.indexActive)
app.add_url_rule("/usuarios/index_by_inactive", 'user_resource_indexInactive', user_resource.indexInactive)
#CRUD de usuarios
app.add_url_rule("/usuarios", 'user_resource_create', user_resource.create, methods=['POST']) #realiza creacion en el modelo
app.add_url_rule("/usuario/new", 'user_resource_new', user_resource.new) #levanta vista de creacion
app.add_url_rule("/usuarios/editar/<int:id>", 'user_resource_edit', user_resource.edit)#levanta vista de edicion
app.add_url_rule("/editar/<int:id>", 'user_resource_execute_edit', user_resource.executeEdit, methods=['POST']) #crea edicion en el modelo
app.add_url_rule("/usuarios/mostrar/<int:id>", 'user_resource_show', user_resource.show) #mostrar datos de usuario
app.add_url_rule("/usuarios/delete/<int:id>", 'user_resource_delete', user_resource.delete)#Baja logica
app.add_url_rule("/usuarios/active/<int:id>", 'user_resource_active', user_resource.active)#activacion de baja logica

#Asignacion de roles
app.add_url_rule("/usuarios/asignar", 'user_resource_indexAssign', user_resource.indexAssign) #listar usuarios y roles
app.add_url_rule("/usuarios/asignar/<string:user>/<string:rol>", 'user_resource_asignarRol', user_resource.assign) #asignar un rol
app.add_url_rule("/usuarios/eliminarRol/<string:user>/<string:rol>", 'user_resource_deleteRol', user_resource.deleteRol) #desasignar un rol

#CRUD de libros
app.add_url_rule("/libros/new/<string:isbn>", 'book_new', book.new)
app.add_url_rule("/libros/<string:isbn>", 'book_create', book.create, methods=['POST'])
app.add_url_rule("/librosnew_chapter/<string:isbn>", 'book_new_chapter', book.new_chapter)
app.add_url_rule("/librosnew_chapter/<string:isbn>", 'book_create_chapter', book.create_chapter, methods=['POST'])
app.add_url_rule("/librosEliminar/<string:isbn>", 'book_delete', book.delete)
app.add_url_rule("/librosdel_chap_menu/<string:isbn>", 'book_delete_menu', book.render_delete_menu)
app.add_url_rule("/librosdel_chap/<string:isbn>/<int:num>", 'book_delete_chap', book.delete_chapter)
#Gestion de fechas
app.add_url_rule("/librosfecha/<string:isbn>", 'book_date_menu', book.date_menu)
app.add_url_rule("/librosfechabook/<string:isbn>", 'book_date_book', book.date_render_book)
app.add_url_rule("/librosfechabook/<string:isbn>/<int:num>", 'book_date_chap', book.date_render_chap)
app.add_url_rule("/librosfechabook/<string:isbn>", 'book_date_mod_book', book.date_book, methods=['POST'])
app.add_url_rule("/librosfechabook/<string:isbn>/<int:num>", 'book_date_mod_chap', book.date_chap, methods=['POST'])
#Metadatos
app.add_url_rule("/libros/meta", 'book_meta', book.render_meta)
app.add_url_rule("/libros/meta", 'book_load_meta', book.load_meta, methods=['POST'])
app.add_url_rule("/libros/editar_meta/<string:isbn>", "book_meta_edit", book.edit_meta)
app.add_url_rule("/libros/editar_meta/<string:isbn>", "book_load_meta_edit", book.load_edit_meta, methods=['POST'])
app.add_url_rule("/libros/eliminar/<string:isbn>", "book_meta_remove", book.remove_meta)
#Manejo de libros
app.add_url_rule("/libros", 'book_menu', book.render_menu, methods=['POST', 'GET'])
app.add_url_rule("/librosHistorial", 'book_historial', book.render_historial)
app.add_url_rule("/libros_busqueda", 'book_search', book.search, methods=['POST'])
app.add_url_rule("/librosver/<string:isbn>", 'book_open', book.open_book)
app.add_url_rule("/librosver_cap/<string:isbn>", 'book_cap_menu', book.open_cap_menu)
app.add_url_rule("/librosver_cap_abrir/<string:isbn>/<int:num>", 'book_open_cap', book.open_cap)
app.add_url_rule("/librosver_any/<string:isbn>/<string:name>", 'book_open_any', book.open_any)
#CRUD autor
app.add_url_rule("/autor/new", 'author_new', autor.new)
app.add_url_rule("/autor/create", "author_create", autor.create,methods=['POST'])
#CRUD editorial
app.add_url_rule("/editorial/new", 'editorial_new', editorial.new)
app.add_url_rule("/editorial/create", "editorial_create", editorial.create,methods=['POST'])
#CRUD genero
app.add_url_rule("/genero/new", 'genero_new', genero.new)
app.add_url_rule("/genero/create", "genero_create", genero.create,methods=['POST'])


#CRUD novedades
app.add_url_rule("/novedades/new", "novedad_new", novedad.new)
app.add_url_rule("/novedades/list", "novedad_list", novedad.list)
app.add_url_rule("/novedades/create", "novedad_create", novedad.create,methods=['POST'])
app.add_url_rule("/novedades", "novedad_index", novedad.index)
app.add_url_rule("/novedades/edit/<int:id>", "novedad_renderEdit", novedad.renderEdit_novedad)
app.add_url_rule("/novedades/edit/<int:id>", "novedad_edit", novedad.edit_novedad, methods=['POST'])
app.add_url_rule("/novedades/remove/<int:id>", "novedad_remove", novedad.remove_novedad)

#CRUD trailers
app.add_url_rule("/trailers", 'trailer_menu', trailer.render_menu)
app.add_url_rule("/trailers/new", 'trailer_new', trailer.new)
app.add_url_rule("/trailers/remove/<int:id>", "trailer_remove", trailer.remove_trailer)
app.add_url_rule("/trailers/edit_trailer/<int:id>", "trailer_edit", trailer.edit_trailer)
app.add_url_rule("/trailers/edit_trailer/<int:id>", "trailer_load_edit", trailer.load_edit, methods=['POST'])
app.add_url_rule("/trailer/create", 'trailer_create', trailer.render_trailer)
app.add_url_rule("/trailer/create", 'trailer_load', trailer.load_trailer, methods=['POST'])

#CRUD perfiles
app.add_url_rule("/perfiles/new", "perfil_new", perfil.new)
app.add_url_rule("/perfiles/create", "perfil_create", perfil.create,methods=['POST'])
app.add_url_rule("/perfilesdelete/<int:id>", "perfil_delete", perfil.delete)
app.add_url_rule("/perfiles", "perfil_menu", perfil.render_menu)
app.add_url_rule("/perfiles/<int:id>", "perfil_select", perfil.select)
#Cambio de Plan
app.add_url_rule("/perfilesTopremium", "perfil_to_premium", perfil.to_premium)
app.add_url_rule("/perfilesTobasic", "perfil_to_basic", perfil.to_basic)


@app.route("/")
def hello():
    Configuracion.db = get_db
    info = Configuracion.get_information()
    if(info.get('habilitado')):
        if not authenticated(session):
            return render_template('home.html', titulo=info.get('titulo'), descripcion=info.get('descripcion'), mail = info.get('mail_orquesta'))
        else:
            return redirect(url_for("book_menu"))
    else:
        return render_template('home_inactive.html') 
     
