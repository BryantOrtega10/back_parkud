-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-06-2023 a las 04:16:04
-- Versión del servidor: 10.4.13-MariaDB
-- Versión de PHP: 7.4.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `parkud`
--
CREATE DATABASE IF NOT EXISTS `parkud` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `parkud`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administrador`
--

CREATE TABLE `administrador` (
  `idAdministrador` bigint(20) NOT NULL,
  `nombre` varchar(80) DEFAULT NULL,
  `apellido` varchar(80) DEFAULT NULL,
  `documentoIdentidad` varchar(20) DEFAULT NULL,
  `idUsuario` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `administrador`
--

INSERT INTO `administrador` (`idAdministrador`, `nombre`, `apellido`, `documentoIdentidad`, `idUsuario`) VALUES
(1, 'Bryant', 'Administrador', '1022', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `caracteristica`
--

CREATE TABLE `caracteristica` (
  `idCaracteristica` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `caracteristica`
--

INSERT INTO `caracteristica` (`idCaracteristica`, `nombre`) VALUES
(1, 'Cubierto'),
(2, 'Semi descubierto'),
(3, 'Descubierto');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `caracteristica_sede`
--

CREATE TABLE `caracteristica_sede` (
  `idCaracteristica` bigint(20) NOT NULL,
  `idSede` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `caracteristica_sede`
--

INSERT INTO `caracteristica_sede` (`idCaracteristica`, `idSede`) VALUES
(1, 1),
(1, 12),
(2, 2),
(2, 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `idCliente` bigint(20) NOT NULL,
  `nombre` varchar(80) NOT NULL,
  `apellido` varchar(80) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `documentoIdentidad` varchar(20) NOT NULL,
  `idUsuario` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`idCliente`, `nombre`, `apellido`, `telefono`, `documentoIdentidad`, `idUsuario`) VALUES
(1, 'Bryant David', 'Ortega', '3154861174', '1022397', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion`
--

CREATE TABLE `configuracion` (
  `id` varchar(5) NOT NULL,
  `valor` varchar(50) DEFAULT NULL,
  `tipoDeDato` varchar(50) DEFAULT NULL COMMENT 'Especifica el tipo de dato del valor.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='Tabla que contiene la parametrizacion de las funcionalidades del sistema';

--
-- Volcado de datos para la tabla `configuracion`
--

INSERT INTO `configuracion` (`id`, `valor`, `tipoDeDato`) VALUES
('C_ADM', 'bdortegav@udistrital.edu.co', 'string'),
('N_FAI', '3', 'int');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `operario`
--

CREATE TABLE `operario` (
  `idOperario` bigint(20) NOT NULL,
  `nombre` varchar(80) DEFAULT NULL,
  `apellido` varchar(80) DEFAULT NULL,
  `documentoIdentidad` varchar(20) DEFAULT NULL,
  `idSede` bigint(20) DEFAULT NULL,
  `idUsuario` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `operario`
--

INSERT INTO `operario` (`idOperario`, `nombre`, `apellido`, `documentoIdentidad`, `idSede`, `idUsuario`) VALUES
(1, 'Bryant Opera', 'rio', '10223', 12, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parqueadero`
--

CREATE TABLE `parqueadero` (
  `idParqueadero` int(11) NOT NULL,
  `idSede` bigint(20) NOT NULL,
  `idTipo_Parqueadero` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `parqueadero`
--

INSERT INTO `parqueadero` (`idParqueadero`, `idSede`, `idTipo_Parqueadero`) VALUES
(11, 12, 1),
(12, 12, 1),
(13, 12, 1),
(14, 12, 1),
(15, 12, 1),
(16, 12, 2),
(17, 12, 2),
(18, 12, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reserva`
--

CREATE TABLE `reserva` (
  `idReserva` bigint(20) NOT NULL,
  `horaInicio` TIMESTAMP DEFAULT NULL,
  `horaSalida` TIMESTAMP DEFAULT NULL,
  `registroSalida` TIMESTAMP DEFAULT NULL COMMENT 'Hora en la que el operador registra la salida del cliente',
  `subtotal` bigint(20) DEFAULT NULL,
  `idTarjeta` bigint(20) DEFAULT NULL,
  `idParqueadero` int(11) DEFAULT NULL,
  `idSede` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sede`
--

CREATE TABLE `sede` (
  `idSede` bigint(20) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `latitud` float(20,15) DEFAULT NULL,
  `longitud` float(20,15) DEFAULT NULL,
  `estado` char(1) NOT NULL DEFAULT 'A',
  `fidelizacion` tinyint(4) DEFAULT NULL,
  `horaInicio` time(4) DEFAULT NULL,
  `horaFin` time(4) DEFAULT NULL,
  `tiempoCompleto` tinyint(4) DEFAULT 0,
  `idAdministrador` bigint(20) DEFAULT NULL,
  `idUbicacion` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `sede`
--

INSERT INTO `sede` (`idSede`, `nombre`, `latitud`, `longitud`, `estado`, `fidelizacion`, `horaInicio`, `horaFin`, `tiempoCompleto`, `idAdministrador`, `idUbicacion`) VALUES
(1, 'Titan Plaza', 4.694730281829834, -74.086181640625000, 'A', 0, '00:00:00.0000', '00:00:00.0000', 1, NULL, 3),
(2, 'Primavera Urbana', 4.134982109069824, -73.640449523925780, 'A', 0, '09:00:00.0000', '20:00:00.0000', 0, NULL, 4),
(12, 'TEST Norte', 4.751732826232910, -74.046638488769530, 'A', 0, '09:00:00.0000', '23:00:00.0000', 0, 1, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarifa`
--

CREATE TABLE `tarifa` (
  `idTarifa` bigint(20) NOT NULL,
  `valor` double(10,2) DEFAULT NULL,
  `idSede` bigint(20) DEFAULT NULL,
  `idTipo_Parqueadero` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tarifa`
--

INSERT INTO `tarifa` (`idTarifa`, `valor`, `idSede`, `idTipo_Parqueadero`) VALUES
(1, 3500.00, 1, 3),
(2, 6000.00, 1, 2),
(3, 13000.00, 1, 1),
(4, 4000.00, 2, 2),
(5, 8000.00, 2, 1),
(9, 110.00, 12, 1),
(10, 130.00, 12, 2),
(11, 15.00, 12, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarjeta`
--

CREATE TABLE `tarjeta` (
  `idTarjeta` bigint(20) NOT NULL,
  `tipo` char(1) DEFAULT NULL COMMENT 'Tipo de la tarjeta: ''C'' credito, ''D'' debito.',
  `numero` varchar(16) DEFAULT NULL,
  `fechaExpiracion` varchar(5) DEFAULT NULL,
  `csv` varchar(3) DEFAULT NULL,
  `token` varchar(250) DEFAULT NULL,
  `idCliente` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_parqueadero`
--

CREATE TABLE `tipo_parqueadero` (
  `idTipo_Parqueadero` bigint(20) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tipo_parqueadero`
--

INSERT INTO `tipo_parqueadero` (`idTipo_Parqueadero`, `nombre`) VALUES
(1, 'Carros'),
(2, 'Motos'),
(3, 'Bicicletas');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_ubicacion`
--

CREATE TABLE `tipo_ubicacion` (
  `idTipo_Ubicacion` bigint(20) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `tipo_ubicacion`
--

INSERT INTO `tipo_ubicacion` (`idTipo_Ubicacion`, `nombre`) VALUES
(1, 'Región'),
(2, 'Ciudad');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ubicacion`
--

CREATE TABLE `ubicacion` (
  `idUbicacion` bigint(20) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `fkUbicacion` bigint(20) DEFAULT NULL,
  `idTipo_Ubicacion` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `ubicacion`
--

INSERT INTO `ubicacion` (`idUbicacion`, `descripcion`, `fkUbicacion`, `idTipo_Ubicacion`) VALUES
(1, 'Región Andina', NULL, 1),
(2, 'Región Orinoquia', NULL, 1),
(3, 'Bogotá D.C', 1, 2),
(4, 'Ciudad de Villavicencio', 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idUsuario` bigint(20) NOT NULL,
  `usuario` varchar(8) DEFAULT NULL,
  `contrasena` varchar(32) DEFAULT NULL,
  `rol` char(1) DEFAULT NULL,
  `cambiarContrasena` tinyint(4) DEFAULT NULL COMMENT 'Identifica si el usuario inicia sesion por primera vez, o si solicita cambio de contraseña, entre otros.',
  `contrasenaDobleFactor` varchar(32) DEFAULT NULL,
  `numIntentosFallidos` smallint(6) DEFAULT NULL COMMENT 'Numero de intentos fallidos del usuario.',
  `estado` char(1) DEFAULT NULL COMMENT 'Identifica si el usuario esta bloqueado (B), activo(A)...',
  `token` varchar(250) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `usuario`, `contrasena`, `rol`, `cambiarContrasena`, `contrasenaDobleFactor`, `numIntentosFallidos`, `estado`, `token`, `correo`) VALUES
(1, 'bryant', 'caa8bf140dd336a6b2be2506a1011d43', 'S', 0, '92eb554f797ee376efd5ec06a04c7b5a', 0, 'S', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZFVzdWFyaW8iOjF9.bD9NJDScWO8iJxHjj8JzJoajGAbrNNaUpiYSNFpqgIU', 'bdortegav@udistrital.edu.co'),
(2, 'bry_adm', 'caa8bf140dd336a6b2be2506a1011d43', 'A', 0, 'ad18258b0525d396f9e9abbba8ce66e8', 0, 'A', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZFVzdWFyaW8iOjJ9.Xdc1vK1LNuCNOvTdpqY0mmaBrsitws5Kli-vueqche8', 'bryant.ortega1010@gmail.com'),
(3, 'bry_mdc1', '569c9a5855fc6e0ab318370d5e46f049', 'O', 1, '', 0, 'A', NULL, 'bryant@mdccolombia.com');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD PRIMARY KEY (`idAdministrador`),
  ADD KEY `IXFK_Administrador_Usuario` (`idUsuario`);

--
-- Indices de la tabla `caracteristica`
--
ALTER TABLE `caracteristica`
  ADD PRIMARY KEY (`idCaracteristica`);

--
-- Indices de la tabla `caracteristica_sede`
--
ALTER TABLE `caracteristica_sede`
  ADD PRIMARY KEY (`idCaracteristica`,`idSede`),
  ADD KEY `IXFK_Caracteristica_Sede_Caracteristicas` (`idCaracteristica`),
  ADD KEY `IXFK_Caracteristica_Sede_Sede` (`idSede`);

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`idCliente`),
  ADD KEY `IXFK_Cliente_Usuario` (`idUsuario`);

--
-- Indices de la tabla `configuracion`
--
ALTER TABLE `configuracion`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `operario`
--
ALTER TABLE `operario`
  ADD PRIMARY KEY (`idOperario`),
  ADD KEY `IXFK_Operario_Sede` (`idSede`),
  ADD KEY `IXFK_Operario_Usuario` (`idUsuario`);

--
-- Indices de la tabla `parqueadero`
--
ALTER TABLE `parqueadero`
  ADD PRIMARY KEY (`idParqueadero`,`idSede`),
  ADD KEY `IXFK_Parqueadero_Sede` (`idSede`),
  ADD KEY `IXFK_Parqueadero_Tipo_Parqueadero` (`idTipo_Parqueadero`);

--
-- Indices de la tabla `reserva`
--
ALTER TABLE `reserva`
  ADD PRIMARY KEY (`idReserva`),
  ADD KEY `IXFK_Reserva_Parqueadero` (`idParqueadero`,`idSede`),
  ADD KEY `IXFK_Reserva_Tarjeta` (`idTarjeta`);

--
-- Indices de la tabla `sede`
--
ALTER TABLE `sede`
  ADD PRIMARY KEY (`idSede`),
  ADD KEY `IXFK_Sede_Administrador` (`idAdministrador`),
  ADD KEY `IXFK_Sede_Ubicacion` (`idUbicacion`);

--
-- Indices de la tabla `tarifa`
--
ALTER TABLE `tarifa`
  ADD PRIMARY KEY (`idTarifa`),
  ADD KEY `IXFK_Tarifa_Sede` (`idSede`),
  ADD KEY `IXFK_Tarifa_Tipo_Parqueadero` (`idTipo_Parqueadero`);

--
-- Indices de la tabla `tarjeta`
--
ALTER TABLE `tarjeta`
  ADD PRIMARY KEY (`idTarjeta`),
  ADD KEY `IXFK_Tarjeta_Cliente` (`idCliente`);

--
-- Indices de la tabla `tipo_parqueadero`
--
ALTER TABLE `tipo_parqueadero`
  ADD PRIMARY KEY (`idTipo_Parqueadero`);

--
-- Indices de la tabla `tipo_ubicacion`
--
ALTER TABLE `tipo_ubicacion`
  ADD PRIMARY KEY (`idTipo_Ubicacion`);

--
-- Indices de la tabla `ubicacion`
--
ALTER TABLE `ubicacion`
  ADD PRIMARY KEY (`idUbicacion`),
  ADD KEY `IXFK_Ubicacion_Tipo_Ubicacion` (`idTipo_Ubicacion`),
  ADD KEY `IXFK_Ubicacion_Ubicacion` (`fkUbicacion`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idUsuario`),
  ADD UNIQUE KEY `UK_Correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administrador`
--
ALTER TABLE `administrador`
  MODIFY `idAdministrador` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `caracteristica`
--
ALTER TABLE `caracteristica`
  MODIFY `idCaracteristica` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `idCliente` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `operario`
--
ALTER TABLE `operario`
  MODIFY `idOperario` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `parqueadero`
--
ALTER TABLE `parqueadero`
  MODIFY `idParqueadero` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `sede`
--
ALTER TABLE `sede`
  MODIFY `idSede` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `tarifa`
--
ALTER TABLE `tarifa`
  MODIFY `idTarifa` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `tarjeta`
--
ALTER TABLE `tarjeta`
  MODIFY `idTarjeta` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_parqueadero`
--
ALTER TABLE `tipo_parqueadero`
  MODIFY `idTipo_Parqueadero` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idUsuario` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `administrador`
--
ALTER TABLE `administrador`
  ADD CONSTRAINT `FK_Administrador_Usuario` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `caracteristica_sede`
--
ALTER TABLE `caracteristica_sede`
  ADD CONSTRAINT `FK_Caracteristica_Sede_Caracteristicas` FOREIGN KEY (`idCaracteristica`) REFERENCES `caracteristica` (`idCaracteristica`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_Caracteristica_Sede_Sede` FOREIGN KEY (`idSede`) REFERENCES `sede` (`idSede`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `FK_Cliente_Usuario` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `operario`
--
ALTER TABLE `operario`
  ADD CONSTRAINT `FK_Operario_Sede` FOREIGN KEY (`idSede`) REFERENCES `sede` (`idSede`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `FK_Operario_Usuario` FOREIGN KEY (`idUsuario`) REFERENCES `usuario` (`idUsuario`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `parqueadero`
--
ALTER TABLE `parqueadero`
  ADD CONSTRAINT `FK_Parqueadero_Sede` FOREIGN KEY (`idSede`) REFERENCES `sede` (`idSede`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_Parqueadero_Tipo_Parqueadero` FOREIGN KEY (`idTipo_Parqueadero`) REFERENCES `tipo_parqueadero` (`idTipo_Parqueadero`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `reserva`
--
ALTER TABLE `reserva`
  ADD CONSTRAINT `FK_Reserva_Tarjeta` FOREIGN KEY (`idTarjeta`) REFERENCES `tarjeta` (`idTarjeta`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `sede`
--
ALTER TABLE `sede`
  ADD CONSTRAINT `FK_Sede_Administrador` FOREIGN KEY (`idAdministrador`) REFERENCES `administrador` (`idAdministrador`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `FK_Sede_Ubicacion` FOREIGN KEY (`idUbicacion`) REFERENCES `ubicacion` (`idUbicacion`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `tarifa`
--
ALTER TABLE `tarifa`
  ADD CONSTRAINT `FK_Tarifa_Sede` FOREIGN KEY (`idSede`) REFERENCES `sede` (`idSede`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `FK_Tarifa_Tipo_Parqueadero` FOREIGN KEY (`idTipo_Parqueadero`) REFERENCES `tipo_parqueadero` (`idTipo_Parqueadero`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `tarjeta`
--
ALTER TABLE `tarjeta`
  ADD CONSTRAINT `FK_Tarjeta_Cliente` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `ubicacion`
--
ALTER TABLE `ubicacion`
  ADD CONSTRAINT `FK_Ubicacion_Tipo_Ubicacion` FOREIGN KEY (`idTipo_Ubicacion`) REFERENCES `tipo_ubicacion` (`idTipo_Ubicacion`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `FK_Ubicacion_Ubicacion` FOREIGN KEY (`fkUbicacion`) REFERENCES `ubicacion` (`idUbicacion`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
