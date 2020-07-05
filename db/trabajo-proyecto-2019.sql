-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Servidor: localhost
-- Tiempo de generación: 17-07-2019 a las 18:56:33
-- Versión del servidor: 5.7.19-0ubuntu0.16.04.1-log
-- Versión de PHP: 7.0.18-0ubuntu0.16.04.1


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Base de datos: `grupo21`
--
-- --------------------------------------------------------
DROP DATABASE IF EXISTS `grupo21`;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `grupo21` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `grupo21`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--
DROP TABLE IF EXISTS `usuario`;

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `dni` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '0',
  `updated_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `subscription` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `codigo` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `numero_tarjeta` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `perfil`;

CREATE TABLE `perfil`(  
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `usuario_id` int(11) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT FK_perfil_usuario_id FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `historial`;

CREATE TABLE `historial`(  
  `isbn` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `titulo` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `archivo` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `perfil_id` int(11) NOT NULL,
  `fecha_ultima` datetime DEFAULT NULL,
  PRIMARY KEY (archivo, perfil_id),
  CONSTRAINT FK_historial_perfil_id FOREIGN KEY (perfil_id) REFERENCES perfil(id) ON DELETE CASCADE,
  CONSTRAINT FK_historial_isbn FOREIGN KEY (isbn) REFERENCES metadato(isbn)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `novedad`;

CREATE TABLE `novedad`(
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `descripcion` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `trailer`;

CREATE TABLE `trailer`(
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `titulo` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `archivo` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




DROP TABLE IF EXISTS `libro`;

CREATE TABLE `libro`(
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `archivo` varchar(255) COLLATE utf8_unicode_ci,
  `available_from` datetime DEFAULT NULL,
  `available_to` datetime DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT FK_libro_isbn FOREIGN KEY (isbn) REFERENCES metadato(isbn)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `capitulo`;

CREATE TABLE `capitulo`(
  `num` int(11) NOT NULL,
  `isbn` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `archivo` varchar(255) COLLATE utf8_unicode_ci,
  `available_from` datetime DEFAULT NULL,
  `available_to` datetime DEFAULT NULL,
  CONSTRAINT PK_capitulo PRIMARY KEY (num, isbn)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


DROP TABLE IF EXISTS `metadato`;

CREATE TABLE `metadato`(
  `isbn` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `titulo` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `autor_id` int(11),
  `sinopsis` varchar(8000) COLLATE utf8_unicode_ci NOT NULL,
  `editorial_id` int(11) NOT NULL,
  `genero_id` int(11) NOT NULL,
  `completo` tinyInt(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (isbn),
  CONSTRAINT FK_metadato_autor_id FOREIGN KEY (autor_id) REFERENCES autor(id),
  CONSTRAINT FK_metadato_editorial_id FOREIGN KEY (editorial_id) REFERENCES editorial(id),
  CONSTRAINT FK_metadato_genero_id FOREIGN KEY (genero_id) REFERENCES genero(id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;





DROP TABLE IF EXISTS `autor`;

CREATE TABLE `autor`(
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `editorial`;

CREATE TABLE `editorial`(
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

DROP TABLE IF EXISTS `genero`;

CREATE TABLE `genero`(
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (2,'sofia@gmail.com','21423123','fede','1234',1,19-11-20,19-11-20,'sofia','fernandez', 'basic', 19-11-20,'500','1234123412341234');
INSERT INTO `usuario` VALUES (1,'ivan@gmail.com','11123123','ivan','1234',1,19-11-20,19-11-20,'ivan','Mindlin', 'premium', 19-11-20,'500','1234123412341234');
INSERT INTO `usuario` VALUES (3,'martin@gmail.com','33123123','lorenzo','1234',1,19-11-20,19-11-20,'martin','delpino', 'premium', 19-11-20,'500','1234123412341234');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;


--
-- Estructura de tabla para la tabla `rol`
--
DROP TABLE IF EXISTS `rol`;
CREATE TABLE `rol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
INSERT INTO `rol` VALUES (1,'Admin'),(2,'Docente'),(3,'Preceptor');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permiso`
--

CREATE TABLE `permiso` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

LOCK TABLES `permiso` WRITE;
/*!40000 ALTER TABLE `permiso` DISABLE KEYS */;
INSERT INTO `permiso` VALUES (1,'usuario_index'),(2,'usuario_new'),(3,'usuario_destroy'),(4,'usuario_update'),(5,'usuario_show'),(6,'usuario_activar'),(7,'usuario_desactivar'),(8,'usuario_asignar_rol'), (9,'configuracion_paginado'), (10,'configuracion_info'), (11, 'configuracion_habilitado'), (12, 'configuracion_usarInhabilitado'), (13, 'estudiantes_new'), (14, 'estudiantes_index'), (15, 'estudiantes_show'), (16, 'estudiantes_update'), (17, 'estudiantes_destroy'), (18, 'docentes_new'), (19, 'docentes_index'), (20, 'docentes_show'), (21, 'docentes_update'), (22, 'docentes_destroy'), (23, 'lectivo_new'), (24, 'lectivo_index'), (25, 'lectivo_show'), (26, 'lectivo_update'), (27, 'lectivo_destroy'), (28, 'instrumento_new'), (29, 'instrumento_index'), (30, 'instrumento_show'), (31, 'instrumento_update'), (32, 'instrumento_destroy'), (33, 'horario_index'), (34, 'horario_show'), (35, 'horario_new'), (36, 'horario_update'), (37, 'horario_destroy');
/*!40000 ALTER TABLE `permiso` ENABLE KEYS */;
UNLOCK TABLES;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_tiene_permiso`
--

CREATE TABLE `rol_tiene_permiso` (
  `rol_id` int(11) NOT NULL,
  `permiso_id` int(11) NOT NULL,
  PRIMARY KEY (rol_id, permiso_id),
  CONSTRAINT FK_rol_id FOREIGN KEY (rol_id) REFERENCES rol(id),
  CONSTRAINT FK_permiso_id FOREIGN KEY (permiso_id) REFERENCES permiso(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;




LOCK TABLES `rol_tiene_permiso` WRITE;
/*!40000 ALTER TABLE `rol_tiene_permiso` DISABLE KEYS */;
INSERT INTO `rol_tiene_permiso` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),
(2,1), (2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(3,1),(3,2),(3,3),(3,4),(3,5), (1, 12),
(1, 13), (1, 14), (1, 15), (1, 16), (1, 17),
(1, 18), (1, 19), (1, 20), (1, 21), (1, 22),
(1, 23), (1, 24), (1, 25), (1, 26), (1, 27),
(2, 14), (2, 15), (2, 16), (1, 28), (1, 29),
(3, 14), (3, 15), (3, 16), (1, 30), (1, 31),
(3, 19), (3, 20), (2, 29), (2, 30), (1, 32),
(3, 24), (3, 25), (1,33),(1,34),(1,35),(1,36),(1,37),(2,33),(2,34);

/*!40000 ALTER TABLE `rol_tiene_permiso` ENABLE KEYS */;
UNLOCK TABLES;
-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_tiene_permiso`
--

CREATE TABLE `usuario_tiene_rol` (
  `usuario_id` int(11) NOT NULL,
  `rol_id` int(11) NOT NULL,
  PRIMARY KEY (usuario_id, rol_id),
  CONSTRAINT FK_usuario_utp_id FOREIGN KEY (usuario_id) REFERENCES usuario(id),
  CONSTRAINT FK_rol_utp_id FOREIGN KEY (rol_id) REFERENCES rol(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


LOCK TABLES `usuario_tiene_rol` WRITE;
/*!40000 ALTER TABLE `usuario_tiene_rol` DISABLE KEYS */;
INSERT INTO `usuario_tiene_rol` VALUES (1,1),(2,2),(3,1);
/*!40000 ALTER TABLE `usuario_tiene_rol` ENABLE KEYS */;
UNLOCK TABLES;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion`
--

DROP TABLE IF EXISTS `configuracion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `configuracion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cantidad_elementos_pagina` int(5),
  `habilitado` tinyInt(1),
  `titulo` varchar (255),
  `descripcion` varchar (255),
  `mail_orquesta` varchar(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `configuracion` WRITE;
/*!40000 ALTER TABLE `configuracion` DISABLE KEYS */;
INSERT INTO `configuracion` VALUES (1,10,1,'Bookflix','Bookflix, para leer y leerse','contact@bookflix.com');
/*!40000 ALTER TABLE `configuracion` ENABLE KEYS */;
UNLOCK TABLES;

DROP TABLE IF EXISTS `paginado`;

CREATE TABLE `paginado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tamanio_paginado` int (5),
  `indice_actual` int (5),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

LOCK TABLES `paginado` WRITE;
INSERT INTO `paginado` VALUES (1, 5, 0);
UNLOCK TABLES;

