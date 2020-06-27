from flask import redirect, render_template, request, url_for, abort, session, flash
from flaskps.db import get_db
from flaskps.models.user_model import Usuario
from flaskps.models.configuracion import Configuracion
from flaskps.models.permits import Permit

def login():
    Configuracion.db = get_db
    info = Configuracion.get_information()
    if (info.get('habilitado')):
        return render_template('auth/login.html', inhabilitado=False)
    else:
        return render_template('auth/login.html', inhabilitado=True)

def authenticate():
    params = request.form
    set_usuario_db()
    usuario = Usuario.find_by_email_and_pass(params['email'], params['password'])

    if not usuario:
        flash("Usuario o clave incorrecto.")
        return redirect(url_for('auth_login'))
    if usuario['activo'] == 0:
        flash("Usuario inhabilitado")
        return redirect(url_for('auth_login'))
    session['usuario'] = usuario['email']
    session['usuario_id'] = usuario['id']
    session['permisos'] = getCurrentPermits()
    Configuracion.db = get_db
    info = Configuracion.get_information()
    if (info.get('habilitado') == 0) and ('configuracion_usarInhabilitado' not in session['permisos']):
        flash("Sitio temporalmente inhabilitado")
        del session['usuario']
        del session['permisos']
    flash("La sesión se inició correctamente.")
    return redirect(url_for('book_menu', type='all'))


def logout():
    del session['usuario']
    del session['permisos']
    flash("La sesión se cerró correctamente.")
    return redirect(url_for('auth_login'))

def getCurrentPermits():
    usuario = Usuario.find_by_email(session['usuario'])
    set_permit_db()
    return Permit.get_permits(usuario)

def hasPermit(permit):
    return permit in session['permisos']

def set_usuario_db():
    Usuario.db = get_db()
def set_permit_db():
    Permit.db = get_db()
