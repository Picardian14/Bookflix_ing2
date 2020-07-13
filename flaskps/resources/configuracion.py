from flask import redirect, render_template, request, url_for, session, abort, flash
from flaskps.db import get_db
from flaskps.models.configuracion import Configuracion
from flaskps.models.user_model import Usuario
from flaskps.helpers.auth import authenticated


def config():
    if not authenticated(session):
        flash("Acceso inhabilitado")
        return redirect('/')
    set_db()
    adm = False
    inhabilitado = False
    Configuracion.db = get_db
    info = Configuracion.get_information()
    if not (info.get('habilitado')):
        inhabilitado = True
    if "usuario_index" in session['permisos']: #si tiene permiso para indexar usuario va a poder ir a lal pagina de configuracion
        adm = True
        return render_template('config/config.html', adm=adm, inhabilitado=inhabilitado, title=info.get('titulo'),
                               description=info.get('descripcion'), mail=info.get('mail_orquesta'), permiso_paginado = "configuracion_paginado" in session['permisos'] , permiso_info = "configuracion_info" in session['permisos'] , permiso_habilitar = "configuracion_habilitado" in session['permisos'] )
    else:
        return render_template('user/index.html', adm=adm, inhabilitado=inhabilitado)


def toggleActive():
    set_db()
    if Configuracion.get_current_status() == 0:
        Configuracion.active()
        flash('Sitio Activo')
    else:
        Configuracion.deactive()
        flash('Sitio Inactivo')
    return redirect(url_for('user_resource_index'))     

def changePage(): # cambiar paginacion
    if not authenticated(session):
        abort(401)
    if 'configuracion_paginado' not in session['permisos']:
        flash('¡Sólo el admin puede cambiar la paginación!')
        return redirect(url_for('user_resource_index'))    
    set_db()
    Configuracion.change_page_size(request.form['page'])
    return redirect(url_for('user_resource_index'))    

def renderEditarInformacion(): #levanta la vista para editar informacion
    if not authenticated(session):
        abort(401)    
    return render_template("config/title.html")

def editarInformacion():  #edita la informacion
    if not authenticated(session):
        abort(401)
    if 'configuracion_habilitado' not in session['permisos']:
        flash('¡Sólo el admin puede Cambiar la informacion la pagina!')
        return redirect(url_for('user_resource_index'))
    set_db()
    Configuracion.edit_information(request.form)
    flash('Se cambio la informacion correctamente')
    return redirect(url_for('user_resource_index'))

def set_db():
    Configuracion.db = get_db()

# def renderlistadoUsuarios(): 
#     if not authenticated(session):
#     abort(401) 


#     return render_template('config/listadoUsuarios.html' )

# def renderlistadoVisitas(): 
#     if not authenticated(session):
#     abort(401) 


#     return render_template('config/listadoVisitas.html')



