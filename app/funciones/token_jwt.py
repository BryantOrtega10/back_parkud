import jwt
from functools import wraps
from http import HTTPStatus
from flask import jsonify, request, current_app
from app.models.entidades import Usuario
from app.daos.DAOFactory import DAOFactorySQL

#crear decorador para obtener token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
           return jsonify({'error': 'Token faltante'}), HTTPStatus.UNAUTHORIZED

        try:
           data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'El token ha expirado'}), HTTPStatus.UNAUTHORIZED
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), HTTPStatus.UNAUTHORIZED
        except:
            return jsonify({'error': 'Token inválido'}), HTTPStatus.UNAUTHORIZED

        return f(*args, **kwargs)

    return decorated

def validar_usuario_token():
    token = request.headers.get('Authorization')
    data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], ["HS256"])
    usuario = Usuario(id=data["idUsuario"])
    usuario = DAOFactorySQL.get_usuario_dao().read(usuario)
    if usuario.estado == 'B':
        return jsonify({"success": False, "error" : f"El usuario se encuentra bloqueado comuniquese con el administrado de PARKUD"})
    
    if usuario.cambiarContrasena == 1:
        return jsonify({"success": False, "error" : f"El usuario debe cambiar de contraseña"})
    
    return usuario

def validar_superadmin_token():
    token = request.headers.get('Authorization')
    data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], ["HS256"])
    usuario = Usuario(id=data["idUsuario"])
    usuario = DAOFactorySQL.get_usuario_dao().read(usuario)
    if usuario is None:
        return jsonify({"success": False, "error" : f"Token Vencido"})
    
    if usuario.estado == 'B':
        return jsonify({"success": False, "error" : f"El usuario se encuentra bloqueado comuniquese con el administrado de PARKUD"})
    
    if usuario.rol != 'S':
        return jsonify({"success": False, "error" : f"El usuario no es superadministrador"})
    
    if usuario.cambiarContrasena == 1:
        return jsonify({"success": False, "error" : f"El usuario debe cambiar de contraseña"})
    
    return usuario