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
    def get_cliente_correo(self, correo):
        pass

    @abstractmethod
    def get_cliente_usuario(self, id_usuario):
        pass

class TarjetaDAO(DAOGenerico):
    @abstractmethod
    def get_tarjetas_usuario(self):
        pass

class UsuarioDAO(DAOGenerico):
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