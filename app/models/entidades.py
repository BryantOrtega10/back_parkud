import inspect

class Entidad:

    def __init__(self,id,list_no,id_txt):
        self.id = id
        self.no_attr = list_no
        self.id_txt = id_txt

    def get_attrs(self):
        atrrs= []
        values = []

        for i in inspect.getmembers(self):
            # to remove private and protected
            # functions
            if not i[0].startswith('_'):
                # To remove other methods that
                # doesnot start with a underscore
                if not inspect.ismethod(i[1]):
                    if i[0] not in self.no_attr:
                        atrrs.append(i[0])
                        values.append(i[1])
        return tuple(atrrs), tuple(values)
    
    def get_name_class(self):
        return type(self).__name__

    def __str__(self):
        c,v = self.get_attrs()
        zipped = zip(c,v)
        m =" ".join(f"{attr} : {str(value)}, \n" for attr,value in zipped)
        return '{ \n id : '+str(self.id)+', \n '+m+'}'


class Tarjeta(Entidad):
    def __init__(self, nombre = '', tipo = '', numero = '', fechaExpiracion = '', csv = '', token = '', idCliente = '', id=None):
        
        if id is not None:
            super().__init__(id,["no_attr","id","idTarjeta","id_txt"], 'idTarjeta')
            self.idTarjeta = id
        else:
            super().__init__(0,["no_attr","id","idTarjeta","id_txt"], 'idTarjeta')
            self.idTarjeta = id
        self.nombre = nombre
        self.tipo = tipo
        self.numero = numero
        self.fechaExpiracion = fechaExpiracion
        self.csv = csv
        self.token = token
        self.idCliente = idCliente
    

class Usuario(Entidad):
    def __init__(self, usuario = '', contrasena = '', correo = '', rol = '', cambiarContrasena = 1, contrasenaDobleFactor = '', numIntentosFallidos = 0, estado = 'A', token = None, id=None):
        if id is not None:
            super().__init__(id,["no_attr","id","idUsuario","id_txt"],'idUsuario')
            self.idUsuario = id
        else:
            super().__init__(0,["no_attr","id","idUsuario","id_txt"], 'idUsuario')
            self.idUsuario = 0
        
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol
        self.correo = correo
        self.cambiarContrasena = cambiarContrasena
        self.contrasenaDobleFactor = contrasenaDobleFactor
        self.numIntentosFallidos = numIntentosFallidos
        self.estado = estado
        self.token = token

class Cliente(Entidad):
    def __init__(self, nombre = '', apellido = '', telefono = '', documentoIdentidad = '', idUsuario = 0, id=None):
        if id is not None:
            super().__init__(id,["no_attr","id","idCliente","id_txt","tarjetas"], 'idCliente')
            self.idCliente = 0
        else:
            super().__init__(0,["no_attr","id","idCliente","id_txt","tarjetas"], 'idCliente')
            self.idCliente = 0

        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.documentoIdentidad = documentoIdentidad
        self.idUsuario = idUsuario
        self.tarjetas = list()

    def agregar_tarjeta(self, tarjeta):
        self.tarjetas.append(tarjeta)

    def eliminar_tarjeta(self, tarjeta):
        for i in range(0,len(self.tarjetas)):
            if self.tarjetas[i].id_tarjeta == tarjeta.id_tarjeta:
                self.tarjetas.pop(i)
        

class Configuracion(Entidad):
    def __init__(self, valor = '', tipoDeDato = '', id=None):
        if id is not None:
            super().__init__(id,["no_attr","id","id_txt"],'id')
        else:
            super().__init__(0,["no_attr","id","id_txt"], 'id')
       
        self.valor = valor
        self.tipoDeDato = tipoDeDato

class Administrador(Entidad):
    def __init__(self, nombre = '', apellido = '', documentoIdentidad = '', idUsuario = '', id=None):
        if id is not None:
            super().__init__(id,["no_attr","id","idAdministrador","id_txt"],'idAdministrador')
            self.idAdministrador = id
        else:
            super().__init__(0,["no_attr","id","idAdministrador","id_txt"], 'idAdministrador')
            self.idAdministrador = 0
        
        self.nombre = nombre
        self.apellido = apellido
        self.documentoIdentidad = documentoIdentidad
        self.idUsuario = idUsuario

class Sede(Entidad):
    def __init__(self, nombre = '', latitud = '', longitud = '', fidelizacion = '', horaInicio = '', horaFin = '', tiempoCompleto = '', idAdministrador = '', idUbicacion = '', id=None):
        if id is not None:
            super().__init__(id,["no_attr","id","idSede","id_txt"],'idSede')
            self.idSede = id
        else:
            super().__init__(0,["no_attr","id","idSede","id_txt"], 'idSede')
            self.idSede = 0
        
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.fidelizacion = fidelizacion
        self.horaInicio = horaInicio
        self.horaFin = horaFin
        self.tiempoCompleto = tiempoCompleto
        self.idAdministrador = idAdministrador
        self.idUbicacion = idUbicacion


class Caracteristica(Entidad):
    def __init__(self, nombre = '', id=None):
        if id is not None:
            super().__init__(id,["no_attr","idCaracteristica","id_txt"],'idCaracteristica')
            self.idCaracteristica = id
        else:
            super().__init__(0,["no_attr","idCaracteristica","id_txt"], 'idCaracteristica')
            self.idCaracteristica = id
       
        self.nombre = nombre


class Caracteristica_Sede(Entidad):
    def __init__(self, idCaracteristica = '', idSede=''):
        self.idCaracteristica = idCaracteristica
        self.idSede = idSede


class Tipo_Parqueadero(Entidad):
    def __init__(self, nombre = '', id=None):
        if id is not None:
            super().__init__(id,["no_attr","idTipo_Parqueadero","id_txt"],'idTipo_Parqueadero')
            self.idTipo_Parqueadero = id
        else:
            super().__init__(0,["no_attr","idTipo_Parqueadero","id_txt"], 'idTipo_Parqueadero')
            self.idTipo_Parqueadero = id
       
        self.nombre = nombre

class Tarifa(Entidad):
    def __init__(self, valor = '', idSede = '', idTipo_Parqueadero = '', id=None):
        if id is not None:
            super().__init__(id,["no_attr","idTarifa","id_txt"],'idTarifa')
            self.idTarifa = id
        else:
            super().__init__(0,["no_attr","idTarifa","id_txt"], 'idTarifa')
            self.idTarifa = id
       
        self.valor = valor
        self.idSede = idSede
        self.idTipo_Parqueadero = idTipo_Parqueadero


class Ubicacion(Entidad):
    def __init__(self, descripcion = '', fkUbicacion = '', idTipo_Ubicacion = '', id=None):
        if id is not None:
            super().__init__(id,["no_attr","idUbicacion","id_txt"],'idUbicacion')
            self.idUbicacion = id
        else:
            super().__init__(0,["no_attr","idUbicacion","id_txt"], 'idUbicacion')
            self.idUbicacion = id
       
        self.descripcion = descripcion
        self.fkUbicacion = fkUbicacion
        self.idTipo_Ubicacion = idTipo_Ubicacion
