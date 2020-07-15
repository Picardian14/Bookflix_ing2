class Novedad(object):
    db = None
    @classmethod
    def create(cls, data):
        sql = ' INSERT INTO novedad (titulo, descripcion, created_at) VALUES (%s, %s, %s)'
        data = (data.get('titulo'), data.get('descripcion'), data.get('created_at'))
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True
    
    @classmethod
    def deleteNovedad(cls, id):
        sql = "DELETE FROM novedad WHERE id = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, id)
        cls.db.commit()
        return True

    @classmethod
    def updateMeta(cls, data, isbn, autor_id, editorial_id, genero_id):
        sql = 'UPDATE metadato SET titulo = %s, autor_id = %s, sinopsis = %s, editorial_id = %s, genero_id = %s WHERE isbn = %s '
        data = (data.get('titulo'), autor_id, data.get('sinopsis'), editorial_id, genero_id, isbn)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def editDetalle(cls, desc, id):
        sql = "UPDATE novedad SET descripcion = %s WHERE id= %s"
        data = (desc,id)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        cls.db.commit()
        return True


    @classmethod
    def editTitulo(cls,titulo,id):
        sql = "UPDATE novedad SET titulo = %s WHERE id= %s"
        data = (titulo,id)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        cls.db.commit()
        return True



    #GETS
    @classmethod
    def all(cls):
        sql = 'SELECT * FROM novedad;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


    @classmethod
    def find_novedad_by_id(cls, id):
        sql = 'SELECT * FROM novedad WHERE id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, id)