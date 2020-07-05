import datetime
class Usuario(object):

    db = None
    #paginado = 5
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM usuario;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def create(cls, data):
        sql = ' INSERT INTO usuario (email,username, dni,password, activo,updated_at, created_at,first_name, last_name, subscription,numero_tarjeta,codigo,fecha) VALUES (%s, %s,%s, %s,%s, %s, %s, %s,%s, %s, %s,%s, %s)'
        data = (data.get('email'),data.get('username'),data.get('dni'),data.get('password'),1, datetime.datetime.now(),datetime.datetime.now(),data.get('first_name'),data.get('last_name'), "basic", data.get('numero_tarjeta'), data.get('codigo'), data.get('fecha')+"-01")
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def find_by_email_and_pass(cls, email, password):
        sql = """
            SELECT * FROM usuario AS u
            WHERE u.email = %s AND u.password = %s
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (email, password))

        return cursor.fetchone()

    @classmethod
    def find_by_email(cls, email):
        sql = """
            SELECT * FROM usuario AS u
            WHERE u.email = %s 
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (email))
        return cursor.fetchone()
        
    @classmethod
    def find_by_username(cls, username):
        cursor = cls.db.cursor()
        cursor.execute("SELECT * FROM usuario AS u WHERE u.username LIKE '%s%%'" % username)
        usu = cursor.fetchall()
        return usu
    @classmethod
    def find_by_id(cls, id):
        cursor = cls.db.cursor()
        dada = cursor.execute("SELECT * FROM usuario AS u WHERE u.id =%s ", str(id))
        return cursor.fetchone()

    @classmethod
    def  find_by_active(cls):
        cursor = cls.db.cursor()
        data = cursor.execute("SELECT * FROM usuario AS u WHERE u.activo = 1")
        return cursor.fetchall()

    @classmethod
    def  find_by_inactive(cls):
        cursor = cls.db.cursor()
        data = cursor.execute("SELECT * FROM usuario AS u WHERE u.activo = 0")
        return cursor.fetchall()

    @classmethod
    def get_id_by_username(cls, username):
        cursor = cls.db.cursor()
        cursor.execute("SELECT * FROM usuario AS u WHERE u.username LIKE '%s%%'" % username)
        user = cursor.fetchone()
        return user['id']

    @classmethod
    def get_username_by_id(cls, id):
        cursor = cls.db.cursor()
        cursor.execute("SELECT username FROM usuario AS u WHERE u.id = %s" % id)
        user = cursor.fetchone()
        return user
    @classmethod
    def change_rol(cls, user, rol):
        sql = "INSERT INTO usuario_tiene_rol (rol_id, usuario_id) VALUES (%s, %s) "
        cursor = cls.db.cursor()
        cursor.execute(sql, (rol, user))
        cls.db.commit()
        return True

    @classmethod
    def delete_rol(cls, user, rol):
        sql = "DELETE FROM usuario_tiene_rol WHERE rol_id = %s AND usuario_id = %s "
        cursor = cls.db.cursor()
        cursor.execute(sql, (rol, user))
        cls.db.commit()
        return True
    @classmethod
    def get_rol(cls, user):
        sql = "SELECT rol_id FROM usuario_tiene_rol WHERE usuario_id = %s "
        cursor = cls.db.cursor()
        cursor.execute(sql, user)
        r_id = cursor.fetchone()
        return r_id

    @classmethod
    def delete(cls, id):
        sql = ' DELETE FROM usuario where id = %s'
        cursor = cls.db.cursor()        
        cursor.execute(sql, (id))
        cls.db.commit()
        return True

    @classmethod
    def update(cls,data, id):
        sql = 'UPDATE usuario SET email = %s, username = %s, updated_at = %s, first_name = %s, last_name = %s, subscription = %s, numero_tarjeta = %s, codigo = %s, fecha = %s WHERE id = %s;'
        cursor = cls.db.cursor()
        data = (data.get('email'),data.get('username'), datetime.datetime.now(),data.get('first_name'),data.get('last_name'),data.get('subscription'), data.get('numero_tarjeta'),data.get('codigo'),data.get('fecha')+"-01", str(id))
        cursor.execute(sql, data)
        cls.db.commit()
        return True
    
    @classmethod
    def active (cls, id):
        sql = ' UPDATE usuario SET activo = 1, updated_at = %s where id = %s'
        cursor = cls.db.cursor()
        data = (datetime.datetime.now(), str(id))
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def toPremium(cls, id):
        sql = 'UPDATE usuario SET subscription = %s WHERE id = %s'
        cursor = cls.db.cursor()        
        cursor.execute(sql, ("premium", id))
        cls.db.commit()
        return True

    @classmethod
    def toBasic(cls, id):
        sql = 'UPDATE usuario SET subscription = %s WHERE id = %s'
        cursor = cls.db.cursor()        
        cursor.execute(sql, ("basic", id))
        cls.db.commit()
        return True

        

    