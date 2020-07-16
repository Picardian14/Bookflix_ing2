class Comentario(object):

    db = None


        #COMENTAR LIBRO
    @classmethod
    def comment_book(cls,comment,isbn,calificacion,today,user_id, perfil_id):
        sql = "INSERT INTO comentarios(comentario,isbn,calificacion,fecha,usuario_id,perfil_id) VALUES (%s,%s,%s,%s,%s, %s)"
        data = (comment,isbn,calificacion,today,user_id,perfil_id)
        cursor = cls.db.cursor()
        cursor.execute(sql,data)
        cls.db.commit()
        return True


    @classmethod
    def setPuntuacion(cls,isbn,calificacion,today,user_id,perfil_id):
        sql = "INSERT INTO comentarios(isbn,calificacion,fecha,usuario_id,perfil_id) VALUES (%s,%s,%s,%s,%s)"
        data = (isbn,calificacion,today,user_id,perfil_id)
        cursor = cls.db.cursor()
        cursor.execute(sql,(data))
        cls.db.commit()
        return True

    @classmethod
    def isSpoiler(cls,idComment):
        sql = 'UPDATE comentarios SET spoiler = true WHERE id = %s'
        data = (idComment)
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
