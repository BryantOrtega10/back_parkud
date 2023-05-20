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
    def __init__(self, usuario = '', contrasena = '', rol = '', cambiarContrasena = 1, contrasenaDobleFactor = '', numIntentosFallidos = 0, estado = 'A', token = None, id=None):
        if id is not None:
            super().__init__(id,["no_attr","id","idUsuario","id_txt"],'idUsuario')
            self.idUsuario = id
        else:
            super().__init__(0,["no_attr","id","idUsuario","id_txt"], 'idUsuario')
            self.idUsuario = 0
        
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol
        self.cambiarContrasena = cambiarContrasena
        self.contrasenaDobleFactor = contrasenaDobleFactor
        self.numIntentosFallidos = numIntentosFallidos
        self.estado = estado
        self.token = token

class Cliente(Entidad):
    def __init__(self, nombre = '', apellido = '', correo = '', telefono = '', documentoIdentidad = '', idUsuario = 0, id=None):
        if id is not None:
            super().__init__(id,["no_attr","id","idCliente","id_txt","tarjetas"], 'idCliente')
            self.idCliente = 0
        else:
            super().__init__(0,["no_attr","id","idCliente","id_txt","tarjetas"], 'idCliente')
            self.idCliente = 0

        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
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
