-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-06-2023 a las 05:20:09
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
-- Base de datos: `parkud`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `reserva`
--

CREATE TABLE `reserva` (
  `idReserva` bigint(20) NOT NULL,
  `horaInicio` time(4) DEFAULT NULL,
  `horaSalida` time(4) DEFAULT NULL,
  `registroSalida` time(4) DEFAULT NULL COMMENT 'Hora en la que el operador registra la salida del cliente',
  `estado` char(1) DEFAULT 'R',
  `subtotal` bigint(20) DEFAULT NULL,
  `idTarjeta` bigint(20) DEFAULT NULL,
  `idParqueadero` int(11) DEFAULT NULL,
  `idSede` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `reserva`
--

INSERT INTO `reserva` (`idReserva`, `horaInicio`, `horaSalida`, `registroSalida`, `estado`, `subtotal`, `idTarjeta`, `idParqueadero`, `idSede`) VALUES
(1, '09:00:00.0000', '10:30:00.0000', NULL, 'R', NULL, 1, 11, 12),
(2, '12:15:00.0000', '16:30:00.0000', NULL, 'R', NULL, 1, 12, 12),
(3, '15:45:00.0000', '21:00:00.0000', NULL, 'R', NULL, 1, 16, 12),
(4, '10:30:00.0000', '14:30:00.0000', NULL, 'R', NULL, 1, 17, 12),
(5, '16:00:00.0000', '21:45:00.0000', NULL, 'R', NULL, 1, 18, 12);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `reserva`
--
ALTER TABLE `reserva`
  ADD PRIMARY KEY (`idReserva`),
  ADD KEY `IXFK_Reserva_Parqueadero` (`idParqueadero`,`idSede`),
  ADD KEY `IXFK_Reserva_Tarjeta` (`idTarjeta`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `reserva`
--
ALTER TABLE `reserva`
  ADD CONSTRAINT `FK_Reserva_Tarjeta` FOREIGN KEY (`idTarjeta`) REFERENCES `tarjeta` (`idTarjeta`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
