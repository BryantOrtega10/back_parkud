from flask import current_app
from app.daos import DAOGen

from app.models.entidades import Cliente, Tarjeta, Usuario, Configuracion, Ubicacion, Sede, Administrador, Caracteristica, Tipo_Parqueadero, Operario, Tarifa, Parqueadero, Reserva

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
            #return entity
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
            print(results, entity.get_name_class())
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

    def get_total(self):
        try:
            sql = "SELECT COUNT(*) FROM usuario WHERE rol = 'A' "
            self.cur.execute(sql)
            res = self.cur.fetchone()
            if res is None:
                return None

            return res[0]
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_usuario_correo_mod(self, correo, idUsuario):
        try:
            sql = "SELECT * FROM usuario WHERE correo = %s and idUsuario <> %s"
            values = (correo,idUsuario)
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            if res is None:
                return None
            
            res = res[1:] + (res[0],)
            return Usuario(*res) 
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_usuario_username_mod(self, usuario, idUsuario):
        try:
            sql = "SELECT * FROM usuario WHERE usuario = %s  and idUsuario <> %s"
            values = (usuario,idUsuario)
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

    def get_admin_x_usuario(self,idUsuario):
        try:
            sql = "SELECT * FROM administrador WHERE idUsuario = %s"
            values = (idUsuario, )
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            res = res[1:] + (res[0],)
            if res is None:
                return None
            return Administrador(*res) 
        
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def contar_total(self):        
        try:
            sql = "SELECT count(idAdministrador) as cuenta FROM administrador "
            self.cur.execute(sql)
            res = self.cur.fetchall()
            return res[0][0]
        
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_administradores(self, limit=None, offset=None):
        if limit is None and offset is None :
            try:
                sql = "SELECT * FROM administrador ORDER BY CONCAT(nombre,' ',apellido) "
                self.cur.execute(sql)
                res = self.cur.fetchall()
                for r in res:
                    print(r)
                res = [ r[1:] + (r[0],) for r in res]
                if res is None:
                    return None
                
                return [Administrador(*r) for r in res]
            except mysql.connector.Error as error:
                # Capturar la excepción y manejar el error
                print("Se produjo un error durante la ejecución de la consulta:", error)
        elif offset is None:
            try:
                sql = "SELECT * FROM administrador ORDER BY CONCAT(nombre,' ',apellido) LIMIT %s"
                values = (limit)
                self.cur.execute(sql, values)
                res = self.cur.fetchall()
                res = [ r[1:] + (r[0],) for r in res]
                if res is None:
                    return None
                
                return [Administrador(*r) for r in res]
            except mysql.connector.Error as error:
                # Capturar la excepción y manejar el error
                print("Se produjo un error durante la ejecución de la consulta:", error)
        else:
            try:
                sql = "SELECT * FROM administrador ORDER BY CONCAT(nombre,' ',apellido) LIMIT %s OFFSET %s"
                values = (limit, offset)
                self.cur.execute(sql, values)
                res = self.cur.fetchall()
                res = [ r[1:] + (r[0],) for r in res]
                if res is None:
                    return None
                
                return [Administrador(*r) for r in res]
            except mysql.connector.Error as error:
                # Capturar la excepción y manejar el error
                print("Se produjo un error durante la ejecución de la consulta:", error)


class SedeDAOSQL(DAOGenericoSQL, DAOGen.SedeDAO):

    def get_parqueaderos_tipo(self, idSede):
        try:
            sql = '''SELECT p.idParqueadero, tp.nombre from parqueadero p 
                     JOIN tipo_parqueadero tp on tp.idTipo_Parqueadero = p.idTipo_Parqueadero
                     WHERE p.idSede = %s;
                  '''
            values = (idSede, )
            self.cur.execute(sql, values)
            return self.cur.fetchall()
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

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

    def get_cantidad_sedes(self):
        try:
            sql = "SELECT COUNT(*) FROM sede"
            self.cur.execute(sql)
            res = self.cur.fetchone()
            if res is None:
                return None

            return res[0]
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_sedes_activas(self,limit,offset):
        try:
            sql = "SELECT * FROM sede WHERE estado = 'A' ORDER BY idSede LIMIT %s OFFSET %s"
            values = (limit, offset)
            self.cur.execute(sql, values)
            res = self.cur.fetchall()
            res = [ r[1:] + (r[0],) for r in res]
            if res is None:
                return None
            return [Sede(*r) for r in res]
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
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_sede_x_admin(self,idAdministrador):
        try:
            sql = "SELECT * FROM sede WHERE idAdministrador = %s and estado = 'A'"
            values = (idAdministrador, )
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            if res is None:
                return None
            res = res[1:] + (res[0],)
            return Sede(*res) 
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)
            res = res[1:] + (res[0],)
            return Sede(*res) 
            
class CaracteristicaDAOSQL(DAOGenericoSQL, DAOGen.CaracteristicaDAO):

    def get_carac_x_sede(self, idSede):
        try:
            sql = "SELECT caracteristica.* FROM caracteristica JOIN caracteristica_sede ON caracteristica_sede.idCaracteristica = caracteristica.idCaracteristica WHERE caracteristica_sede.idSede = %s "
            values = (idSede, )
            self.cur.execute(sql, values)
            res = self.cur.fetchall()
            res = [ r[1:] + (r[0],) for r in res]
            if res is None:
                return None
            return [Caracteristica(*r) for r in res]

        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

class Caracteristica_SedeDAOSQL(DAOGenericoSQL, DAOGen.Caracteristica_SedeDAO):
    def eliminar_x_sede(self, idSede):
        try:
            sql = "DELETE FROM caracteristica_sede WHERE idSede = %s "
            values = (idSede, )
            self.cur.execute(sql, values)
            return True

        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)


class Tipo_ParqueaderoDAOSQL(DAOGenericoSQL, DAOGen.Tipo_ParqueaderoDAO):
    pass

class TarifaDAOSQL(DAOGenericoSQL, DAOGen.TarifaDAO):

    def get_tarifa_x_sede_x_tpParq(self, idSede, idTipo_Parqueadero):
        try:
            sql = "SELECT * FROM tarifa WHERE idSede = %s and idTipo_Parqueadero = %s "
            values = (idSede, idTipo_Parqueadero, )
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            if res is None:
                return None
            return Tarifa(*res)

        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_tarifa_x_sede(self, idSede):
        try:
            sql = "SELECT * FROM tarifa WHERE idSede = %s "
            values = (idSede, )
            self.cur.execute(sql, values)
            res = self.cur.fetchall()
            res = [ r[1:] + (r[0],) for r in res]
            if res is None:
                return None
            return [Tarifa(*r) for r in res]

        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)


class ParqueaderoDAOSQL(DAOGenericoSQL, DAOGen.ParqueaderoDAO):
    
    def get_cuenta_parq_x_tipoParq_x_sede(self,idSede):
        try:
            sql = "SELECT count(*),idTipo_Parqueadero FROM parqueadero WHERE idSede = %s GROUP BY idTipo_Parqueadero"
            values = (idSede,)
            self.cur.execute(sql, values)
            res = self.cur.fetchall()
            res = [{"cuenta": r[0], "idTipo_Parqueadero": r[1] } for r in res]
            return res
        
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

class OperarioDAOSQL(DAOGenericoSQL, DAOGen.OperarioDAO):
    def get_operario_x_usuario(self, idUsuario):
        try:
            sql = "SELECT * FROM operario WHERE idUsuario = %s "
            values = (idUsuario, )
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            res = res[1:] + (res[0],)
            if res is None:
                return None
            return Operario(*res) 

        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)
    
    def get_operarios_x_sede(self, idSede):
        try:
            sql = "SELECT * FROM operario WHERE idSede = %s "
            values = (idSede, )
            self.cur.execute(sql, values)
            res = self.cur.fetchall()
            res = [ r[1:] + (r[0],) for r in res]
            if res is None:
                return None
            return [Operario(*r) for r in res]

        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)
    

class UbicacionDAOSQL(DAOGenericoSQL, DAOGen.UbicacionDAO):
    def get_regionales(self):
        try:
            sql = "SELECT * FROM ubicacion WHERE fkUbicacion is NULL "
            self.cur.execute(sql)
            res = self.cur.fetchall()
            res = [ r[1:] + (r[0],) for r in res]
            if res is None:
                return None
            
            return [Ubicacion(*r) for r in res]
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_ubicacion_regional(self,idregional):
        try:
            sql = "SELECT * FROM ubicacion WHERE fkUbicacion = %s "
            values = (idregional,)
            self.cur.execute(sql, values)
            res = self.cur.fetchall()
            res = [ r[1:] + (r[0],) for r in res]
            if res is None:
                return None
            
            return [Ubicacion(*r) for r in res]
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

class ReservaDAOSQL(DAOGenericoSQL, DAOGen.ReservaDAO):
    
    def get_datos(self,idReserva):
        try:
            sql = '''SELECT r.idReserva, r.horaInicio, r.horaSalida, p.idParqueadero, 
                    tp.nombre, c.nombre, c.apellido, r.estado FROM reserva r
                    JOIN parqueadero p ON p.idParqueadero = r.idParqueadero
                    JOIN tipo_parqueadero tp ON tp.idTipo_Parqueadero = p.idTipo_Parqueadero
                    JOIN tarjeta t ON t.idTarjeta = r.idTarjeta
                    JOIN cliente c ON c.idCliente = t.idCliente
                    WHERE r.idReserva = %s;'''
            
            values = (idReserva,)
            self.cur.execute(sql, values)
            res = self.cur.fetchone()
            return res
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)

    def get_estado(self,dia,idParqueadero,idSede):
        try:
            sql = '''SELECT r.idReserva, r.horaInicio, r.horaSalida FROM reserva r
                    WHERE (DATE(r.horaInicio) = %s or DATE(r.horaSalida) = %s) and r.idParqueadero = %s and r.idSede = %s;'''
            
            values = (dia,dia,idParqueadero,idSede,)
            self.cur.execute(sql, values)
            return self.cur.fetchall()
        except mysql.connector.Error as error:
            # Capturar la excepción y manejar el error
            print("Se produjo un error durante la ejecución de la consulta:", error)