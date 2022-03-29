
from flask.views import MethodView
from flask import jsonify, request, session
#from model import users
import hashlib
import pymysql
import bcrypt # pip3 install bcrypt
import jwt # pip3 install pyjwt
from config import KEY_TOKEN_AUTH
import datetime
from validators import CreateRegisterSchema
from validators import CreateLoginSchema
from validators import CreateProductoSchema

def crear_conexion():
    try:
        #conexion a la db
        conexion = pymysql.connect(host='localhost',user='root',passwd='',db="taller1" )
        return conexion
    except pymysql.Error as error:
        print('Se ha producido un error al crear la conexión:', error)

#validaciones

create_register_schema = CreateRegisterSchema()
create_login_schema = CreateLoginSchema()
create_producto_schema = CreateProductoSchema()

#http://127.0.0.1:5000/registeruser  - REGISTRO DE USUARIOS

class RegisterControllers(MethodView):
    """
        register
    """
    def post(self):
        content = request.get_json() # se envia por json
        correo = content.get("correo")# =jhonfabermr@hotmail.com
        nombres = content.get("nombres")# = Jhon Faber
        apellidos = content.get("apellidos") #Muñoz Restrepo
        password = content.get("password") # 123456789
        print("--------", correo, nombres, apellidos,password)

        salt = bcrypt.gensalt() ## son para hacer hash
        hash_password = bcrypt.hashpw(bytes(str(password), encoding= 'utf-8'), salt)## son para hacer hash
        print ("este es el hash de password ",hash_password)
        
        #ARCHIVO VALIDATORS
        errors = create_register_schema.validate(content)
        if errors:
            return errors, 400

        conexion=crear_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT clave,correo FROM usuarios WHERE correo=%s", (correo,))
        auto=cursor.fetchone()
        if auto==None:
            cursor.execute(
                 "INSERT INTO usuarios (correo,nombres,apellidos,clave) VALUES(%s,%s,%s,%s)", (correo,nombres,apellidos,hash_password,))
            conexion.commit()
            conexion.close()
            return ("*******Bienvenido registro exitoso en el sistema ******")
        else :
            conexion.commit()   
            conexion.close()
            return ("el usuario ya esta registrado")

#http://127.0.0.1:5000/login

class LoginControllers(MethodView): # LOGIN DE USUARIOS - INICIO DE SESION
    """
        Login
    """
    def post(self):  # se envia por json
        content = request.get_json() # se envia por json
        correo = content.get("correo")# =jhonfabermr@hotmail.com
        password = content.get("password") # 123456789
        print("--------", correo,password)

        #ARCHIVO VALIDATORS
        errors = create_login_schema.validate(content)
        if errors:
            return errors, 400

        salt = bcrypt.gensalt()
        user_password= bcrypt.hashpw(bytes(str(password), encoding= 'utf-8'), salt) #user_password= hash de 123456789
        conexion=crear_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT clave,correo,nombres FROM usuarios WHERE correo=%s", (correo, ))
        auto = cursor.fetchone()
        conexion.close()

        if auto==None:
            print(auto)
            return jsonify({"Status": "usuario no registrado 22"}), 400

        db_password = bytes(auto[0], encoding="utf-8") #hash almacenado en la base de datos

        if (auto[1]==correo):
            if not bcrypt.checkpw(user_password, db_password):# compara el hash de las aptenido del usuario con el alamacenado
                encoded_jwt = jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3000), 'correo': correo, 'nombres':auto[2]}, KEY_TOKEN_AUTH , algorithm='HS256')
                return jsonify({"Status": "login exitoso","usuario: "+auto[2]+ " token ": encoded_jwt}), 200
        else:
            return jsonify({"Status": "correo o clave incorrecta"}), 400


#http://127.0.0.1:5000/crearproducto

# 
# {
#  "producto": "mouse",
#  "precio":2000
#}


class CrearProductoControllers(MethodView): #Crear producto en la base de datos - tabla productos
    def post(self):
        content = request.get_json()
        print("***Que contiene****",content)
        var_jwt=request.headers.get('Authorization')
        print("Authorization: ", var_jwt)
        datosHeader= var_jwt.split(" ")
        if (len(datosHeader) <= 1):
            return jsonify({"Status": "Header de autorización no válido"}), 400
        print("datosHeader: ", datosHeader[1])
        print(datosHeader)
        jwt_token= (datosHeader[1])
        print("Este es el token: ",datosHeader[1])
        try:
            payload = jwt.decode(jwt_token,KEY_TOKEN_AUTH,algorithms='HS256')
        except:
            return jsonify({"Status": "Token no válido"}), 400
        print("este es el token ", payload)

        ##ARCHIVO VALIDATORS
        errors = create_producto_schema.validate(content)
        if errors:
            return errors, 400

        conexion=crear_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT producto,precio FROM productos WHERE producto=%s", (content.get("producto",)))
        auto=cursor.fetchone()
        if auto==None:
            cursor.execute(
            "INSERT INTO productos(producto,precio) VALUES(%s,%s)", (content.get("producto"),content.get("precio"),))
            conexion.commit()
            conexion.close()
            return jsonify({"Status": "El producto fue creeado Correctamente","token":jwt_token}), 200 
        else:
            return ("el producto ya esta registrado"),400     
            

















#http://127.0.0.1:5000/productos
class ProductosControllers(MethodView):
    """
        json
    """
    def get(self):
        #idprodc= request.headers.get("idproducto") # asi es que envia por cabecera un solo producto - headers idproducto - 1
        #consulta base de datos
        conexion=crear_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT * FROM productos")
        auto=cursor.fetchall()
        print("Lista de productos",auto)
        conexion.close()
        return jsonify(auto), 200
