from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from app.funciones.token_jwt import token_required, validar_superadmin_token
from app.models.entidades import Sede, Caracteristica, Tipo_Parqueadero, Ubicacion, Usuario, Tarifa, Caracteristica_Sede

from app.daos.DAOFactory import DAOFactorySQL


sede_bp = Blueprint('sede', __name__)

@token_required
@sede_bp.route('/', methods=["GET"])
def obtener_sedes():
    usuario = validar_superadmin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    json_recibido = request.get_json()

    offset = 0
    if 'offset' in json_recibido:
        offset = int(json_recibido["offset"])
    
    limit = 10
    if 'limit' in json_recibido:
        limit = int(json_recibido["limit"])
    
    cuenta = DAOFactorySQL.get_sede_dao().contar_total()
    sedes = DAOFactorySQL.get_sede_dao().obtener_activas(offset, limit)

    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "sedes" : sedes, "cuenta" : cuenta}) , HTTPStatus.OK


@token_required
@sede_bp.route('/obtener_regionales', methods=["GET"])
def obtener_regionales():
    usuario = validar_superadmin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    regionales = DAOFactorySQL.get_ubicacion_dao().obtener_regionales()


    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "regionales" : regionales}) , HTTPStatus.OK

@token_required
@sede_bp.route('/obtener_datos/<int:id_regional>', methods=["GET"])
def obtener_datos(id_regional):
    usuario = validar_superadmin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    ciudades = DAOFactorySQL.get_ubicacion_dao().obtener_ubic_x_reg(id_regional)
    caracteristicas = DAOFactorySQL.get_caracteristica_dao().findall(Caracteristica())
    tiposParqueaderos = DAOFactorySQL.get_tipo_parqueadero_dao().findall(Tipo_Parqueadero())

    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "ciudades" : ciudades, "caracteristicas" : caracteristicas, "tiposParqueaderos" : tiposParqueaderos}) , HTTPStatus.OK


@token_required
@sede_bp.route('/agregar', methods=["POST"])
def agregar():
    usuario = validar_superadmin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios_sede(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    #los datos no estan vacíos, se obtienen en variables para mayor comodidad
    req_nombre = json_recibido["nombre"]
    req_latitud = json_recibido["latitud"]
    req_longitud = json_recibido["longitud"]
    req_fidelizacion = json_recibido["fidelizacion"]
    req_horaInicio = json_recibido["horaInicio"]
    req_horaFin = json_recibido["horaFin"]
    req_tiempoCompleto = json_recibido["tiempoCompleto"]
    req_idAdministrador = json_recibido["idAdministrador"]
    req_idUbicacion = json_recibido["idUbicacion"]
    req_caracteristicas = json_recibido["caracteristicas"]
    req_tarifas = json_recibido["tarifas"]
    
    sede = Sede(nombre=req_nombre,latitud=req_latitud,longitud=req_longitud,fidelizacion=req_fidelizacion,horaInicio=req_horaInicio,horaFin=req_horaFin,tiempoCompleto=req_tiempoCompleto,idAdministrador=req_idAdministrador,idUbicacion=req_idUbicacion)
    sede = DAOFactorySQL.get_sede_dao().create(sede)

    # {
    #     "idTipo_Parqueadero" : "1",
    #     "valor" : 1000
    # }
    for r_tarifa in req_tarifas:
        tarifa = Tarifa(valor=r_tarifa["valor"], idSede=sede.idSede, idTipo_Parqueadero=r_tarifa["idTipo_Parqueadero"])
        DAOFactorySQL.get_tarifa_dao().create(tarifa)

    # {
    #     "idCaracteristica" : "1"
    # }
    for r_caracteristica in req_caracteristicas:
        caracteristica_sede = Caracteristica_Sede(idCaracteristica=r_caracteristica["idCaracteristica"], idSede=sede.idSede)
        DAOFactorySQL.get_caracteristica_sede_dao().create(caracteristica_sede)

    return jsonify({"success": True, "message" : "Sede creada con éxito", "sede": {
        "idSede": sede.idSede, "nombre" : sede.nombre
    }}) , HTTPStatus.OK


def verificar_datos_vacios_sede(json_recibido):
    if 'nombre' not in json_recibido or len(json_recibido['nombre'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo nombre vacio"})
    
    if 'latitud' not in json_recibido or len(json_recibido['latitud'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo latitud vacio"})
    
    if 'longitud' not in json_recibido or len(json_recibido['longitud'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo longitud vacio"})
    
    if 'fidelizacion' not in json_recibido or len(json_recibido['fidelizacion'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo fidelizacion vacio"})
    
    if 'horaInicio' not in json_recibido or len(json_recibido['horaInicio'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo hora de inicio vacio"})

    if 'horaFin' not in json_recibido or len(json_recibido['horaFin'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo hora de fin vacio"})

    if 'tiempoCompleto' not in json_recibido or len(json_recibido['tiempoCompleto'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo tiempo Completo vacio"})
    
    if 'idAdministrador' not in json_recibido or len(json_recibido['idAdministrador'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo idAdministrador vacio"})

    if 'idUbicacion' not in json_recibido or len(json_recibido['idUbicacion'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo idUbicacion vacio"})

    if 'caracteristicas' not in json_recibido or len(json_recibido['caracteristicas']) == 0:
        return jsonify({"success": False, "error" : "Campo caracteristicas vacio"})

    if 'tarifas' not in json_recibido or len(json_recibido['tarifas']) == 0:
        return jsonify({"success": False, "error" : "Campo tarifas vacio"})
    

    return None
