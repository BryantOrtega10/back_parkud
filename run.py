from flask import Flask
from config.configuration import ProductionConfig, DevelopmentConfig
from app.controllers.usuario_controller import usuario_bp
from flask_cors import CORS


app = Flask(__name__)

# Configuración de la base de datos
app.config.from_object(DevelopmentConfig())

CORS(app, resources={r"/*": {"origins": "*"}})

# Registro de los controladores
app.register_blueprint(usuario_bp, url_prefix='/usuario')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)