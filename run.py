from flask import Flask
from config.configuration import ProductionConfig, DevelopmentConfig
from app.controllers.usuario_controller import usuario_bp
from app.controllers.sede_controller import sede_bp
from app.controllers.reserva_controller import reserva_bp
from app.controllers.reportes_controller import reportes_bp, estadisticas_bp
from flask_cors import CORS


app = Flask(__name__)

# Configuración de la base de datos
app.config.from_object(DevelopmentConfig())

CORS(app, resources={r"/*": {"origins": "*"}})

# Registro de los controladores
app.register_blueprint(usuario_bp, url_prefix='/usuario')
app.register_blueprint(sede_bp, url_prefix='/sede')
app.register_blueprint(reserva_bp, url_prefix='/reserva')
app.register_blueprint(reportes_bp, url_prefix='/reportes')
app.register_blueprint(estadisticas_bp, url_prefix='/estadisticas')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)