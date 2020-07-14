from flaskps.models.autor import Autor
from flaskps.models.editorial import Editorial
from flaskps.models.genero import Genero
from flaskps.models.comentario import Comentario
from flaskps.models.user_model import Usuario
class Book(object):
    db = None

    @classmethod
    def marcarFavorito(cls,isbn, userID, perfil_id):
        sql = 'INSERT INTO favoritos(isbn,usuario_id, perfil_id) VALUES (%s,%s, %s)'
        data = (isbn, userID, perfil_id)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        cls.db.commit()
        return True

    @classmethod
    def esFavorito(cls,isbn, userID):
        sql = 'SELECT * FROM favoritos WHERE isbn = %s AND perfil_id= %s'
        data = (isbn, userID)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        row = cursor.fetchone()
        if row == None:
            return False
        else:
            return True

    @classmethod
    def deleteFavoritoByISBN(cls,isbn):
        sql = "DELETE FROM favoritos WHERE isbn = %s"
        data = (isbn)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True


    @classmethod
    def getFavoritoMeta(cls,isbn):
        sql = 'SELECT * FROM metadato WHERE isbn = %s'
        data = (isbn)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        return cursor.fetchall
        
    @classmethod
    def deleteFavorito(cls, isbn, userID):
        sql = "DELETE FROM favoritos WHERE isbn = %s AND perfil_id= %s"
        data = (isbn,userID)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def getFavoritos(cls,userID):
        sql = "SELECT * FROM favoritos WHERE perfil_id=%s"
        data = (userID)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        return cursor.fetchall()

    @classmethod
    def existeTrailer(cls,isbn):
        sql = "SELECT * FROM trailer WHERE isbn = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))        
        return cursor.fetchall()

    @classmethod
    def getTrailers(cls):
        sql = 'SELECT * FROM trailer'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def allUsers(cls):
        sql = 'SELECT * FROM usuario;'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    @classmethod
    def getByISBN(cls,isbn):
        sql = 'SELECT * FROM comentarios WHERE isbn = %s'
        data = (isbn)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        return cursor.fetchall()


    @classmethod     
    def getComentarios(cls):
        sql = 'SELECT * FROM comentarios'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()  



    @classmethod
    def comment_book(cls,comment,isbn,calificacion,today,user_id, perfil_id):
        sql = "INSERT INTO comentarios(comentario,isbn,calificacion,fecha,usuario_id, perfil_id) VALUES (%s,%s,%s,%s,%s)"
        data = (comment,isbn,calificacion,today,user_id, perfil_id)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        cls.db.commit()
        return True


    @classmethod
    def setPuntuacion(cls,isbn,calificacion,today,user_id, perfil_id):
        sql = "INSERT INTO comentarios(isbn,calificacion,fecha,usuario_id, perfil_id) VALUES (%s,%s,%s,%s)"
        data = (isbn,calificacion,today,user_id, perfil_id)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        cls.db.commit()
        return True



    @classmethod
    def deleteComment(cls, idComment):
        sql = "DELETE FROM comentarios WHERE id = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, idComment)
        cls.db.commit()
        return True

    @classmethod
    def deleteCommentByISBN(cls, isbn):
        sql = "DELETE FROM comentarios WHERE isbn = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, isbn)
        cls.db.commit()
        return True



    @classmethod
    def isSpoiler(cls,idComment):
        sql = 'UPDATE comentarios SET spoiler = 1 WHERE id = %s'
        data = (idComment)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        cls.db.commit()
        return True



    @classmethod
    def create(cls, data, filename,isbn):
        sql = ' INSERT INTO libro (isbn, archivo, available_from, available_to) VALUES (%s, %s, %s,%s)'
        data = (isbn,filename,data.get('available_from'),data.get('available_to') if data.get('available_to')!='' else None)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def delete(cls, isbn):
        sql = "DELETE FROM libro WHERE isbn = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, isbn)
        cls.db.commit()
        return True

    
    @classmethod
    def create_chapter(cls, data, filename,isbn):
        sql = ' INSERT INTO capitulo (num, isbn, archivo, available_from, available_to) VALUES (%s, %s, %s, %s,%s)'
        data = (data.get('num'), isbn,filename,data.get('available_from'),data.get('available_to') if data.get('available_to')!='' else None)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def delete_chapter(cls, isbn,num):
        sql = "DELETE FROM capitulo WHERE isbn = %s and num = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn, num))
        cls.db.commit()
        return True

    @classmethod
    def delete_all_chapter(cls, isbn):
        sql = "DELETE FROM capitulo WHERE isbn = %s "
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))
        cls.db.commit()
        return True

    @classmethod
    def loadMeta(cls, data,id_autor, id_editorial, id_genero):
        sql = 'INSERT INTO metadato (isbn, titulo, autor_id, sinopsis, editorial_id, genero_id) VALUES (%s, %s, %s, %s,%s, %s)'
        data = (data.get('isbn'), data.get('titulo'), id_autor, data.get('sinopsis'), id_editorial, id_genero)
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
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
    def deleteMeta(cls, isbn):
        sql = "DELETE FROM metadato WHERE isbn = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, isbn)
        cls.db.commit()
        return True

    @classmethod
    def updateDate_allChap(cls, isbn, data):
        sql = "UPDATE capitulo SET available_from = %s, available_to = %s WHERE isbn = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, (data.get('available_from') ,data.get('available_to') if data.get('available_to')!='' else None, isbn) ) 
        cls.db.commit()
        return True

    @classmethod
    def updateDate_oneChap(cls, isbn, num, data):
        sql = "UPDATE capitulo SET available_from = %s, available_to = %s WHERE isbn = %s and num=%s"
        cursor = cls.db.cursor()

        cursor.execute(sql, (data.get('available_from') ,data.get('available_to') if data.get('available_to')!='' else None, isbn, num) ) 
        cls.db.commit()
        return True

    @classmethod
    def updateDate_book(cls, isbn, data):
        sql = "UPDATE libro SET available_from = %s, available_to = %s WHERE isbn = %s"
        cursor = cls.db.cursor()        
        cursor.execute(sql, (data.get('available_from'), data.get('available_to') if data.get('available_to')!='' else None, isbn) ) 
        cls.db.commit()
        return True

    @classmethod
    def record_open(cls, filename, perfil, date, isbn, titulo):
        sql = "INSERT INTO historial (isbn, titulo,archivo, perfil_id, fecha_ultima) values (%s, %s,%s, %s, %s) ON DUPLICATE KEY UPDATE isbn=%s, titulo=%s, archivo=%s, perfil_id=%s, fecha_ultima=%s"
        data = (isbn, titulo,filename, perfil, date, isbn, titulo,filename, perfil, date)        
        cursor = cls.db.cursor()
        cursor.execute(sql, data)
        cls.db.commit()
        return True

    @classmethod
    def delete_records(cls, isbn):
        sql = "DELETE FROM historial WHERE isbn = %s"
        cursor = cls.db.cursor()
        cursor.execute(sql, isbn)
        cls.db.commit()
        return True
    
    #GETS
    @classmethod
    def get_last_read(cls, perfil):
        sql = "SELECT * FROM historial WHERE perfil_id=%s"
        cursor = cls.db.cursor()
        cursor.execute(sql, (perfil))
        books = cursor.fetchall()
        if books != ():
            books.sort(key=lambda b: b['fecha_ultima'], reverse=True)# if books != () else None
        return books

    @classmethod     
    def allMeta(cls):
        sql = 'SELECT * FROM metadato'
        cursor = cls.db.cursor()
        cursor.execute(sql)
        metas = cursor.fetchall()
        for meta in metas:
            meta['autor_id'] = Autor.find_by_id(meta['autor_id'])['nombre']
            meta['editorial_id'] = Editorial.find_by_id(meta['editorial_id'])['nombre']
            meta['genero_id'] = Genero.find_by_id(meta['genero_id'])['nombre']
        return metas

    @classmethod     
    def allChapter(cls, isbn):
        sql = 'SELECT * FROM capitulo WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))        
        return cursor.fetchall()


    @classmethod
    def find_by_isbn(cls, isbn):
        sql = 'SELECT * FROM libro WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))
        return cursor.fetchone()

    @classmethod
    def find_meta_by_isbn(cls, isbn):
        sql = 'SELECT * FROM metadato WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))
        return cursor.fetchone()

    @classmethod
    def find_chapter_by_isbn(cls, isbn, num):
        sql = 'SELECT * FROM capitulo WHERE isbn = %s and num = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn, num))
        return cursor.fetchone()

    @classmethod
    def mark_complete(cls, isbn):
        sql = 'UPDATE metadato SET completo = %s WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, ('1',isbn))
        cls.db.commit()
        return True

    @classmethod
    def mark_incomplete(cls, isbn):
        sql = 'UPDATE metadato SET completo = %s WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, ('0',isbn))
        cls.db.commit()
        return True

    @classmethod
    def is_complete(cls, isbn):
        sql = 'SELECT completo FROM metadato WHERE isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (isbn))
        status = cursor.fetchone()['completo']
        print(status)
        return status==1

    @classmethod     
    def allFavorites(cls, id, isbn):
        sql = 'SELECT * FROM favorito WHERE perfil_id = %s and isbn = %s'
        cursor = cls.db.cursor()
        cursor.execute(sql, (id))  
        favs = cursor.fetchall()   
        for fav in favs:
            fav['autor_id'] = Autor.find_by_id(meta['autor_id'])['nombre']
        return favs
