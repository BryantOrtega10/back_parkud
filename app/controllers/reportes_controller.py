from flask import Blueprint, request, jsonify
from http import HTTPStatus
from app.funciones.token_jwt import token_required, validar_superadmin_token
from app.models.entidades import Usuario, Log
from app.daos.DAOFactory import DAOFactorySQL
from app.bridge_reportes.bridge import ReporteCiudad, ReporteClienteTotal, ReporteDirector, ReporteGeneral, Export, ExportExcel, ExportJson, ExportPdf

estadisticas_bp = Blueprint('estadisticas', __name__)

reportes_bp = Blueprint('reportes', __name__)
@token_required
@reportes_bp.route('/<string:reporte>/<string:export>', methods=["GET"])
def consultar_reportes(reporte, export):
    usuario = validar_superadmin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    rep = None
    if reporte == "ciudad":
        rep = ReporteCiudad()
    elif reporte == "cliente":
        rep = ReporteClienteTotal()
    else:
        return jsonify({"success": False, "error" : "Reporte desconocido"}), HTTPStatus.BAD_REQUEST

    exp = None
    if export == "PDF":
        exp = ExportPdf()
    elif export == "EXCEL":
        exp = ExportExcel()
    elif export == "JSON":
        exp = ExportJson()        
    else:
        return jsonify({"success": False, "error" : "Export desconocido"}), HTTPStatus.BAD_REQUEST

    rep.export_obj = exp
    data = ReporteDirector(rep).build()

    log = Log(mensaje="Generó reporte de " + reporte + " en formato " + export, ip=request.remote_addr, idUsuario=usuario.idUsuario)
    DAOFactorySQL.get_log_dao().create(log)
    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "export" : data}) , HTTPStatus.OK



@token_required
@estadisticas_bp.route('/<string:estadistica_txt>', methods=["GET"])
@estadisticas_bp.route('/<string:estadistica_txt>/<int:regional>', methods=["GET"])
@estadisticas_bp.route('/<string:estadistica_txt>/<int:regional>/<int:sede>', methods=["GET"])
def consultar_estadisticas(estadistica_txt, regional = None, sede = None):
    usuario = validar_superadmin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    arrMeses = [
        "Enero", "Febrero", "Marzo", "Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
    ]

    estadistica = []
    if estadistica_txt == "cupos":
        estadistica = DAOFactorySQL.get_sede_dao().get_estadistica_cupos(regional, sede)
        estadistica = [{"tipoParqueadero" : estad[1], "porcentaje" : round(estad[0] * 100)} for estad in estadistica]
    elif estadistica_txt == "reservas":
        estadistica = DAOFactorySQL.get_sede_dao().get_estadistica_reservas(regional, sede)
        estadistica = [{"mes" : arrMeses[estad[0] - 1], "cantidad" : estad[1]} for estad in estadistica]
    elif estadistica_txt == "ganancias":
        estadistica = DAOFactorySQL.get_sede_dao().get_estadistica_ganancias(regional, sede)
        estadistica = [{"mes" : arrMeses[estad[0] - 1], "ganancias" : estad[1]} for estad in estadistica]
    else:
        return jsonify({"success": False, "error" : "Estadistica desconocida"}), HTTPStatus.BAD_REQUEST
    
    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "estadistica" : estadistica}) , HTTPStatus.OK