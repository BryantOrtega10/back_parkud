from app.daos.DAOSql import ClienteDAOSQL, TarjetaDAOSQL, UsuarioDAOSQL, ConfiguracionDAOSQL, AdministradorDAOSQL, SedeDAOSQL, CaracteristicaDAOSQL, Caracteristica_SedeDAOSQL, Tipo_ParqueaderoDAOSQL, TarifaDAOSQL, UbicacionDAOSQL, ParqueaderoDAOSQL, OperarioDAOSQL

class DAOFactorySQL:
    _instance = None
    _cliente_dao = None
    _tarjeta_dao = None
    _usuario_dao = None
    _configuracion_dao = None
    _administrador_dao = None
    _sede_dao = None
    _caracteristica_dao = None
    _caracteristica_sede_dao = None
    _tipo_parqueadero_dao = None
    _tarifa_dao = None
    _ubicacion_dao = None
    _parqueadero_dao = None
    _operario_dao = None

    def __new__(self, *args, **kwargs):
        if not self._instance:
            self._instance = super().__new__(self)
        return self._instance

    @classmethod
    def get_cliente_dao(self):
        if not self._cliente_dao:
            self._cliente_dao = ClienteDAOSQL()  
        return self._cliente_dao

    @classmethod
    def get_tarjeta_dao(self):
        if not self._tarjeta_dao:
            self._tarjeta_dao = TarjetaDAOSQL()  
        return self._tarjeta_dao

    @classmethod
    def get_usuario_dao(self):
        if not self._usuario_dao:
            self._usuario_dao = UsuarioDAOSQL() 
        return self._usuario_dao
    
    @classmethod
    def get_configuracion_dao(self):
        if not self._configuracion_dao:
            self._configuracion_dao = ConfiguracionDAOSQL() 
        return self._configuracion_dao
    
    @classmethod
    def get_administrador_dao(self):
        if not self._administrador_dao:
            self._administrador_dao = AdministradorDAOSQL() 
        return self._administrador_dao
        
    @classmethod    
    def get_sede_dao(self):
        if not self._sede_dao:
            self._sede_dao = SedeDAOSQL()
        return self._sede_dao
    
    @classmethod            
    def get_caracteristica_dao(self):
        if not self._caracteristica_dao:
            self._caracteristica_dao = CaracteristicaDAOSQL()
        return self._caracteristica_dao
    
    @classmethod            
    def get_caracteristica_sede_dao(self):
        if not self._caracteristica_sede_dao:
            self._caracteristica_sede_dao = Caracteristica_SedeDAOSQL()
        return self._caracteristica_sede_dao
    
    @classmethod            
    def get_tipo_parqueadero_dao(self):
        if not self._tipo_parqueadero_dao:
            self._tipo_parqueadero_dao = Tipo_ParqueaderoDAOSQL()
        return self._tipo_parqueadero_dao
    
    @classmethod            
    def get_tarifa_dao(self):
        if not self._tarifa_dao:
            self._tarifa_dao = TarifaDAOSQL()
        return self._tarifa_dao
    
    @classmethod            
    def get_ubicacion_dao(self):
        if not self._ubicacion_dao:
            self._ubicacion_dao = UbicacionDAOSQL()
        return self._ubicacion_dao
    
    @classmethod            
    def get_parqueadero_dao(self):
        if not self._parqueadero_dao:
            self._parqueadero_dao = ParqueaderoDAOSQL()
        return self._parqueadero_dao

    @classmethod            
    def get_operario_dao(self):
        if not self._operario_dao:
            self._operario_dao = OperarioDAOSQL()
        return self._operario_dao