import jwt
from functools import wraps
from http import HTTPStatus
from flask import jsonify, request, current_app

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

