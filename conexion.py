import mysql.connector

bd = mysql.connector.connect(user='dayal', 
    password='123456789', database='Musiclab')

cursor = bd.cursor()

def user_exists(correo):
    query = "SELECT COUNT(*) FROM usuario WHERE correo = %s"
    cursor.execute(query,(correo,) )

    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False
import hashlib
def create_usuario(nombre,correo, contra):
    if user_exists(correo):
        return False
    else:
        h = hashlib.new('sha256', bytes(contra, 'utf-8'))
        h = h.hexdigest()
        insert = "INSERT INTO usuario(nombre, correo, contrasenia) VALUES(%s, %s, %s)"
        cursor.execute(insert, (nombre, correo, h))
        bd.commit()
        return True

def artist_exists(nombre):
    query = "SELECT COUNT(*) FROM artista WHERE nombre = %s"
    cursor.execute(query,(nombre,) )

    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False
def create_artist(nombre,bio,foto):
    if artist_exists(nombre):
        return False
    else:
        insert = "INSERT INTO artista(nombre, biografia, foto) VALUES(%s, %s, %s)"
        cursor.execute(insert, (nombre, bio, foto) )
        bd.commit()
        return True

def album_exists(titulo, artistaId):
    query = "SELECT COUNT(*) FROM album WHERE titulo = %s AND artistaId = %s"
    cursor.execute(query,(titulo,artistaId) )
    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False
def create_album(titulo,anio,caratula,puntua,userId,artistId):
    if album_exists(titulo,artistId):
        return False
    else:
        insert = "INSERT INTO album(titulo, anio_produccion, caratula, puntuacion, usuarioId, artistaId)\
        VALUES(%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert, (titulo,anio,caratula,puntua,userId,artistId))
        bd.commit()
        return True

def track_exists(titulo, albumId):
    query = "SELECT COUNT(*) FROM track WHERE titulo = %s AND albumId = %s"
    cursor.execute(query,(titulo,albumId) )
    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False
def add_track(titulo,duracion,albumId):
    if track_exists(titulo,albumId):
        return False
    else:
        insert = "INSERT INTO track(titulo, duracion, albumId) VALUES(%s, %s, %s)"
        cursor.execute(insert, (titulo, duracion, albumId))
        bd.commit()
        return True

def get_albums():
    query = "SELECT album.titulo, album.anio_produccion, album.caratula, album.puntuacion, artista.nombre, album.artistaId, album.id FROM album INNER JOIN artista ON album.artistaId=artista.id"
    cursor.execute(query)
    albums = []
    for row in cursor.fetchall():
        album = {
            "titulo" : row[0],
            "anio_produccion" : row[1],
            "caratula" : row[2],
            "puntuacion" : row[3],
            "artista" : row[4],
            "artistaId" : row[5],
            "id" : row[6]
        }
        albums.append(album)
    return albums

def delete_album(id):
    delete_tracks = "DELETE FROM track WHERE albumId = %s"
    cursor.execute(delete_tracks, (id,) ) 
    #Se eliminan todos los tracks de ese album para que no haya un error por referencias y porque ese album ya no existirá
    delete_tracks = "DELETE FROM comentario WHERE albumId = %s"
    cursor.execute(delete_tracks, (id,) ) 
    #Se eliminan todos los comentarios de ese album para que no haya un error por referencias y porque ese album ya no existirá
    bd.commit()
    delete = "DELETE FROM album WHERE id = %s"
    cursor.execute(delete, (id,) )
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def get_tracks(id):
    query = "SELECT titulo, duracion FROM track WHERE albumId = %s"
    cursor.execute(query, (id,) )
    tracks = []
    for row in cursor.fetchall():
        track = {
            "titulo" : row[0],
            "duracion" : str(row[1]) #Se convierte a string porque el tipo de dato DATE no se puede poner en un json
        }
        tracks.append(track)
    return tracks

def modify_album(id, caratula):
    update = "UPDATE album SET caratula = %s WHERE id = %s"
    cursor.execute(update, (caratula, id))
    bd.commit()
    """
    update = f"UPDATE album SET {columna} = %s WHERE id = %s"
    cursor.execute(update, (valor, id))
    bd.commit()

    Esta implementacion se me hace mejor debido a que se puede modificar cualquier
    dato del album sin embargo lo dejé para que solo se pueda modificar la carátula 
    como se pide
    """
    if cursor.rowcount:
        return True
    else:
        return False

def get_artists():
    query = "SELECT * FROM artista"
    cursor.execute(query)
    artists = []
    for row in cursor.fetchall():
        artist = {
            "id": row[0],
            "nombre": row[1],
            "biografia": row[2],
            "foto": row[3]
        }
        artists.append(artist)
    return artists
def get_artist(id):
    query = "SELECT nombre,biografia,foto FROM artista WHERE id = %s"
    cursor.execute(query, (id,) )
    artists = []
    for row in cursor.fetchall():
        artist = {
            "nombre": row[0],
            "biografia": row[1],
            "foto": row[2]
        }
        artists.append(artist)
    return artists

def get_caratula(id):
    query = "SELECT caratula, id FROM album WHERE id = %s"
    cursor.execute(query, (id,) )
    for row in cursor.fetchall():
        artist = {
            "caratula": row[0],
            "id": row[1]
        }
    return artist

def create_comentario(texto,fecha,albumId,usuarioId):
    insert = "INSERT INTO comentario(texto, fecha_realizado, albumId, usuarioId)\
    VALUES(%s, %s, %s, %s)"
    cursor.execute(insert, (texto, fecha, albumId, usuarioId))
    bd.commit()
    return True

def get_comentarios(id):
    query = "SELECT comentario.texto, comentario.fecha_realizado, usuario.nombre FROM comentario INNER JOIN usuario ON comentario.usuarioId=usuario.id WHERE comentario.albumId = %s "
    cursor.execute(query, (id,) )
    comentarios = []
    for row in cursor.fetchall():
        coment = {
            "texto": row[0],
            "fecha_realizado": row[1],
            "nombre": row[2]
        }
        comentarios.append(coment)
    return comentarios