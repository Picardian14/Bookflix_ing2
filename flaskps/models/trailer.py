from flaskps.models.autor import Autor
from flaskps.models.editorial import Editorial
from flaskps.models.genero import Genero


class Trailer(object):
    db = None

    @classmethod
    def setTrailer(cls,data,archivo):
    	sql = 'INSERT INTO trailer (titulo, archivo) VALUES (%s,%s)'
    	data = (data.get('titulo'),archivo)
    	cursor = cls.db.cursor()
    	cursor.execute(sql, data)
    	cls.db.commit()
    	return True


    @classmethod
    def setTrailerAsociado(cls,data,archivo,isbn):
        sql = 'INSERT INTO trailer (titulo, archivo, isbn) VALUES (%s,%s,%s)'
        data = (data.get('titulo'),archivo,isbn)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True


    @classmethod
    def allMeta(cls):
        sql = 'SELECT * FROM metadato;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


    @classmethod
    def getTrailerByID(cls,idTrailer):
        sql = 'SELECT * FROM trailer WHERE ID = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idTrailer))
        return cursor.fetchall()

    @classmethod
    def tituloById(cls,idTrailer):
        sql = 'SELECT titulo FROM trailer WHERE ID = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idTrailer))        
        return cursor.fetchone()

    @classmethod
    def filenameById(cls,idTrailer):
        sql = 'SELECT archivo FROM trailer WHERE ID = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (idTrailer))        
        return cursor.fetchone()



    @classmethod
    def tituloByIsbn(cls,isbn):
        sql = 'SELECT titulo FROM trailer WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))        
        return cursor.fetchone()

    @classmethod
    def filenameByIsbn(cls,isbn):
        sql = 'SELECT archivo FROM trailer WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))        
        return cursor.fetchone()


    @classmethod
    def updateFilename(cls,archivo,idTrailer):
        sql = 'UPDATE trailer SET archivo = %s WHERE ID = %s'
        data = (archivo,idTrailer)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True


    @classmethod
    def updateTitle(cls,idTrailer,titulo):
        sql = 'UPDATE trailer SET titulo = %s WHERE ID = %s'
        data = (titulo,idTrailer)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True



    @classmethod
    def deleteTrailer(cls,idTrailer):
        sql = "DELETE FROM trailer WHERE ID = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, idTrailer)
        cls.db.commit()
        return True


    @classmethod
    def existe(cls,isbn):
        sql = "SELECT * FROM trailer WHERE isbn = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))        
        return cursor.fetchall()

    @classmethod
    def getByISBN(cls,isbn):
        sql = 'SELECT * FROM trailer WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))
        return cursor.fetchall()
