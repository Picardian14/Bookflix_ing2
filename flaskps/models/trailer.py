class Trailer(object):
    db = None
    @classmethod
    def setTrailer(cls,data, titulo):
        sql = ' INSERT INTO trailer (titulo, archivo) VALUES (%s, %s)'
        data = (titulo, data.get('archivo'))
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        cls.db.commit()
        return True


    @classmethod
    def create(cls,data,filename):
        sql = ' INSERT INTO trailer (titulo,archivo) VALUES(%s,%s)'
        data = (data.get('titulo'),filename)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        cls.db.commit()
        return True    


    @classmethod
    def updateTrailer(cls,tituloNue,id):
        sql = 'UPDATE trailer SET titulo = %s WHERE id = %s'
        data = (tituloNue, id)
        cursor = cls.db.cursor()    
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def deleteTrailer(cls,id):
    	sql = "DELETE FROM trailer where id = %s"
    	cursor = cls.db.cursor()
    	cursor.execute(sql,id)
    	cls.db.commit()
    	return True

    @classmethod
    def getTrailers(cls):
    	sql = 'SELECT * from trailer'
    	cursor = cls.db.cursor()
    	cursor.execute(sql)
    	return cursor.fetchall()


    @classmethod
    def getTrailerByID(cls,id):
        sql = 'SELECT * FROM trailer WHERE id = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, id)
        return cursor.fetchone()
