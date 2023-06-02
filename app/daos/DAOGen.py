from abc import ABC, abstractmethod
class DAOGenerico(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def findall(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

class ClienteDAO(DAOGenerico):

    @abstractmethod
    def get_cliente_usuario(self, id_usuario):
        pass

class TarjetaDAO(DAOGenerico):
    @abstractmethod
    def get_tarjetas_cliente(self, cliente_id):
        pass

class UsuarioDAO(DAOGenerico):

    @abstractmethod
    def get_usuario_correo(self, correo):
        pass

    @abstractmethod
    def get_usuario_username(self, usuario):
        pass

    @abstractmethod
    def get_usuario_username_password(self, usuario, password):
        pass

    @abstractmethod
    def get_usuario_username_doble_factor(self, usuario, doble_factor):
        pass

    @abstractmethod
    def get_total(self):
        pass

    @abstractmethod
    def get_usuario_correo_mod(self):
        pass
    
    @abstractmethod
    def get_usuario_username_mod(self):
        pass
    

    
class ConfiguracionDAO(DAOGenerico):
    pass

class ParqueaderoDAO(DAOGenerico):
    pass

class OperarioDAO(DAOGenerico):
    pass

class AdministradorDAO(DAOGenerico):
    
    @abstractmethod
    def get_admin_x_usuario(self):
        pass
    
    @abstractmethod
    def contar_total(self):
        pass

    @abstractmethod
    def get_administradores(self, limit=None, offset=None):
        pass

class SedeDAO(DAOGenerico):
    @abstractmethod
    def filtrar(self, filtro):
        pass
  
    @abstractmethod
    def get_parqueadero_disponible(self,sede, hora_inicio, hora_fin):
        pass
      
    @abstractmethod
    def get_cantidad_sedes(self):
        pass

    @abstractmethod
    def get_sedes_activas(self,limit,offset):
        pass

    @abstractmethod
    def get_sede_x_admin(self,idAdministrador):
        pass

class CaracteristicaDAO(DAOGenerico):
    @abstractmethod
    def get_carac_x_sede(self,idSede):
        pass
    

class Caracteristica_SedeDAO(DAOGenerico):
    @abstractmethod
    def eliminar_x_sede(self):
        pass

class Tipo_ParqueaderoDAO(DAOGenerico):
    pass

class TarifaDAO(DAOGenerico):
    pass

class UbicacionDAO(DAOGenerico):
    @abstractmethod
    def get_regionales(self):
        pass

    @abstractmethod
    def get_ubicacion_regional(self,idregional):
        pass


class ReservaDAO(DAOGenerico):
    @abstractmethod
    def get_datos(self,idReserva):
        pass