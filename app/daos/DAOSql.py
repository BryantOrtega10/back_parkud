from flask import current_app
from app.daos import DAOGen
from app.models.entidades import Cliente, Tarjeta, Usuario, Configuracion, Sede, Parqueadero
import mysql.connector

class DAOGenericoSQL(DAOGen.DAOGenerico):

    def __init__(self):
        current_conf = current_app
        self.con = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASS'],
            database=current_app.config['MYSQL_BD']
        )
        self.cur = self.con.cursor()

    def create(self,entity):
        try:
            columns,values =  entity.get_attrs()
            columns_str = ", ".join("`{}`".format(column) for column in columns)
            placeholders_str = ", ".join("%s" for _ in values)
            sql = "INSERT INTO {} ({}) VALUES ({})".format(entity.get_name_class().lower(), columns_str, placeholders_str)
            print(sql)
            print(values)
            self.cur.execute(sql, values)
            self.con.commit()
            id_generada = self.cur.lastrowid
            setattr(entity, entity.id_txt, id_generada)
            entity.id = id_generada
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)


    def delete(self,entity):
        try:
            sql = "DELETE FROM {} WHERE {} = %s".format(entity.get_name_class().lower(), entity.id_txt)
            values = (entity.id,)
            print(sql, values)
            self.cur.execute(sql, values)
            if self.cur.rowcount > 0:
                entity = None
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)


    def findall(self, entity):
        try:
            sql = "SELECT * FROM {}".format(entity.get_name_class().lower())
            print(sql)
            self.cur.execute(sql)
            results = self.cur.fetchall()
            results = [ res[1:] + (res[0],) for res in results]
            print(results)
            ent_type = globals()[entity.get_name_class()]
            entities = [ent_type(*res) for res in results]
            return entities
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)


    def read(self, entity):
        try:
            sql = "SELECT * FROM {} WHERE {} = %s".format(entity.get_name_class().lower(),entity.id_txt)
            values = (entity.id,)
            print(sql, values)
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            ent_type = globals()[entity.get_name_class()]
            entity = ent_type(*res) 
            return entity

        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)


    def update(self, entity):
        try:
            columns, values = entity.get_attrs()
            set_clause = ", ".join(f"{column} = %s" for column in columns)
            sql = "UPDATE {} SET {} WHERE {} = %s".format(entity.get_name_class().lower(), set_clause, entity.id_txt)
            query_values = [*values, entity.id]
            print(sql, query_values)
            self.cur.execute(sql, query_values)
            self.con.commit()
            if self.cur.rowcount > 0:
                return True
            else:
                return False
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)


class ClienteDAOSQL(DAOGenericoSQL, DAOGen.ClienteDAO):

    def get_cliente_usuario(self, id_usuario):
        try:
            sql = "SELECT * FROM cliente WHERE idUsuario = %s"
            values = (id_usuario,)
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            if res is None:
                return None
            res = res[1:] + (res[0],)
            return Cliente(*res) 
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

class TarjetaDAOSQL(DAOGenericoSQL, DAOGen.TarjetaDAO):
    def get_tarjetas_cliente(self, cliente_id) :
        try:
            sql = '''SELECT t.*
            FROM tarjeta t
            JOIN cliente c ON t.idCliente = c.idCliente
            WHERE c.idCliente = %s'''
            values = (cliente_id,)
            self.cur.execute(sql,values)
            results = self.cur.fetchall()
            results = [ res[1:] + (res[0],) for res in results]
            sedes = [Sede(*res) for res in results]
            return sedes
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)
class UsuarioDAOSQL(DAOGenericoSQL, DAOGen.UsuarioDAO):

    def get_usuario_correo(self, correo):
        try:
            sql = "SELECT * FROM usuario WHERE correo = %s"
            values = (correo,)
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return Usuario(*res) 
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_usuario_username(self, usuario):
        try:
            sql = "SELECT * FROM usuario WHERE usuario = %s"
            values = (usuario,)
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return Usuario(*res) 
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_usuario_username_password(self, usuario, password):
        try:
            sql = "SELECT * FROM usuario WHERE usuario = %s AND contrasena = %s "
            values = (usuario,password,)
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return Usuario(*res) 
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_usuario_username_doble_factor(self, usuario, doble_factor):
        try:
            sql = "SELECT * FROM usuario WHERE usuario = %s AND contrasenaDobleFactor = %s "
            values = (usuario,doble_factor,)
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return Usuario(*res) 
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)


class ConfiguracionDAOSQL(DAOGenericoSQL, DAOGen.ConfiguracionDAO):
    pass

class AdministradorDAOSQL(DAOGenericoSQL, DAOGen.AdministradorDAO):
    pass

class SedeDAOSQL(DAOGenericoSQL, DAOGen.SedeDAO):
    def filtrar(self, filtro):
        try:
            sql = filtro.toSQL()
            self.cur.execute(sql)
            results = self.cur.fetchall()
            results = [ res[1:] + (res[0],) for res in results]
            sedes = [Sede(*res) for res in results]
            return sedes
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_parqueadero_disponible(self,id_sede, hora_inicio, hora_fin):
        try:
            sql = ''' SELECT p.idParqueadero, p.idSede, p.idTipo_Parqueadero FROM sede s, parqueadero p WHERE
            s.idSede = p.idSede and s.idSede = %s and p.idParqueadero not in(
                    SELECT r.idParqueadero FROM reserva r WHERE 
                    (%s BETWEEN r.horaInicio and r.horaSalida OR
                    %s BETWEEN r.horaInicio and r.horaSalida OR
                    r.horaInicio BETWEEN %s and %s OR
                    r.horaSalida BETWEEN %s and %s) 
                    and r.estado <> 'F'
            )'''
            values = (id_sede,hora_inicio,hora_fin,hora_inicio,hora_fin,hora_inicio,hora_fin,)
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return Parqueadero(*res) 
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

class CaracteristicaDAOSQL(DAOGenericoSQL, DAOGen.CaracteristicaDAO):
    pass

class Caracteristica_SedeDAOSQL(DAOGenericoSQL, DAOGen.Caracteristica_SedeDAO):
   pass


class Tipo_ParqueaderoDAOSQL(DAOGenericoSQL, DAOGen.Tipo_ParqueaderoDAO):
    pass

class TarifaDAOSQL(DAOGenericoSQL, DAOGen.TarifaDAO):
    pass

class UbicacionDAOSQL(DAOGenericoSQL, DAOGen.UbicacionDAO):
    pass

class ReservaDAOSQL(DAOGenericoSQL, DAOGen.Reserva):
    pass