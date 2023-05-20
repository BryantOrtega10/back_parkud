from app.daos.DAOSql import ClienteDAOSQL, TarjetaDAOSQL, UsuarioDAOSQL, ConfiguracionDAOSQL

class DAOFactorySQL:
    _instance = None
    _cliente_dao = None
    _tarjeta_dao = None
    _usuario_dao = None
    _configuracion_dao = None

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