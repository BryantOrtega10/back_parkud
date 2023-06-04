from abc import ABC, abstractmethod
import os
import pandas as pd
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
import json
from app.daos.DAOFactory import DAOFactorySQL

class ReporteDirector():

    def __init__(self, reporte):
        self._reporteGeneral = reporte

    def build(self):        
        self._reporteGeneral.initialize()
        return self._reporteGeneral.doExport()

class ReporteGeneral(ABC):

    def __init__(self) :
        self._idReserva = False
        self._ciudad = False
        self._region = False
        self._sede = False
        self._tipoParqueadero = False
        self._fechaInicio = False
        self._fechaFin = False
        self._registroSalida = False
        self._cliente = False
        self._total = False
        self._administrador = False
        self._cantidad = False
        self.export_obj = None

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def doExport(self):
        pass
    
    def obtenerDesdeBD(self):
        return DAOFactorySQL.get_reserva_dao().get_report(self._idReserva,self._ciudad,self._region,self._sede,self._tipoParqueadero,self._fechaInicio,self._fechaFin,self._registroSalida,self._cliente,self._total,self._administrador,self._cantidad)

class ReporteCiudad(ReporteGeneral):

    def initialize(self):
        self._idReserva = True
        self._ciudad = True
        self._region = True
        self._sede = True

    def doExport(self):
        reporte = self.obtenerDesdeBD()
        reporte = [{
            "idReserva" : rep[0],
            "ciudad" : rep[1],
            "region" : rep[2],
            "sede" : rep[3]
        } for rep in reporte]
        return self.export_obj.export(reporte)

class ReporteClienteTotal(ReporteGeneral):

    def initialize(self):
        self._idReserva = True
        self._tipoParqueadero = True
        self._fechaInicio = True
        self._fechaFin = True
        self._cliente = True
        self._total = True

    def doExport(self):
        reporte = self.obtenerDesdeBD()
        print(reporte)
        reporte = [{
            "idReserva" : rep[0],
            "tipoParqueadero" : rep[1],
            "fechaInicio" : rep[2],
            "fechaFin" : rep[3],
            "cliente" : rep[4],
            "total" : rep[5]
        } for rep in reporte]
        return self.export_obj.export(reporte)

class Export(ABC):

    @abstractmethod
    def export(self):
        pass


class ExportPdf(Export):
    def export(self, json_object):
        data = []
    
        # Obtener las claves del primer objeto para crear las cabeceras de la tabla
        headers = list(json_object[0].keys())
        
        # Agregar las cabeceras a la lista de datos
        data.append(headers)
        
        # Agregar los valores al resto de filas de la tabla
        for item in json_object:
            row = [str(item[key]) for key in headers]
            data.append(row)
        
        # Crear el documento PDF en memoria
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        
        # Crear la tabla con los datos
        table = Table(data)
        
        # Estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        
        # Aplicar el estilo a la tabla
        table.setStyle(style)
        
        # Crear el contenido del PDF y agregar la tabla
        content = [table]
        
        # Construir el PDF
        doc.build(content)
        
        # Obtener el contenido del PDF en memoria
        pdf_data = pdf_buffer.getvalue()
        
        # Codificar el archivo PDF en Base64
        encoded_pdf = base64.b64encode(pdf_data).decode('utf-8')
        
        return encoded_pdf


class ExportExcel(Export):
    def export(self, json_object):

        df = pd.DataFrame(json_object)
    
        # Crear un objeto BytesIO para almacenar el archivo Excel en memoria
        excel_buffer = pd.ExcelWriter('temp.xlsx', engine='xlsxwriter')
        
        # Exportar el DataFrame a un archivo Excel
        df.to_excel(excel_buffer, index=False)
        excel_buffer.close()
        
        # Leer el archivo Excel guardado en memoria
        with open('temp.xlsx', 'rb') as file:
            excel_data = file.read()
        
        # Codificar el archivo Excel en Base64
        encoded_excel = base64.b64encode(excel_data).decode('utf-8')
        os.remove("temp.xlsx")
        return encoded_excel

class ExportJson(Export):
    def export(self, json_object):
        return json_object
