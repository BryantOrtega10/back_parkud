from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from app.funciones.token_jwt import token_required, validar_usuario_token
from app.models.entidades import Reserva, Tipo_Parqueadero, Usuario, Parqueadero, Cliente, Sede
from app.daos.DAOFactory import DAOFactorySQL
import datetime
from email.mime.text import MIMEText
from app.controllers.usuario_controller import validar_correo
import smtplib, ssl

reserva_bp = Blueprint('reserva', __name__)

@token_required
@reserva_bp.route('/<int:id_reserva>', methods=['GET'])
def obtener_reserva(id_reserva):
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    reserva = DAOFactorySQL.get_reserva_dao().get_datos(id_reserva)
    print(reserva)
    if reserva is None:
        return jsonify({"success": False, "error" : "No se encontró una reserva con ese ID"}) , HTTPStatus.BAD_REQUEST

    if reserva[7] == 'F':
        return jsonify({"success": False, "error" : "La reserva ya ha finalizado"}) , HTTPStatus.BAD_REQUEST
    
    if reserva == 'A':
        return jsonify({"success": False, "error" : "La reserva ya esta activa"}) , HTTPStatus.BAD_REQUEST
    

    reserva = {
        "idReserva": reserva[0],
        "horaInicio": reserva[1].strftime("%Y-%m-%d %H:%M"),
        "horaSalida": reserva[2].strftime("%Y-%m-%d %H:%M"),
        "idParqueadero": reserva[3],
        "tipoParqueadero" : reserva[4],
        "nombreCliente" : reserva[5],
        "apellidoCliente" : reserva[6]
    }

    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "reserva" : reserva}) , HTTPStatus.OK


@token_required
@reserva_bp.route('/<int:id_reserva>/entrada', methods=['POST'])
def registrar_entrada(id_reserva):
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    reserva = Reserva(id=id_reserva)
    reserva = DAOFactorySQL.get_reserva_dao().read(reserva)
    if reserva is None:
        return jsonify({"success": False, "error" : "No se encontró una reserva con ese ID"}) , HTTPStatus.BAD_REQUEST

    if reserva.estado == 'F':
        return jsonify({"success": False, "error" : "La reserva ya ha finalizado"}) , HTTPStatus.BAD_REQUEST
    
    if reserva.estado == 'A':
        return jsonify({"success": False, "error" : "La reserva ya esta activa"}) , HTTPStatus.BAD_REQUEST
    
    reserva.estado = 'A'
    DAOFactorySQL.get_reserva_dao().update(reserva)

    return jsonify({"success": True, "message" : "Entrada registrada con éxito"}) , HTTPStatus.OK


@token_required
@reserva_bp.route('/enviar_registro', methods=['POST'])
def enviar_registro():
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    json_recibido = request.get_json()

    if 'correo' not in json_recibido or len(json_recibido['correo'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo correo vacio"})
    
    req_correo = json_recibido["correo"]

    #Verificar que el correo sea válido y no exista en BD. 
    error = validar_correo(req_correo)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    msg = MIMEText(f'<h1>Solicitud de registro</h1>'\
                f'<p>Has solicitado el registro en ParkUD, el enlace para registrarte es: <a href="http://google.com.co">Link</a></p>'\
                f'<p>Cordialmente <br> ParkUD Colombia</p>'                   
                , 'html')

    msg['Subject'] = 'Solicitud de registro ParkUD'
    msg['From'] = 'info@parkud.com'
    msg['To'] = req_correo

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
        server.login(current_app.config['MAIL'], current_app.config['MAIL_PASS'])
        server.sendmail(current_app.config['MAIL'], req_correo, msg.as_string())

    return jsonify({"success": True, "message" : "Se ha enviado el correo de registro al cliente"}) , HTTPStatus.OK


@token_required
@reserva_bp.route('/<int:id_reserva>/salida', methods=['POST'])
def registrar_salida(id_reserva):
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    reserva = Reserva(id=id_reserva)
    reserva = DAOFactorySQL.get_reserva_dao().read(reserva)
    if reserva is None:
        return jsonify({"success": False, "error" : "No se encontró una reserva con ese ID"}) , HTTPStatus.BAD_REQUEST

    if reserva.estado == 'F':
        return jsonify({"success": False, "error" : "La reserva ya ha finalizado"}) , HTTPStatus.BAD_REQUEST
    
    if reserva.estado == 'R':
        return jsonify({"success": False, "error" : "La reserva aun no ha iniciado"}) , HTTPStatus.BAD_REQUEST
    
    reserva.estado = 'F'
    fechaActual = datetime.datetime.now()
    reserva.registroSalida = fechaActual.strftime("%Y-%m-%d %H:%M:%S")
    
    fechaInicio = datetime.datetime.strptime(str(reserva.horaInicio), "%Y-%m-%d %H:%M:%S")
    fechaFin = datetime.datetime.strptime(str(reserva.horaSalida), "%Y-%m-%d %H:%M:%S")
    if fechaActual > fechaFin:
        fechaFin = fechaActual

    minutos = (fechaFin - fechaInicio).total_seconds() / 60
    
    parqueadero = Parqueadero(id=reserva.idParqueadero)
    parqueadero = DAOFactorySQL.get_parqueadero_dao().read(parqueadero)

    tarifa = DAOFactorySQL.get_tarifa_dao().get_tarifa_x_sede_x_tpParq(reserva.idSede,parqueadero.idTipo_Parqueadero)
    if tarifa is None:
        return jsonify({"success": False, "error" : "Tarifa no encontrada para la sede y parqueadero de la reserva"}) , HTTPStatus.BAD_REQUEST

    reserva.subtotal = minutos * tarifa.valor

    DAOFactorySQL.get_reserva_dao().update(reserva)

    #PAGO de tarjeta

    return jsonify({"success": True, "message" : "Salida registrada con éxito"}) , HTTPStatus.OK


@token_required
@reserva_bp.route('/estado-general', methods=['GET'])
def estado_general():
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    operario = DAOFactorySQL.get_operario_dao().get_operario_x_usuario(usuario.idUsuario)
    if operario is None:
        return jsonify({"success": False, "error" : "El usuario no es un operario"}) , HTTPStatus.BAD_REQUEST
    
    parqueaderos = DAOFactorySQL.get_sede_dao().get_parqueaderos_tipo(operario.idSede)
    fechaActual = datetime.datetime.now()
    fecha_txt = fechaActual.strftime("%Y-%m-%d")

    parqueaderos_json = []
    for parqueadero in parqueaderos:
        place_parq = {"idParqueadero": parqueadero[0], "tipoParqueadero" : parqueadero[1], "reservas": []}
        reservas = DAOFactorySQL.get_reserva_dao().get_estado(fecha_txt,parqueadero[0],operario.idSede)
        if reservas is not None and len(reservas) > 0:
            place_parq["reservas"] = [{
                "idReserva": reserva[0],
                "horaInicio": reserva[1].strftime("%H:%M"),
                "horaSalida": reserva[2].strftime("%H:%M")
                } for reserva in reservas]
        parqueaderos_json.append(place_parq)


    return jsonify({"success": True, "message" : "Consulta registrada con éxito", "parqueaderos" : parqueaderos_json}) , HTTPStatus.OK



@token_required
@reserva_bp.route('/reservar', methods=['POST'])
def reservar():
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    json_recibido = request.get_json()

    error = verificar_datos_reservar(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    horaInicio_txt = json_recibido["horaInicio"]
    horaSalida_txt = json_recibido["horaSalida"]
    idTarjeta_txt = json_recibido["idTarjeta"]
    idSede_txt = json_recibido["idSede"]

    parqueadero = DAOFactorySQL.get_sede_dao().get_parqueadero_disponible(idSede_txt, horaInicio_txt, horaSalida_txt)
    if parqueadero is None:
        return jsonify({"success": False, "error" : "No se encontraron parqueaderos disponibles"}) , HTTPStatus.BAD_REQUESTre

    reserva = Reserva(horaInicio = horaInicio_txt,
                      horaSalida = horaSalida_txt,
                      idTarjeta = idTarjeta_txt,
                      idParqueadero = parqueadero[0],
                      idSede = idSede_txt)

    DAOFactorySQL.get_reserva_dao().create(reserva)

    return jsonify({"success": True, "message" : "Reserva registrada con éxito", "reserva": {
        "idReserva" : reserva.idReserva,
        "horaInicio" : reserva.horaInicio,
        "horaSalida" : reserva.horaSalida
    }}) , HTTPStatus.OK


def verificar_datos_reservar(json_recibido):
    if 'horaInicio' not in json_recibido or len(json_recibido['horaInicio']) == 0:
        return jsonify({"success": False, "error" : "Campo horaInicio vacio"})
    
    if 'horaSalida' not in json_recibido or len(json_recibido['horaSalida']) == 0:
        return jsonify({"success": False, "error" : "Campo horaSalida vacio"})
    
    if 'idTarjeta' not in json_recibido or len(json_recibido['idTarjeta']) == 0:
        return jsonify({"success": False, "error" : "Campo idTarjeta vacio"})
    
    if 'idSede' not in json_recibido or len(json_recibido['idSede']) == 0:
        return jsonify({"success": False, "error" : "Campo idSede vacio"})

    return None