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

    
class ConfiguracionDAO(DAOGenerico):
    pass

class AdministradorDAO(DAOGenerico):
    pass

class SedeDAO(DAOGenerico):
    def filtrar(self, filtro):
        pass

    def get_parqueadero_disponible(self,sede, hora_inicio, hora_fin):
        pass

class CaracteristicaDAO(DAOGenerico):
    pass

class Caracteristica_SedeDAO(DAOGenerico):
    pass

class Tipo_ParqueaderoDAO(DAOGenerico):
    pass

class TarifaDAO(DAOGenerico):
    pass

class UbicacionDAO(DAOGenerico):
    pass

class Reserva(DAOGenerico):
    pass