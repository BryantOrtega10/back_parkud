from flask import Blueprint, request, jsonify, current_app
from http import HTTPStatus
from app.funciones.token_jwt import token_required, validar_usuario_token,validar_superadmin_token, validar_admin_token
from app.models.entidades import Usuario, Cliente, Administrador, Tarjeta, Configuracion, Operario
from app.daos.DAOFactory import DAOFactorySQL
import re
import random
import string
import smtplib, ssl
from email.mime.text import MIMEText
import hashlib
import jwt
from datetime import datetime, timedelta


usuario_bp = Blueprint('usuario', __name__)

@token_required
@usuario_bp.route('/tarjetas', methods=["GET"])
def obtener_tarjetas():
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    cliente = DAOFactorySQL.get_cliente_dao().get_cliente_usuario(usuario.idUsuario)
    if cliente is None:
        return jsonify({"success": False, "error" : "El usuario no es cliente"}) , HTTPStatus.BAD_REQUEST

    
    tarjetas = DAOFactorySQL.get_tarjeta_dao().get_tarjetas_cliente(cliente.idCliente)
    for tarjeta in tarjetas:
        print(tarjeta)
        
    tarjetas = [{"idTarjeta" : tarjeta.idTarjeta, "tarjeta": ("XXXX XXXX XXXX " + tarjeta.numero[12:16])} for tarjeta in tarjetas]

    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "tarjetas": tarjetas}) , HTTPStatus.OK

@token_required
@usuario_bp.route('/admins', methods=['GET'])
@usuario_bp.route('/admins/<int:limit>', methods=['GET'])
@usuario_bp.route('/admins/<int:limit>/<int:offset>', methods=['GET'])
def lista_administradores(limit = 10, offset = 0):
    usuario = validar_superadmin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    cuenta = DAOFactorySQL.get_administrador_dao().contar_total()
    admins = DAOFactorySQL.get_administrador_dao().get_administradores(limit, offset)
    admins = [{"idAdministrador": admin.idAdministrador, "nombre" : admin.nombre + " " + admin.apellido} for admin in admins]

    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "admins" : admins, "cuenta" : cuenta}) , HTTPStatus.OK



@token_required
@usuario_bp.route('/admins/todos', methods=['GET'])
def obtener_administradores():
    usuario = validar_superadmin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST

    admins = DAOFactorySQL.get_administrador_dao().get_administradores()
    admins = [{"idAdministrador": admin.idAdministrador, "nombre" : admin.nombre + " " + admin.apellido} for admin in admins]
    return jsonify({"success": True, "message": "Administradores consultados correctamente", "admins" : admins}), HTTPStatus.OK


@token_required
@usuario_bp.route('/operario/<int:id>', methods=["GET"])
def obtener_operario(id):
    usuario = validar_admin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    operario = Operario(id=id)
    operario = DAOFactorySQL.get_operario_dao().read(operario)

    usuario_op = Usuario(id=operario.idUsuario)
    usuario_op = DAOFactorySQL.get_usuario_dao().read(usuario_op)


    return jsonify({"success": True, "message" : "Consulta realizada con éxito", "operario": {
        "idOperario": operario.idOperario,
        "nombre" : operario.nombre,
        "apellido" : operario.apellido,
        "documentoIdentidad" : operario.documentoIdentidad,
        "usuario" : usuario_op.usuario,
        "correo" : usuario_op.correo
    }}) , HTTPStatus.OK

@token_required
@usuario_bp.route('/operario/<int:id>', methods=["PUT"])
def modificar_operario(id):
    usuario_1 = validar_admin_token()
    if not isinstance(usuario_1, Usuario):
        return usuario_1, HTTPStatus.BAD_REQUEST
    
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios_operario(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    req_nombre = json_recibido["nombre"]
    req_apellido = json_recibido["apellido"]
    req_documentoIdentidad = json_recibido["documentoIdentidad"]
    req_idSede = json_recibido["idSede"]
    req_usuario = json_recibido["usuario"]
    req_correo = json_recibido["correo"]

    operario = Operario(id=id)
    operario = DAOFactorySQL.get_operario_dao().read(operario)

    #Verificar número de caracteres del usuario. 
    if len(req_usuario.strip()) > 8 or len(req_usuario.strip()) < 5:
        return jsonify({"success": False, "error" : "El usuario debe contener entre 5 a 8 caracteres"}) , HTTPStatus.BAD_REQUEST
    
    #Verificar que el usuario no exista en BD. 
    usuario = DAOFactorySQL.get_usuario_dao().get_usuario_username_mod(req_usuario, operario.idUsuario)
    if usuario is not None:
        return jsonify({"success": False, "error" : "Este nombre de usuario ya se encuentra registrado utilice otro"}) , HTTPStatus.BAD_REQUEST

    #Verificar que el correo sea válido y no exista en BD. 
    error = validar_correo(req_correo)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    usuario_c = DAOFactorySQL.get_usuario_dao().get_usuario_correo_mod(req_correo, operario.idUsuario)
    if usuario_c is not None:
        return jsonify({"success": False, "error" : "Este correo ya se encuentra registrado utilice otro"}) , HTTPStatus.BAD_REQUEST

    usuario_op = Usuario(id=operario.idUsuario)
    usuario_op = DAOFactorySQL.get_usuario_dao().read(usuario_op)    
    operario.nombre = req_nombre
    operario.apellido = req_apellido
    operario.documentoIdentidad = req_documentoIdentidad
    operario.idSede = req_idSede
    usuario_op.usuario = req_usuario
    usuario_op.correo = req_correo

    DAOFactorySQL.get_operario_dao().update(operario)
    DAOFactorySQL.get_usuario_dao().update(usuario_op)

    return jsonify({"success": True, "message" : "Se ha modificado el operario con éxito", "operario": {
        "idOperario": operario.idOperario,
        "nombre" : operario.nombre,
        "apellido" : operario.apellido,
        "documentoIdentidad" : operario.documentoIdentidad,
        "usuario" : usuario_op.usuario,
        "correo" : usuario_op.correo
    }}) , HTTPStatus.OK


@token_required
@usuario_bp.route('/operario', methods=['POST'])
def agregar_operario():
    usuario = validar_admin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios_operario(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    #los datos no estan vacíos, se obtienen en variables para mayor comodidad
    req_nombre = json_recibido["nombre"]
    req_apellido = json_recibido["apellido"]
    req_documentoIdentidad = json_recibido["documentoIdentidad"]
    req_idSede = json_recibido["idSede"]
    req_usuario = json_recibido["usuario"]
    req_correo = json_recibido["correo"]

    #Verificar número de caracteres del usuario. 
    if len(req_usuario.strip()) > 8 or len(req_usuario.strip()) < 5:
        return jsonify({"success": False, "error" : "El usuario debe contener entre 5 a 8 caracteres"}) , HTTPStatus.BAD_REQUEST
    
    #Verificar que el usuario no exista en BD. 
    usuario = DAOFactorySQL.get_usuario_dao().get_usuario_username(req_usuario)
    if usuario is not None:
        return jsonify({"success": False, "error" : "Este nombre de usuario ya se encuentra registrado utilice otro"}) , HTTPStatus.BAD_REQUEST

    #Verificar que el correo sea válido y no exista en BD. 
    error = validar_correo(req_correo)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    usuario_c = DAOFactorySQL.get_usuario_dao().get_usuario_correo(req_correo)
    if usuario_c is not None:
        return jsonify({"success": False, "error" : "Este correo ya se encuentra registrado utilice otro"}) , HTTPStatus.BAD_REQUEST
    
    contra_rand = generar_contraena_aleatoria()
    contra_rand_enc = hashlib.md5(contra_rand.encode()).hexdigest()
    usuario = Usuario(usuario=req_usuario, contrasena=contra_rand_enc, correo = req_correo, rol='O')
    DAOFactorySQL.get_usuario_dao().create(usuario)

    operario = Operario(nombre = req_nombre, apellido = req_apellido, documentoIdentidad = req_documentoIdentidad, idSede=req_idSede, idUsuario = usuario.idUsuario)
    DAOFactorySQL.get_operario_dao().create(operario)
   
    #enviar correo
    msg = MIMEText(f'<h1>Bienvenido {req_nombre} a ParkUD</h1>'\
                   f'<p>Te damos la bienvenida a ParkUD, recuerda que debes iniciar sesión con la siguiente contraseña <b>{contra_rand}</b></p>'\
                   f'<p>Cordialmente <br> ParkUD Colombia</p>'                   
                   , 'html')

    msg['Subject'] = 'Se registro satisfactoriamente en ParkUD!'
    msg['From'] = current_app.config['MAIL']
    msg['To'] = req_correo

    
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
        server.login(current_app.config['MAIL'], current_app.config['MAIL_PASS'])
        server.sendmail(current_app.config['MAIL'], req_correo, msg.as_string())

    return jsonify({"success": True, "message": f"Usuario registrado correctamente"}), HTTPStatus.OK



@token_required
@usuario_bp.route('/agregar_administrador', methods=['POST'])
def agregar_administrador():
    usuario = validar_superadmin_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios_admin(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    #los datos no estan vacíos, se obtienen en variables para mayor comodidad
    req_nombre = json_recibido["nombre"]
    req_apellido = json_recibido["apellido"]
    req_correo = json_recibido["correo"]
    req_documento_identidad = json_recibido["documentoIdentidad"]
    req_usuario = json_recibido["usuario"]

    #Verificar número de caracteres del usuario. 
    if len(req_usuario.strip()) > 8 or len(req_usuario.strip()) < 5:
        return jsonify({"success": False, "error" : "El usuario debe contener entre 5 a 8 caracteres"}) , HTTPStatus.BAD_REQUEST
    
    #Verificar que el usuario no exista en BD. 
    usuario = DAOFactorySQL.get_usuario_dao().get_usuario_username(req_usuario)
    if usuario is not None:
        return jsonify({"success": False, "error" : "Este nombre de usuario ya se encuentra registrado utilice otro"}) , HTTPStatus.BAD_REQUEST

    #Verificar que el correo sea válido y no exista en BD. 
    error = validar_correo(req_correo)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    usuario_c = DAOFactorySQL.get_usuario_dao().get_usuario_correo(req_correo)
    if usuario_c is not None:
        return jsonify({"success": False, "error" : "Este correo ya se encuentra registrado utilice otro"}) , HTTPStatus.BAD_REQUEST
    
    contra_rand = generar_contraena_aleatoria()
    contra_rand_enc = hashlib.md5(contra_rand.encode()).hexdigest()
    usuario = Usuario(usuario=req_usuario, contrasena=contra_rand_enc, correo = req_correo, rol='A')
    DAOFactorySQL.get_usuario_dao().create(usuario)

    administrador = Administrador(nombre = req_nombre, apellido = req_apellido, documentoIdentidad = req_documento_identidad, idUsuario = usuario.idUsuario)
    DAOFactorySQL.get_administrador_dao().create(administrador)
   
    #enviar correo
    msg = MIMEText(f'<h1>Bienvenido {req_nombre} a ParkUD</h1>'\
                   f'<p>Te damos la bienvenida a ParkUD, recuerda que debes iniciar sesión con la siguiente contraseña <b>{contra_rand}</b></p>'\
                   f'<p>Cordialmente <br> ParkUD Colombia</p>'                   
                   , 'html')

    msg['Subject'] = 'Se registro satisfactoriamente en ParkUD!'
    msg['From'] = current_app.config['MAIL']
    msg['To'] = req_correo

    
    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
        server.login(current_app.config['MAIL'], current_app.config['MAIL_PASS'])
        server.sendmail(current_app.config['MAIL'], req_correo, msg.as_string())

    return jsonify({"success": True, "message": f"Usuario registrado correctamente"}), HTTPStatus.OK




@token_required
@usuario_bp.route('/validar_cambio_contrasena', methods=["GET"])
def ruta_general():
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    
    return jsonify({"success": True, "message" : "El usuario ya cambio de contraseña, perfecto"}) , HTTPStatus.OK


@token_required
@usuario_bp.route('/obtener_usuario', methods=["GET"])
def obtener_usuario():
    usuario = validar_usuario_token()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    if usuario.rol == 'C':
        cliente = DAOFactorySQL.get_cliente_dao().get_cliente_usuario(usuario.idUsuario)

        return jsonify({"success": True, 
                        "user":{"idUsuario": usuario.idUsuario, "nombre": cliente.nombre, 
                            "apellido": cliente.apellido, "correo": usuario.correo, "rol": usuario.rol}
                        }) , HTTPStatus.OK
    elif usuario.rol == 'A':
        administrador = DAOFactorySQL.get_administrador_dao().get_admin_x_usuario(usuario.idUsuario)

        return jsonify({"success": True, 
                        "user":{"idUsuario": usuario.idUsuario, "nombre": administrador.nombre, 
                            "apellido": administrador.apellido, "correo": usuario.correo, "rol": usuario.rol}
                        }) , HTTPStatus.OK
    elif usuario.rol == 'O':
        operario = DAOFactorySQL.get_operario_dao().get_operario_x_usuario(usuario.idUsuario)

        return jsonify({"success": True, 
                        "user":{"idUsuario": usuario.idUsuario, "nombre": operario.nombre, 
                            "apellido": operario.apellido, "correo": usuario.correo, "rol": usuario.rol}
                        }) , HTTPStatus.OK
    elif usuario.rol == 'S':
        return jsonify({"success": True, "message": f"Ha iniciado sesión correctamente",
                        "user":{"idUsuario": usuario.idUsuario, "correo": usuario.correo, "nombre": "SuperAdministrador", "apellido" : "ParkUD" , "rol": usuario.rol}}), HTTPStatus.OK
        



@token_required
@usuario_bp.route('/cambiar_contrasena', methods=["PUT"])
def cambiar_contrasena():
    usuario = validar_usuario_token_sin_cambio()
    if not isinstance(usuario, Usuario):
        return usuario, HTTPStatus.BAD_REQUEST
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios_cambiar_contra(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    #los datos no estan vacíos, se obtienen en variables para mayor comodidad
    req_nueva_contrasena = json_recibido["nueva_contrasena"]
    if not validar_contrasena(req_nueva_contrasena):
        return jsonify({"success": False, "error" : "La contraseña debe contener mayusculas, minusculas y al menos un número, con una longitud entre 5 a 8 caracteres"}) , HTTPStatus.BAD_REQUEST
    
    req_nueva_contrasena = hashlib.md5(req_nueva_contrasena.encode()).hexdigest()
    usuario.contrasena = req_nueva_contrasena
    usuario.cambiarContrasena = 0
    usuario =  DAOFactorySQL.get_usuario_dao().update(usuario)

    return jsonify({"success": True, "message" : "La contraseña ha sido cambiada exitosamente"}) , HTTPStatus.OK

@usuario_bp.route('/login/<int:id>', methods=["POST"])
def doble_factor(id):
    
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios_doble_factor(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    usuario = Usuario(id=id)
    usuario = DAOFactorySQL.get_usuario_dao().read(usuario)

    
    #los datos no estan vacíos, se obtienen en variables para mayor comodidad
    req_doble_factor = json_recibido["doble_factor"]
    req_doble_factor = hashlib.md5(req_doble_factor.encode()).hexdigest()
    usuario_doble_factor = DAOFactorySQL.get_usuario_dao().get_usuario_username_doble_factor(usuario.usuario, req_doble_factor)
    
    if usuario_doble_factor is None:
        return jsonify({"success": False, "error" : "La contraseña de doble factor no coincide intente nuevamente"}) , HTTPStatus.BAD_REQUEST

    #expiracion = datetime.utcnow() + timedelta(minutes=60)
    token = jwt.encode({'idUsuario': usuario_doble_factor.idUsuario}, current_app.config['JWT_SECRET_KEY'])
    usuario_doble_factor.token = token
    DAOFactorySQL.get_usuario_dao().update(usuario_doble_factor)
    
    if usuario_doble_factor.cambiarContrasena == 1:
        return jsonify({"success": True, "message" : "¡Bienvenido!, Debes cambiar la contraseña para continuar", "token": token,
                        "cambiarContrasena": usuario_doble_factor.cambiarContrasena}) , HTTPStatus.OK
    
    return jsonify({"success": True, "message" : "¡Bienvenido!", "token": token,"cambiarContrasena": usuario_doble_factor.cambiarContrasena}) , HTTPStatus.OK

@usuario_bp.route('/login', methods=['POST'])
def login():
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios_login(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    #los datos no estan vacíos, se obtienen en variables para mayor comodidad
    req_usuario = json_recibido["usuario"]
    req_contrasena = json_recibido["contrasena"]
    req_contrasena = hashlib.md5(req_contrasena.encode()).hexdigest()
    #Validar datos de inicio de sesion
    #Verificar que el usuario exista en BD. 
    usuario = DAOFactorySQL.get_usuario_dao().get_usuario_username(req_usuario)
    if usuario is None:
        return jsonify({"success": False, "error" : "El nombre de usuario no se encuentra registrado"}) , HTTPStatus.BAD_REQUEST

    if usuario.estado == 'B':
        return jsonify({"success": False, "error" : "El usuario se encuentra bloqueado comuniquese con el administrado de PARKUD"}) , HTTPStatus.BAD_REQUEST

    usuario_login = DAOFactorySQL.get_usuario_dao().get_usuario_username_password(req_usuario, req_contrasena)

    if usuario_login is None and usuario.rol != 'S':
        usuario.numIntentosFallidos += 1
        DAOFactorySQL.get_usuario_dao().update(usuario)

        max_Intentos = parse_configuration("N_FAI")
        if(usuario.numIntentosFallidos >= max_Intentos):
            usuario.estado = 'B'
            DAOFactorySQL.get_usuario_dao().update(usuario)
            correo_super_admin = parse_configuration("C_ADM")
            msg = MIMEText(f'<h1>Usuario Bloqueado</h1>'\
                        f'<p>Se informa de un bloqueo del usuario <b>{req_usuario}</b>, dado que excedio el '\
                        f'número máximo de intentos de ingreso fallidos en la aplicación, le recordamos '\
                        f'que usted es el único en la capacidad para desbloquear esta cuenta</p>'\
                        f'<p>Cordialmente <br> ParkUD Colombia</p>'                   
                        , 'html')

            msg['Subject'] = 'Usuario Bloqueado en ParkUD'
            msg['From'] = 'info@parkud.com'
            msg['To'] = correo_super_admin

            contexto = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
                server.login(current_app.config['MAIL'], current_app.config['MAIL_PASS'])
                server.sendmail(current_app.config['MAIL'], correo_super_admin, msg.as_string())
            return jsonify({"success": False, 
                    "error" : f"Contraseña incorrecta, ha excedido el número de intentos fallidos, por lo tanto su cuenta ha sido bloqueada comuniquese con el administrado de PARKUD"
                    }) , HTTPStatus.BAD_REQUEST
        
        return jsonify({"success": False, "error" : f"Contraseña incorrecta, número de intentos fallidos: {usuario.numIntentosFallidos}", "numIntentosFallidos": usuario.numIntentosFallidos}) , HTTPStatus.BAD_REQUEST
    elif usuario_login is None and usuario.rol == 'S':
        return jsonify({"success": False, "error" : f"Contraseña incorrecta"}) , HTTPStatus.BAD_REQUEST
    
    usuario_login.numIntentosFallidos = 0
    if usuario_login.rol == 'C':
        cliente = DAOFactorySQL.get_cliente_dao().get_cliente_usuario(usuario_login.idUsuario);
        contra_rand = generar_contraena_aleatoria()
        contra_rand_enc = hashlib.md5(contra_rand.encode()).hexdigest()
        usuario_login.contrasenaDobleFactor = contra_rand_enc
        
        DAOFactorySQL.get_usuario_dao().update(usuario_login)


        msg = MIMEText(f'<h1>Contraseña doble factor</h1>'\
                    f'<p>¡Hola <b>{req_usuario}</b>!, se ha generado la contraseña de doble factor:<br><b>{contra_rand}</b><br>'\
                    f'<br>Ingresala para poder continuar</p>'\
                    f'<p>Cordialmente <br> ParkUD Colombia</p>'                   
                    , 'html')

        msg['Subject'] = 'Contraseña doble factor ParkUD'
        msg['From'] = 'info@parkud.com'
        msg['To'] = usuario_login.correo

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
            server.login(current_app.config['MAIL'], current_app.config['MAIL_PASS'])
            server.sendmail(current_app.config['MAIL'], usuario_login.correo, msg.as_string())

        
        return jsonify({"success": True, "message": f"Ha iniciado sesión correctamente, se ha enviado la contraseña de doble fator a su correo",
                        "user":{"idUsuario": usuario_login.idUsuario, "nombre": cliente.nombre, 
                        "apellido": cliente.apellido, "correo": usuario_login.correo, "rol": usuario_login.rol}}), HTTPStatus.OK
    elif usuario_login.rol == 'A':
        administrador = DAOFactorySQL.get_administrador_dao().get_admin_x_usuario(usuario_login.idUsuario)
        contra_rand = generar_contraena_aleatoria()
        contra_rand_enc = hashlib.md5(contra_rand.encode()).hexdigest()
        usuario_login.contrasenaDobleFactor = contra_rand_enc
        
        DAOFactorySQL.get_usuario_dao().update(usuario_login)


        msg = MIMEText(f'<h1>Contraseña doble factor</h1>'\
                    f'<p>¡Hola <b>{req_usuario}</b>!, se ha generado la contraseña de doble factor:<br><b>{contra_rand}</b><br>'\
                    f'<br>Ingresala para poder continuar</p>'\
                    f'<p>Cordialmente <br> ParkUD Colombia</p>'                   
                    , 'html')

        msg['Subject'] = 'Contraseña doble factor ParkUD'
        msg['From'] = 'info@parkud.com'
        msg['To'] = usuario_login.correo

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
            server.login(current_app.config['MAIL'], current_app.config['MAIL_PASS'])
            server.sendmail(current_app.config['MAIL'], usuario_login.correo, msg.as_string())

        
        return jsonify({"success": True, "message": f"Ha iniciado sesión correctamente, se ha enviado la contraseña de doble fator a su correo",
                        "user":{"idUsuario": usuario_login.idUsuario, "nombre": administrador.nombre, 
                        "apellido": administrador.apellido, "correo": usuario_login.correo, "rol": usuario_login.rol}}), HTTPStatus.OK
    
    elif usuario_login.rol == 'O':
        operario = DAOFactorySQL.get_operario_dao().get_operario_x_usuario(usuario_login.idUsuario)
        contra_rand = generar_contraena_aleatoria()
        contra_rand_enc = hashlib.md5(contra_rand.encode()).hexdigest()
        usuario_login.contrasenaDobleFactor = contra_rand_enc
        
        DAOFactorySQL.get_usuario_dao().update(usuario_login)


        msg = MIMEText(f'<h1>Contraseña doble factor</h1>'\
                    f'<p>¡Hola <b>{req_usuario}</b>!, se ha generado la contraseña de doble factor:<br><b>{contra_rand}</b><br>'\
                    f'<br>Ingresala para poder continuar</p>'\
                    f'<p>Cordialmente <br> ParkUD Colombia</p>'                   
                    , 'html')

        msg['Subject'] = 'Contraseña doble factor ParkUD'
        msg['From'] = 'info@parkud.com'
        msg['To'] = usuario_login.correo

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
            server.login(current_app.config['MAIL'], current_app.config['MAIL_PASS'])
            server.sendmail(current_app.config['MAIL'], usuario_login.correo, msg.as_string())

        
        return jsonify({"success": True, "message": f"Ha iniciado sesión correctamente, se ha enviado la contraseña de doble fator a su correo",
                        "user":{"idUsuario": usuario_login.idUsuario, "nombre": operario.nombre, 
                        "apellido": operario.apellido, "correo": usuario_login.correo, "rol": usuario_login.rol}}), HTTPStatus.OK
    
    elif usuario_login.rol == 'S':
        contra_rand = generar_contraena_aleatoria()
        contra_rand_enc = hashlib.md5(contra_rand.encode()).hexdigest()
        usuario_login.contrasenaDobleFactor = contra_rand_enc
        
        DAOFactorySQL.get_usuario_dao().update(usuario_login)


        msg = MIMEText(f'<h1>Contraseña doble factor</h1>'\
                    f'<p>¡Hola <b>{req_usuario}</b>!, se ha generado la contraseña de doble factor:<br><b>{contra_rand}</b><br>'\
                    f'<br>Ingresala para poder continuar</p>'\
                    f'<p>Cordialmente <br> ParkUD Colombia</p>'                   
                    , 'html')

        msg['Subject'] = 'Contraseña doble factor ParkUD'
        msg['From'] = 'info@parkud.com'
        msg['To'] = usuario_login.correo

        contexto = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
            server.login(current_app.config['MAIL'], current_app.config['MAIL_PASS'])
            server.sendmail(current_app.config['MAIL'], usuario_login.correo, msg.as_string())

        return jsonify({"success": True, "message": f"Ha iniciado sesión correctamente",
                        "user":{"idUsuario": usuario_login.idUsuario, "correo": usuario_login.correo, "nombre": "SuperAdministrador", "apellido" : "ParkUD" , "rol": usuario_login.rol}}), HTTPStatus.OK

@usuario_bp.route('/registro', methods=['POST'])
def create():
    json_recibido = request.get_json()
    #Verificar que los campos obligatorios no estén vacíos. 
    error = verificar_datos_vacios(json_recibido)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    #los datos no estan vacíos, se obtienen en variables para mayor comodidad
    req_nombre = json_recibido["nombre"]
    req_apellido = json_recibido["apellido"]
    req_correo = json_recibido["correo"]
    req_telefono = json_recibido["telefono"]
    req_documento_identidad = json_recibido["documentoIdentidad"]
    req_usuario = json_recibido["usuario"]
    req_nombre_tarjeta = json_recibido["nombreTarjeta"]
    req_tipo = json_recibido["tipo"]
    req_numero = json_recibido["numero"]
    req_fecha_expiracion = json_recibido["fechaExpiracion"]
    req_csv = json_recibido["csv"]

    #Verificar número de caracteres del usuario. 
    if len(req_usuario.strip()) > 8 or len(req_usuario.strip()) < 5:
        return jsonify({"success": False, "error" : "El usuario debe contener entre 5 a 8 caracteres"}) , HTTPStatus.BAD_REQUEST
    #Verificar que el usuario no exista en BD. 
    usuario = DAOFactorySQL.get_usuario_dao().get_usuario_username(req_usuario)
    if usuario is not None:
        return jsonify({"success": False, "error" : "Este nombre de usuario ya se encuentra registrado utilice otro"}) , HTTPStatus.BAD_REQUEST

    #Verificar que el correo sea válido y no exista en BD. 
    error = validar_correo(req_correo)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST
    
    usuario_c = DAOFactorySQL.get_usuario_dao().get_usuario_correo(req_correo)
    if usuario_c is not None:
        return jsonify({"success": False, "error" : "Este correo ya se encuentra registrado utilice otro"}) , HTTPStatus.BAD_REQUEST
    
    #Verificar que la tarjeta sea válida. 
    error = validar_tarjeta(req_numero)
    if error is not None:
        return error, HTTPStatus.BAD_REQUEST

    contra_rand = generar_contraena_aleatoria()
    contra_rand_enc = hashlib.md5(contra_rand.encode()).hexdigest()
    usuario = Usuario(usuario=req_usuario, contrasena=contra_rand_enc, correo = req_correo, rol='C')
    DAOFactorySQL.get_usuario_dao().create(usuario)

    #usuario.idUsuario = 1
    cliente = Cliente(nombre = req_nombre, apellido = req_apellido, 
                      telefono = req_telefono, 
                      documentoIdentidad = req_documento_identidad, idUsuario = usuario.idUsuario)
    DAOFactorySQL.get_cliente_dao().create(cliente)
    #cliente.idCliente = 1
    tarjeta = Tarjeta(nombre = req_nombre_tarjeta,tipo = req_tipo, numero = req_numero, 
                      fechaExpiracion = req_fecha_expiracion, csv = req_csv, 
                      idCliente = cliente.idCliente)
    DAOFactorySQL.get_tarjeta_dao().create(tarjeta)

    #enviar correo
    msg = MIMEText(f'<h1>Bienvenido {req_nombre} a ParkUD</h1>'\
                   f'<p>Te damos la bienvenida a ParkUD, recuerda que debes iniciar sesión con la siguiente contraseña <b>{contra_rand}</b></p>'\
                   f'<p>Cordialmente <br> ParkUD Colombia</p>'                   
                   , 'html')

    msg['Subject'] = 'Se registro satisfactoriamente en ParkUD!'
    msg['From'] = 'info@parkud.com'
    msg['To'] = req_correo

    contexto = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=contexto) as server:
        server.login(current_app.config['MAIL'], current_app.config['MAIL_PASS'])
        server.sendmail(current_app.config['MAIL'], req_correo, msg.as_string())

    return jsonify({"success": True, "message": f"Usuario registrado correctamente"}), HTTPStatus.OK



def verificar_datos_vacios_cambiar_contra(json_recibido):
    if 'nueva_contrasena' not in json_recibido or len(json_recibido['nueva_contrasena'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo nueva_contrasena vacio"})
    return None

def verificar_datos_vacios_doble_factor(json_recibido):
    if 'doble_factor' not in json_recibido or len(json_recibido['doble_factor'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo doble_factor vacio"})
    return None
    
def verificar_datos_vacios_login(json_recibido):

    if 'usuario' not in json_recibido or len(json_recibido['usuario'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo usuario vacio"})
    
    if 'contrasena' not in json_recibido or len(json_recibido['contrasena'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo contrasena vacio"})
    
    return None

def verificar_datos_vacios(json_recibido):
    if 'nombre' not in json_recibido or len(json_recibido['nombre'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo nombre vacio"})
    
    if 'apellido' not in json_recibido or len(json_recibido['apellido'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo apellido vacio"})
    
    if 'correo' not in json_recibido or len(json_recibido['correo'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo correo vacio"})
    
    if 'telefono' not in json_recibido or len(json_recibido['telefono'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo teléfono vacio"})
    
    if 'documentoIdentidad' not in json_recibido or len(json_recibido['documentoIdentidad'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo documento de identidad vacio"})
    
    if 'usuario' not in json_recibido or len(json_recibido['usuario'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo usuario vacio"})
    
    if 'nombreTarjeta' not in json_recibido or len(json_recibido['nombreTarjeta'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo nombre de la tarjeta vacio"})
    
    if 'tipo' not in json_recibido or len(json_recibido['tipo'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo tipo vacio"})
    
    if 'numero' not in json_recibido or len(json_recibido['numero'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo numero vacio"})

    if 'fechaExpiracion' not in json_recibido or len(json_recibido['fechaExpiracion'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo fecha de expiracion vacio"})
    
    if 'csv' not in json_recibido or len(json_recibido['csv'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo csv vacio"})
    
    return None

def validar_correo(correo):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, correo):
        return None
    else:
        return jsonify({"success": False, "error" : "Correo invalido"})
    
def validar_tarjeta(num_tarjeta):
    # Convertir el número de la tarjeta a una lista de dígitos
    digitos = [int(d) for d in str(num_tarjeta)]

    # Multiplicar por 2 cada segundo dígito, empezando desde el final
    for i in range(len(digitos)-2, -1, -2):
        digitos[i] *= 2

    # Sumar los dígitos individuales de cada número de dos dígitos
    digitos = [d // 10 + d % 10 if d >= 10 else d for d in digitos]

    # Sumar todos los dígitos
    suma_digitos = sum(digitos)

    # Si la suma de dígitos es divisible por 10, entonces la tarjeta es válida
    if suma_digitos % 10 == 0:
        return None
    else:
        return jsonify({"success": False, "error" : "Tarjeta invalida"})
    
def generar_contraena_aleatoria():
    longitud = random.randint(5, 8)  # Genera una longitud aleatoria de 5 a 8 caracteres
    caracteres = string.ascii_letters + string.digits # Crea una lista de caracteres permitidos
    return ''.join(random.choice(caracteres) for i in range(longitud))  # Genera el string aleatorio

def parse_configuration(id_conf):
    configuracion = Configuracion(id=id_conf)
    configuracion = DAOFactorySQL.get_configuracion_dao().read(configuracion)
    print(configuracion, id_conf)
    if configuracion.tipoDeDato == "int":
        return int(configuracion.valor)
    return configuracion.valor

def validar_usuario_token_sin_cambio():
    token = request.headers.get('Authorization')
    data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], ["HS256"])
    usuario = Usuario(id=data["idUsuario"])
    usuario = DAOFactorySQL.get_usuario_dao().read(usuario)
    if usuario.estado == 'B':
        return jsonify({"success": False, "error" : f"El usuario se encuentra bloqueado comuniquese con el administrado de PARKUD"})
    
    return usuario

def verificar_datos_vacios_admin(json_recibido):
    if 'nombre' not in json_recibido or len(json_recibido['nombre'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo nombre vacio"})
    
    if 'apellido' not in json_recibido or len(json_recibido['apellido'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo apellido vacio"})
    
    if 'correo' not in json_recibido or len(json_recibido['correo'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo correo vacio"})
    
    if 'documentoIdentidad' not in json_recibido or len(json_recibido['documentoIdentidad'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo documento de identidad vacio"})
    
    if 'usuario' not in json_recibido or len(json_recibido['usuario'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo usuario vacio"})

    return None

def validar_contrasena(contrasena):
    if len(contrasena) < 5 or len(contrasena) > 8:
        return False
    if not re.search(r'[A-Z]', contrasena):
        return False
    if not re.search(r'[a-z]', contrasena):
        return False
    if not re.search(r'\d', contrasena):
        return False
    return True
    

def verificar_datos_vacios_operario(json_recibido):
    if 'nombre' not in json_recibido or len(json_recibido['nombre'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo nombre vacio"})
    
    if 'apellido' not in json_recibido or len(json_recibido['apellido'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo apellido vacio"})
    
    if 'documentoIdentidad' not in json_recibido or len(json_recibido['documentoIdentidad'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo documentoIdentidad vacio"})
    
    if 'usuario' not in json_recibido or len(json_recibido['usuario'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo usuario vacio"})
    
    if 'correo' not in json_recibido or len(json_recibido['correo'].strip()) == 0:
        return jsonify({"success": False, "error" : "Campo correo vacio"})

    return None
