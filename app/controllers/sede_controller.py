from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from app.funciones.token_jwt import token_required, validar_superadmin_token, validar_admin_token, validar_usuario_token
from app.models.entidades import Sede, Caracteristica, Tipo_Parqueadero, Ubicacion, Usuario, Tarifa, Caracteristica_Sede, Parqueadero, Operario, Log
from app.controllers.usuario_controller import validar_correo
from app.daos.DAOFactory import DAOFactorySQL
from datetime import datetime
from app.builder_sql.query_builder import FiltroBuilder


sede_bp = Blueprint('sede', __name__)

@token_required
@sede_bp.route('/', methods=["GET"])
@sede_bp.route('/<int:limit>', methods=['GET'])
@sede_bp.route('/<int:limit>/<int:offset>', methods=['GET'])
def obtener_sedes(limit = 10, offset = 0):
    usuario = validar_superadmin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    cuenta = DAOFactorySQL.get_sede_dao().get_cantidad_sedes()
    sedes = DAOFactorySQL.get_sede_dao().get_sedes_activas(limit, offset)
    sedes = [{"idSede": sede.idSede, "nombre" : sede.nombre} for sede in sedes]
    log = Log(mensaje="Consultó las sedes con limit y offset", ip=request.remote_addr, idUsuario=usuario.idUsuario)
    DAOFactorySQL.get_log_dao().create(log)
    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "sedes" : sedes, "cuenta" : cuenta}) , HTTPStatus.OK

@token_required
@sede_bp.route('/obtener_regionales', methods=["GET"])
def obtener_regionales():
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    regionales = DAOFactorySQL.get_ubicacion_dao().get_regionales()
    regionales = [{"idUbicacion": regional.idUbicacion, "descripcion" : regional.descripcion} for regional in regionales]
    log = Log(mensaje="Consultó las regionales", ip=request.remote_addr, idUsuario=usuario.idUsuario)
    DAOFactorySQL.get_log_dao().create(log)

    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "regionales" : regionales}) , HTTPStatus.OK

@token_required
@sede_bp.route('/obtener_datos/<int:id_regional>', methods=["GET"])
def obtener_datos(id_regional):
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    ciudades = DAOFactorySQL.get_ubicacion_dao().get_ubicacion_regional(id_regional)
    ciudades = [{"idUbicacion": ciudad.idUbicacion, "descripcion" : ciudad.descripcion} for ciudad in ciudades]
    caracteristicas = DAOFactorySQL.get_caracteristica_dao().findall(Caracteristica())
    caracteristicas = [{"idCaracteristica": caracteristica.idCaracteristica, "nombre" : caracteristica.nombre} for caracteristica in caracteristicas]
    tiposParqueaderos = DAOFactorySQL.get_tipo_parqueadero_dao().findall(Tipo_Parqueadero())
    tiposParqueaderos = [{"idTipo_Parqueadero": tiposParqueadero.idTipo_Parqueadero, "nombre" : tiposParqueadero.nombre} for tiposParqueadero in tiposParqueaderos]

    log = Log(mensaje="Consultó las ciudades y los datos que componen una sede", ip=request.remote_addr, idUsuario=usuario.idUsuario)
    DAOFactorySQL.get_log_dao().create(log)

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
    DAOFactorySQL.get_sede_dao().create(sede)
    for r_tarifa in req_tarifas:
        tarifa = Tarifa(valor=r_tarifa["valor"], idSede=sede.idSede, idTipo_Parqueadero=r_tarifa["idTipo_Parqueadero"])
        DAOFactorySQL.get_tarifa_dao().create(tarifa)
        for i in range(0,int(r_tarifa["cupo"])):
            parqueadero = Parqueadero(idSede=sede.idSede, idTipo_Parqueadero=r_tarifa["idTipo_Parqueadero"])
            DAOFactorySQL.get_parqueadero_dao().create(parqueadero)

    for r_caracteristica in req_caracteristicas:
        caracteristica_sede = Caracteristica_Sede(idCaracteristica=r_caracteristica["idCaracteristica"], idSede=sede.idSede)
        DAOFactorySQL.get_caracteristica_sede_dao().create(caracteristica_sede)

    log = Log(mensaje="Agregó una la sede: " + req_nombre, ip=request.remote_addr, idUsuario=usuario.idUsuario)
    DAOFactorySQL.get_log_dao().create(log)

    return jsonify({"success": True, "message" : "Sede creada con éxito", "sede": {
        "idSede": sede.idSede, "nombre" : sede.nombre
    }}) , HTTPStatus.OK

@token_required
@sede_bp.route('/mi-sede', methods=["GET"])
def mi_sede():
    usuario = validar_admin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST

    adminitrador = DAOFactorySQL.get_administrador_dao().get_admin_x_usuario(usuario.idUsuario)
    sede = DAOFactorySQL.get_sede_dao().get_sede_x_admin(adminitrador.idAdministrador)
   
    if sede.idSede is None:
        return jsonify({"success": False, "error" : "El usuario no esta relacionado a ninguna sede"}) , HTTPStatus.BAD_REQUEST
    
    ciudad = Ubicacion(id=sede.idUbicacion)
    ciudad = DAOFactorySQL.get_ubicacion_dao().read(ciudad)

    regional = Ubicacion(id=ciudad.fkUbicacion)
    regional = DAOFactorySQL.get_ubicacion_dao().read(regional)

    ciudades = DAOFactorySQL.get_ubicacion_dao().get_ubicacion_regional(regional.idUbicacion)
    ciudades = [{"idUbicacion": ciudad2.idUbicacion, "descripcion" : ciudad2.descripcion} for ciudad2 in ciudades]
    caracteristicas = DAOFactorySQL.get_caracteristica_dao().findall(Caracteristica())
    caracteristicas = [{"idCaracteristica": caracteristica.idCaracteristica, "nombre" : caracteristica.nombre} for caracteristica in caracteristicas]
    tiposParqueaderos = DAOFactorySQL.get_tipo_parqueadero_dao().findall(Tipo_Parqueadero())
    tiposParqueaderos = [{"idTipo_Parqueadero": tiposParqueadero.idTipo_Parqueadero, "nombre" : tiposParqueadero.nombre} for tiposParqueadero in tiposParqueaderos]
    
    regionales = DAOFactorySQL.get_ubicacion_dao().get_regionales()
    regionales = [{"idUbicacion": regional2.idUbicacion, "descripcion" : regional2.descripcion} for regional2 in regionales]    

    caracteristicas_sel = DAOFactorySQL.get_caracteristica_dao().get_carac_x_sede(sede.idSede)
    caracteristicas_sel = [{"idCaracteristica": caracteristica.idCaracteristica, "nombre" : caracteristica.nombre} for caracteristica in caracteristicas_sel]

    tarifas = DAOFactorySQL.get_tarifa_dao().get_tarifa_x_sede(sede.idSede)
    tarifas = [{"idTarifa": tarifa.idTarifa, "valor" : tarifa.valor, "idTipo_Parqueadero" : tarifa.idTipo_Parqueadero} for tarifa in tarifas]

    cupos = DAOFactorySQL.get_parqueadero_dao().get_cuenta_parq_x_tipoParq_x_sede(sede.idSede)
    
    operarios = DAOFactorySQL.get_operario_dao().get_operarios_x_sede(sede.idSede);
    operarios = [{"idOperario": operario.idOperario, "nombre" : operario.nombre, "apellido" : operario.nombre} for operario in operarios]
    
    sede.horaInicio = datetime.strptime(str(sede.horaInicio), "%H:%M:%S")
    sede.horaFin = datetime.strptime(str(sede.horaFin), "%H:%M:%S")
    sede = {
        "idSede": sede.idSede,
        "nombre": sede.nombre,
        "latitud": sede.latitud,
        "longitud": sede.longitud,
        "fidelizacion": sede.fidelizacion,
        "horaInicio": sede.horaInicio.strftime("%H:%M"),
        "horaFin": sede.horaFin.strftime("%H:%M"),
        "tiempoCompleto": sede.tiempoCompleto,
        "ciudad": {
            "idUbicacion": ciudad.idUbicacion,
            "descripcion" : ciudad.descripcion
        },
        "regional": {
            "idUbicacion": regional.idUbicacion,
            "descripcion" : regional.descripcion
        },       
        "caracteristicas_sel": caracteristicas_sel,
        "tarifas": tarifas,
        "cupos": cupos,
        "operarios" : operarios    
    }
    
    log = Log(mensaje="Consultó los datos de la sede que tiene relacionada", ip=request.remote_addr, idUsuario=usuario.idUsuario)
    DAOFactorySQL.get_log_dao().create(log)

    return jsonify({"success": True, "message" : "Consulta realizada con éxito", 
                    "sede" : sede,
                    "regionales": regionales,
                    "ciudades": ciudades,
                    "caracteristicas": caracteristicas,
                    "tiposParqueaderos" : tiposParqueaderos
                    }) , HTTPStatus.OK

@token_required
@sede_bp.route('/editar/<int:idSede>', methods=["PUT"])
def modificar(idSede):
    usuario = validar_admin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios_sede_edit(json_recibido)
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
    req_idUbicacion = json_recibido["idUbicacion"]
    req_caracteristicas = json_recibido["caracteristicas"]
    req_tarifas = json_recibido["tarifas"]
    
    log = Log(mensaje="Modificó la sede: " + req_nombre, ip=request.remote_addr, idUsuario=usuario.idUsuario)
    DAOFactorySQL.get_log_dao().create(log)

    sede = Sede(id= idSede)
    sede = DAOFactorySQL.get_sede_dao().read(sede)
    sede.nombre = req_nombre 
    sede.latitud = req_latitud 
    sede.longitud = req_longitud 
    sede.fidelizacion = req_fidelizacion 
    sede.horaInicio = req_horaInicio 
    sede.horaFin = req_horaFin 
    sede.tiempoCompleto = req_tiempoCompleto 
    sede.idUbicacion = req_idUbicacion 
    
    DAOFactorySQL.get_sede_dao().update(sede)
    DAOFactorySQL.get_caracteristica_sede_dao().eliminar_x_sede(idSede)

    for r_tarifa in req_tarifas:
        tarifa = Tarifa(valor=r_tarifa["valor"], idSede=sede.idSede, idTipo_Parqueadero=r_tarifa["idTipo_Parqueadero"], id=r_tarifa["idTarifa"])
        DAOFactorySQL.get_tarifa_dao().update(tarifa)
        # for i in range(0,int(r_tarifa["cupo"])):
        #     parqueadero = Parqueadero(idSede=sede.idSede, idTipo_Parqueadero=r_tarifa["idTipo_Parqueadero"])
        #     DAOFactorySQL.get_parqueadero_dao().create(parqueadero)

    for r_caracteristica in req_caracteristicas:
        caracteristica_sede = Caracteristica_Sede(idCaracteristica=r_caracteristica["idCaracteristica"], idSede=sede.idSede)
        DAOFactorySQL.get_caracteristica_sede_dao().create(caracteristica_sede)

    return jsonify({"success": True, "message" : "Sede modificada con éxito", "sede": {
        "idSede": sede.idSede, "nombre" : sede.nombre
    }}) , HTTPStatus.OK

@token_required
@sede_bp.route('/buscar-sede', methods=["POST"])
def buscar_sede():
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    log = Log(mensaje="Buscó sedes", ip=request.remote_addr, idUsuario=usuario.idUsuario)
    DAOFactorySQL.get_log_dao().create(log)

    filtro = FiltroBuilder()

    json_recibido = request.get_json()
    if 'region' in json_recibido and len(json_recibido['region']) > 0:
        filtro = filtro.region(json_recibido["region"])

    if 'ciudad' in json_recibido and len(json_recibido['ciudad']) > 0:
        filtro = filtro.ciudad(json_recibido["ciudad"])

    if 'tipos_parqueadero' in json_recibido and len(json_recibido['tipos_parqueadero']) > 0:
        for tp in json_recibido['tipos_parqueadero']:
            filtro = filtro.tipos_parqueadero(tp["idTipo_Ubicacion"])

    if 'caracteristicas' in json_recibido and len(json_recibido['caracteristicas']) > 0:
        for tp in json_recibido['caracteristicas']:
            filtro = filtro.caracteristicas(tp["idCaracteristica"])
    
    if  'hora_inicio' in json_recibido and len(json_recibido['hora_inicio']) > 0 and \
        'hora_fin' in json_recibido and len(json_recibido['hora_fin']) > 0:
        filtro = filtro.horas(json_recibido['hora_inicio'],json_recibido['hora_fin'])
    
    if 'fidelizacion' in json_recibido and len(json_recibido['fidelizacion']) > 0:
        filtro = filtro.fidelizacion(json_recibido["fidelizacion"])
    
    sedes = DAOFactorySQL.get_sede_dao().filtrar(filtro.build())
    if sedes is None:
        sedes = []
    sedes = [{
        "idSede": sede.idSede, 
        "nombre" : sede.nombre,
        "latitud" : sede.latitud,
        "longitud" : sede.longitud,
        "estado" : sede.estado,
        "fidelizacion" : sede.fidelizacion,
        "horaInicio" : datetime.strptime(str(sede.horaInicio), "%H:%M:%S").strftime("%H:%M"),
        "horaFin" : datetime.strptime(str(sede.horaFin), "%H:%M:%S").strftime("%H:%M"),
        "tiempoCompleto" : sede.tiempoCompleto
        } for sede in sedes]
    
    return jsonify({"success": True, "message" : "Sede consultada con éxito", "sedes": sedes}) , HTTPStatus.OK

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



def verificar_datos_vacios_sede_edit(json_recibido):
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
    
    if 'idUbicacion' not in json_recibido or len(json_recibido['idUbicacion'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo idUbicacion vacio"})

    if 'caracteristicas' not in json_recibido or len(json_recibido['caracteristicas']) == 0:
        return jsonify({"success": False, "error" : "Campo caracteristicas vacio"})

    if 'tarifas' not in json_recibido or len(json_recibido['tarifas']) == 0:
        return jsonify({"success": False, "error" : "Campo tarifas vacio"})
    

    return None



