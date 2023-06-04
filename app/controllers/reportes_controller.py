from flask import Blueprint, request, jsonify
from http import HTTPStatus
from app.funciones.token_jwt import token_required, validar_superadmin_token
from app.models.entidades import Usuario, Log
from app.daos.DAOFactory import DAOFactorySQL
from app.bridge_reportes.bridge import ReporteCiudad, ReporteClienteTotal, ReporteDirector, ReporteGeneral, Export, ExportExcel, ExportJson, ExportPdf



reportes_bp = Blueprint('reportes', __name__)
@token_required
@reportes_bp.route('/<string:reporte>/<string:export>', methods=["GET"])
def obtener_sedes(reporte, export):
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
