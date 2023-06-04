from abc import ABC, abstractmethod
import pandas as pd
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
import json

class ReporteDirector():

    def __init__(self, reporte: ReporteGeneral):
        self._reporteGeneral = reporte

    def build():
        pass

class ReporteGeneral(ABC):
    self._export = None

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
        self.cantidad = False

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def export(self):
        pass


class ReporteCiudad(ReporteGeneral):
    def initialize(self):
        pass

    def export(self):
        pass

class ReporteClienteTotal(ReporteGeneral):
    def initialize(self):
        pass

    def export(self):
        pass

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
        excel_buffer.save()
        
        # Leer el archivo Excel guardado en memoria
        with open('temp.xlsx', 'rb') as file:
            excel_data = file.read()
        
        # Codificar el archivo Excel en Base64
        encoded_excel = base64.b64encode(excel_data).decode('utf-8')
        
        return encoded_excel

class ExportHtml(Export):
    def export(self, json_object):
        pass
