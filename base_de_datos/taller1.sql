/*create schema taller1;*/

/*use taller1;*/

CREATE TABLE `registro` (
`nombres` char(200) NOT NULL,
`apellidos` char(200) NOT NULL,
`edad` int(3) NOT NULL,
 `ciudad` char(100) NOT NULL,
`clave` char(200) NOT NULL,
`correo` char(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `productos` (
`idproducto` int(3) NOT NULL primary key,
`producto` char(200) NOT NULL,
`cantidad` char(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;