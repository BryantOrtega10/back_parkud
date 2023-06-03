class FiltroSQL:
    def __init__(self):
        self.region = None
        self.ciudad = None
        self.caracteristicas = []
        self.tipos_parqueadero = []
        self.hora_inicio = None
        self.hora_fin = None
        self.fidelizacion = None
        self.idSede = None

    def toSQL(self):
        tablas = ["sede s"]
        condiciones = []

        if self.region is not None:
            tablas.extend(["ubicacion c", "ubicacion r"])
            condiciones.extend([
                "c.idUbicacion = s.idUbicacion",
                "r.idUbicacion = c.fkUbicacion",
                f"r.idUbicacion = {self.region}"
            ])
        
        if self.ciudad is not None:
            tablas.append("ubicacion c")
            condiciones.append(f"c.idUbicacion = {self.ciudad}")
        
        if self.caracteristicas:
            tablas.append("caracteristica_sede cs")
            caracteristicas_str = ', '.join(str(c) for c in self.caracteristicas)
            condiciones.append(f"cs.idSede = s.idSede AND cs.idCaracteristica IN ({caracteristicas_str})")
        
        if self.tipos_parqueadero:
            tablas.append("parqueadero p")
            tipos_str = ', '.join(str(t) for t in self.tipos_parqueadero)
            condiciones.append(f"p.idSede = s.idSede AND p.idTipo_Parqueadero IN ({tipos_str})")
        
        if self.hora_inicio is not None and self.hora_fin is not None:
            tablas.append("parqueadero p")
            condiciones.append(f'''s.idSede = p.idSede
                AND p.idParqueadero NOT IN (
                    SELECT r.idParqueadero
                    FROM reserva r
                    WHERE (
                    TIMESTAMP('{self.hora_inicio}') BETWEEN r.horaInicio AND r.horaSalida
                    OR TIMESTAMP('{self.hora_fin}') BETWEEN r.horaInicio AND r.horaSalida
                    OR r.horaInicio BETWEEN TIMESTAMP('{self.hora_inicio}') AND TIMESTAMP('{self.hora_fin}')
                    OR r.horaSalida BETWEEN TIMESTAMP('{self.hora_inicio}') AND TIMESTAMP('{self.hora_fin}')
                    )
                    AND r.estado <> 'F'
                ) ''')

        if self.fidelizacion is not None :
            condiciones.append(f"s.fidelizacion = {self.fidelizacion}")

        if self.idSede is not None :
            condiciones.append(f"s.idSede = {self.idSede}")

        tablas = list(set(tablas))
        columnas = "s.idSede, s.nombre, s.latitud, s.longitud, s.estado, s.fidelizacion, s.horaInicio, s.horaFin, s.tiempoCompleto, s.idAdministrador, s.idUbicacion"
        consulta = "SELECT DISTINCT "+columnas+" FROM " + ", ".join(tablas)
        if condiciones:
            consulta += " WHERE " + " AND ".join(condiciones)        

        print(consulta)
        return consulta


class FiltroBuilder:
    def __init__(self):
        self.filtro = FiltroSQL()

    def region(self, id_region):
        self.filtro.region = id_region
        return self

    def ciudad(self, id_ciudad):
        self.filtro.ciudad = id_ciudad
        return self
    
    def tipos_parqueadero(self, tipo_parqueadero):
        self.filtro.tipos_parqueadero.append(tipo_parqueadero)
        return self
    
    def caracteristicas(self, caracteristica):
        self.filtro.caracteristicas.append(caracteristica)
        return self
    
    def horas(self, hora_inicio, hora_fin):
        self.filtro.hora_inicio = hora_inicio
        self.filtro.hora_fin = hora_fin
        return self

    def fidelizacion(self, fidelizacion):
        self.filtro.fidelizacion = fidelizacion
        return self

    def build(self):
        return self.filtro
