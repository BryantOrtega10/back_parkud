-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-05-2023 a las 01:53:54
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `par_kud`
--

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `caracteristica`
--

CREATE TABLE `caracteristica` (
  `idCaracteristica` bigint(20) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `caracteristica_sede`
--

INSERT INTO `caracteristica_sede` (`idCaracteristica`, `idSede`) VALUES
(1, 1),
(2, 2);

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion`
--

CREATE TABLE `configuracion` (
  `id` varchar(5) NOT NULL,
  `valor` varchar(50) DEFAULT NULL,
  `tipoDeDato` varchar(50) DEFAULT NULL COMMENT 'Especifica el tipo de dato del valor.'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Tabla que contiene la parametrizacion de las funcionalidades del sistema';

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parqueadero`
--

CREATE TABLE `parqueadero` (
  `idParqueadero` int(11) NOT NULL,
  `idSede` bigint(20) NOT NULL,
  `idTipo_Parqueadero` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `parqueadero`
--

INSERT INTO `parqueadero` (`idParqueadero`, `idSede`, `idTipo_Parqueadero`) VALUES
(1, 1, 1),
(4, 2, 1),
(2, 1, 2),
(5, 2, 2),
(3, 1, 3);

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sede`
--

INSERT INTO `sede` (`idSede`, `nombre`, `latitud`, `longitud`, `estado`, `fidelizacion`, `horaInicio`, `horaFin`, `tiempoCompleto`, `idAdministrador`, `idUbicacion`) VALUES
(1, 'Titan Plaza', 4.694730281829834, -74.086181640625000, 'A', 0, '00:00:00.0000', '00:00:00.0000', 1, NULL, 3),
(2, 'Primavera Urbana', 4.134982109069824, -73.640449523925780, 'A', 0, '09:00:00.0000', '20:00:00.0000', 0, NULL, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarifa`
--

CREATE TABLE `tarifa` (
  `idTarifa` bigint(20) NOT NULL,
  `valor` double(10,2) DEFAULT NULL,
  `idSede` bigint(20) DEFAULT NULL,
  `idTipo_Parqueadero` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tarifa`
--

INSERT INTO `tarifa` (`idTarifa`, `valor`, `idSede`, `idTipo_Parqueadero`) VALUES
(1, 3500.00, 1, 3),
(2, 6000.00, 1, 2),
(3, 13000.00, 1, 1),
(4, 4000.00, 2, 2),
(5, 8000.00, 2, 1);

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_parqueadero`
--

CREATE TABLE `tipo_parqueadero` (
  `idTipo_Parqueadero` bigint(20) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  MODIFY `idAdministrador` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `caracteristica`
--
ALTER TABLE `caracteristica`
  MODIFY `idCaracteristica` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `idCliente` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `operario`
--
ALTER TABLE `operario`
  MODIFY `idOperario` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `sede`
--
ALTER TABLE `sede`
  MODIFY `idSede` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `tarifa`
--
ALTER TABLE `tarifa`
  MODIFY `idTarifa` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

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
  MODIFY `idUsuario` bigint(20) NOT NULL AUTO_INCREMENT;

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
  ADD CONSTRAINT `FK_Caracteristica_Sede_Caracteristicas` FOREIGN KEY (`idCaracteristica`) REFERENCES `caracteristica` (`idCaracteristica`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `FK_Caracteristica_Sede_Sede` FOREIGN KEY (`idSede`) REFERENCES `sede` (`idSede`) ON DELETE NO ACTION ON UPDATE NO ACTION;

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
  ADD CONSTRAINT `FK_Parqueadero_Sede` FOREIGN KEY (`idSede`) REFERENCES `sede` (`idSede`) ON DELETE NO ACTION ON UPDATE NO ACTION,
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
  ADD CONSTRAINT `FK_Tarifa_Sede` FOREIGN KEY (`idSede`) REFERENCES `sede` (`idSede`) ON DELETE NO ACTION ON UPDATE NO ACTION,
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
