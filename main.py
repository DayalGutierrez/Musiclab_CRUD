from flask import Flask, json, jsonify, request
from conexion import create_usuario, create_artist, create_album, add_track, create_comentario
from conexion import get_albums, get_tracks, get_artists, get_artist, get_caratula, get_comentarios
from conexion import delete_album, modify_album

app = Flask(__name__)

@app.route("/music/api/v1/usuarios", methods=["POST"])
def usuario (id=None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()

            if create_usuario(data['nombre'], data['correo'], data['contrasenia']):
                return jsonify(code = 'ok')
            else:
                return jsonify(code = 'Ya existe')
        except:
            return jsonify(code='error')

@app.route("/music/api/v1/artistas", methods=["POST", "GET"])
@app.route("/music/api/v1/artistas/<int:id>", methods=["GET"])
def artistas(id=None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            if create_artist(data["nombre"],data["biografia"], data['foto']):
                return jsonify(code = 'ok')
            else:
                return jsonify(coode = 'Ya existe')
        except:
            return jsonify(code = 'error')
    elif request.method == "GET" and id is None:
        return jsonify(get_artists())
    elif request.method == "GET" and id is not None:
        return jsonify(get_artist(id))

@app.route("/music/api/v1/album/<int:id>", methods=["GET"])
def caratula(id):
    if request.method == "GET":
        return jsonify(get_caratula(id))

@app.route("/music/api/v1/albumes", methods=["POST", "GET"])
@app.route("/music/api/v1/albumes/<int:id>", methods=["GET","DELETE", "PATCH"])
def albumes(id = None):
    if request.method == "POST" and request.is_json and id is None:
        try:
            data = request.get_json()
            if create_album(data["titulo"],data["anio_produccion"],\
                data["caratula"], data["puntuacion"], data["usuarioId"],\
                data["artistaId"]):

                return jsonify(code = 'ok')
            else:
                return jsonify(coode = 'Ya existe')
        except:
            return jsonify(code = 'error')

    elif request.method == "GET" and id is None:
        return jsonify(get_albums())

    elif request.method == "GET" and id is not None:
        return jsonify(get_tracks(id))

    elif request.method == "DELETE" and id is not None:
        if delete_album(id):
            return jsonify(code = "ok")
        else:
            return jsonify(code = "error")

    elif request.method == "PATCH" and request.is_json and id is not None:
        data = request.get_json()

        if modify_album(id, data["caratula"]):
            return jsonify(code = "ok")
        else:
            return jsonify(code = "error")

@app.route("/music/api/v1/tracks", methods=["POST"])
def tracks():
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            if add_track(data["titulo"],data["duracion"],data["albumId"]):
                return jsonify(code = "ok")
            else:
                return jsonify(code = "Ya existe")
        except:
            return jsonify(code = "error")

@app.route("/music/api/v1/comentarios", methods=["POST"])
@app.route("/music/api/v1/comentarios/<int:id>", methods=["GET"])
def comentarios(id=None):
    if request.method == "POST" and id is None:
        try:
            data = request.get_json()
            if create_comentario(data["texto"],data["fecha_realizado"],\
                data["albumId"], data["usuarioId"]):

                return jsonify(code = 'ok')
            else:
                return jsonify(coode = 'Ya existe')
        except:
            return jsonify(code = 'error')
    elif request.method == "GET" and id is not None:
        return jsonify(get_comentarios(id))

app.run(debug=True)