class Perfil(object):
    db = None
    @classmethod
    def create(cls, nombre, usuario_id):
        sql = ' INSERT INTO perfil (nombre, usuario_id) VALUES (%s, %s)'
        data = (nombre, usuario_id)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def delete(cls, id):
        sql = 'DELETE FROM perfil WHERE id = %s'        
        cursor = cls.db.cursor()
        cursor.execute(sql, id)
        cls.db.commit()
        return True

    #GETS
    @classmethod
    def all_with_id(cls, id):
        sql = 'SELECT * FROM perfil WHERE usuario_id = %s;'
        cursor = cls.db.cursor()
        cursor.execute(sql, (id))
        return cursor.fetchall()

    @classmethod
    def get_id_by_name_id(cls, name, id):
        sql = """
            SELECT id FROM perfil AS u
            WHERE u.nombre = %s and u.usuario_id = %s 
        """

        cursor = cls.db.cursor()
        cursor.execute(sql, (name, id))
        return cursor.fetchone()

