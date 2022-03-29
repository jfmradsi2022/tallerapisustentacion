from controllers import RegisterControllers
from controllers import LoginControllers
from controllers import CrearProductoControllers
from controllers import ProductosControllers
#http:127.0.0.1:5000/
routes = {"register": "/registeruser", "register_controllers":RegisterControllers.as_view("register_api"),
"login": "/login", "login_controllers":LoginControllers.as_view("login_api"),
"crearpro": "/crearproducto", "crearpro_controllers":CrearProductoControllers.as_view("crearpro_api"),
"productos": "/productos", "productos_controllers":ProductosControllers.as_view("productos_api"),

}
