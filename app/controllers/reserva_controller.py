from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from app.funciones.token_jwt import token_required, validar_superadmin_token, validar_admin_token, validar_usuario_token
from app.models.entidades import Sede, Caracteristica, Tipo_Parqueadero, Ubicacion, Usuario, Tarifa, Caracteristica_Sede, Parqueadero, Operario
from app.controllers.usuario_controller import validar_correo
from app.daos.DAOFactory import DAOFactorySQL


reserva_bp = Blueprint('reserva', __name__)

@token_required
@reserva_bp.route('/<int:id_reserva>', methods=['GET'])
def obtener_reserva(id_reserva):
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    reserva = Reserva(id=id_reserva)
    reserva = DAOFactorySQL.get_reserva_dao().read(reserva)  
    if reserva is None:
        return jsonify({"success": False, "error" : "No se encontró una reserva con ese ID"}) , HTTPStatus.BAD_REQUESTOK

    if reserva.estado == 'F':
        return jsonify({"success": False, "error" : "La reserva ya ha finalizado"}) , HTTPStatus.BAD_REQUESTOK
    
    if reserva.estado == 'A':
        return jsonify({"success": False, "error" : "La reserva en este momento esta activa"}) , HTTPStatus.BAD_REQUESTOK
    
    parqueadero = Parqueadero(id=reserva.idParqueadero)
    parqueadero = DAOFactorySQL.get_parqueadero_dao().read(parqueadero)

    tipoParqueadero = Tipo_Parqueadero(id=parqueadero.idTipo_Parqueadero)
    tipoParqueadero = DAOFactorySQL.get_tipo_parqueadero_dao().read(id=parqueadero.idTipo_Parqueadero)

    reserva = {
        "idReserva": reserva.idReserva,
        "horaInicio": reserva.horaInicio,
        "horaSalida": reserva.horaSalida,
        "idParqueadero": parqueadero.idParqueadero,
        "idTipo_Parqueadero": parqueadero.idTipo_Parqueadero,
        "tipoParqueadero" : tipoParqueadero.nombre
    }

    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "reserva" : reserva}) , HTTPStatus.OK
