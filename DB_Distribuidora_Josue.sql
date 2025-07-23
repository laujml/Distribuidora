/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-11.8.2-MariaDB, for osx10.20 (arm64)
--
-- Host: localhost    Database: Distribuidora
-- ------------------------------------------------------
-- Server version	11.8.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `Cliente`
--

DROP TABLE IF EXISTS `Cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Cliente` (
  `ID_Cliente` int(11) NOT NULL,
  `Nombre` varchar(60) NOT NULL,
  `Correo` varchar(60) NOT NULL,
  `Telefono` varchar(25) NOT NULL,
  `Direccion` varchar(100) NOT NULL,
  PRIMARY KEY (`ID_Cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cliente`
--

LOCK TABLES `Cliente` WRITE;
/*!40000 ALTER TABLE `Cliente` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Cliente` VALUES
(1,'Wendy Sofia Rodriguez Salazar','analopez.43@correo.com','12345678','calle2'),
(51,'Ana Maria Perez Vaca','anamtruji@gmail.com','79788805','Residencial Buenos Aires, 34, SS'),
(52,'Jose Andres Martinez Salgado','chepena@gmail.com','77552684','Calle Maltes, 56, Santa Tecla, La Libertad'),
(53,'Aurora Elizabeth Smith Fu','auro77@gmail.com','76941167','Residencial Bernal, 55, senda y, SS'),
(54,'Jose Manuel O\'Conell Phelps','josecoto@gmail.com','78547241','Calle Masferrer Norte, senda pino, 78, SS'),
(55,'Roxana Carolina Ortiz Serrano','rocarapa@gmail.com','76953417','Final calle Pinares, senda azul, 12, Santa Tecla, La Libertad'),
(56,'Ricardo Eduardo Rivera Flores','richard09@gmail.com','77432017','Final calle Pinares, senda azul, 12, Santa Tecla, La Libertad'),
(57,'Ariana Valeria Ponce Moreno','bubbleari@gmail.com','79965322','Colonia Guatemala, poligono h, 55, SS'),
(58,'Marcelo Alejandro Cortez Perez','marcesalam@gmail.com','73537027','Colonia La cima, 375, senda Castanos, SS'),
(59,'Ariana Eliza Juarez Cortez','arianapucca10@gmail.com','73244367','Residencial Antibes, 28, SS'),
(60,'Ariana Nicolle Guzman Alvarado','arival00fgr@gmail.com','70856350','Calle Suiza sur, senda 10, 7p, SS'),
(233,'maria','maria@correo.com','244343','calle 4'),
(3454,'Mario Santos','mario@correo.com','234344','calle 5'),
(12345,'ana maria','20correo@correo.com','123456000','calle  1 avenida 2'),
(12000121,'Maria Antonieta Cruz Estrella','123correo@correoimaginario.com','12233445','Residencial sur, 5a ave');
/*!40000 ALTER TABLE `Cliente` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Estado`
--

DROP TABLE IF EXISTS `Estado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Estado` (
  `id_estado` tinyint(4) NOT NULL AUTO_INCREMENT,
  `estado` varchar(25) NOT NULL,
  PRIMARY KEY (`id_estado`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Estado`
--

LOCK TABLES `Estado` WRITE;
/*!40000 ALTER TABLE `Estado` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Estado` VALUES
(1,'Pagado'),
(2,'Pendiente'),
(3,'Pagado parcialmente');
/*!40000 ALTER TABLE `Estado` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Pedido`
--

DROP TABLE IF EXISTS `Pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Pedido` (
  `ID_Pedido` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Cliente` int(11) NOT NULL,
  `fecha_hora` datetime NOT NULL,
  `total` decimal(7,2) DEFAULT 0.00,
  `id_estado` tinyint(4) NOT NULL,
  `pendiente_pagar` decimal(7,2) DEFAULT 0.00,
  `plazo_dias` int(11) DEFAULT NULL CHECK (`plazo_dias` <= 30),
  PRIMARY KEY (`ID_Pedido`),
  KEY `ID_Cliente` (`ID_Cliente`),
  KEY `Pedido_Estado_FK` (`id_estado`),
  CONSTRAINT `Pedido_Estado_FK` FOREIGN KEY (`id_estado`) REFERENCES `Estado` (`id_estado`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`ID_Cliente`) REFERENCES `Cliente` (`ID_Cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pedido`
--

LOCK TABLES `Pedido` WRITE;
/*!40000 ALTER TABLE `Pedido` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Pedido` VALUES
(1,12000121,'2025-07-13 10:51:10',54.75,1,0.00,0),
(2,12000121,'2025-07-13 10:54:10',57.99,1,0.00,0),
(4,12345,'2025-07-13 15:43:19',17.55,1,0.00,0),
(5,53,'2025-07-13 15:48:51',17.55,1,0.00,0),
(6,53,'2025-07-13 16:32:23',56.70,3,20.00,2),
(7,56,'2025-07-13 16:34:59',45.40,1,0.00,0),
(9,57,'2025-07-15 16:07:47',39.98,1,0.00,0),
(10,56,'2025-07-16 16:37:59',18.70,1,0.00,0),
(11,53,'2025-07-16 16:56:59',17.55,1,17.55,1),
(13,12345,'2025-07-16 17:02:20',10.00,1,0.00,0),
(14,54,'2025-07-16 17:35:34',17.55,1,0.00,0),
(15,54,'2025-07-16 17:36:03',30.00,2,30.00,1),
(16,54,'2025-07-16 17:48:24',10.00,1,0.00,0),
(17,51,'2025-07-16 18:11:20',54.00,3,25.00,2),
(19,12345,'2025-07-16 20:53:06',10.00,1,0.00,0),
(20,12345,'2025-07-16 20:54:38',20.00,1,0.00,0),
(21,57,'2025-07-16 20:55:02',10.00,1,0.00,0),
(22,12345,'2025-07-16 20:55:24',30.00,1,0.00,0),
(24,12345,'2025-07-17 10:30:26',105.30,1,0.00,0),
(25,12345,'2025-07-17 14:20:03',18.70,1,0.00,0),
(26,58,'2025-07-18 15:24:32',18.25,1,0.00,0),
(27,12345,'2025-07-18 23:46:22',18.70,1,0.00,0),
(29,3454,'2025-07-22 08:49:50',27.00,1,0.00,0);
/*!40000 ALTER TABLE `Pedido` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Productos`
--

DROP TABLE IF EXISTS `Productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Productos` (
  `ID_Productos` varchar(30) NOT NULL,
  `descripcion` varchar(70) NOT NULL,
  `precio` decimal(5,2) DEFAULT 0.00,
  `talla` decimal(4,1) NOT NULL,
  `color` varchar(60) DEFAULT NULL,
  `stockActual` int(11) DEFAULT 0,
  `fecha_ingreso` date DEFAULT NULL,
  `ID_Proveedor` int(11) DEFAULT NULL,
  PRIMARY KEY (`ID_Productos`),
  KEY `ID_Proveedor` (`ID_Proveedor`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`ID_Proveedor`) REFERENCES `Proveedor` (`ID_Proveedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Productos`
--

LOCK TABLES `Productos` WRITE;
/*!40000 ALTER TABLE `Productos` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Productos` VALUES
('CS-327','Tenis casuales para hombre',18.25,11.0,'Negro',97,'2025-02-15',10),
('DZ-005','Zapato deportivo para hombre',19.00,12.0,'Azul',118,'2025-02-15',6),
('san-12','Sandalias altas para mujer',13.00,8.0,'azul',40,'2025-07-02',2),
('SH-34','Tenis con broche ',9.30,9.0,'blanco',70,'2025-07-10',4),
('SH2001','Sandalia de hule niños',4.50,5.0,'Rojo',88,'2025-02-15',8),
('SH8991','Sandalia para mujer',8.90,7.0,'Beige',91,'2025-02-15',4),
('SN254','Sneakers con luces para niños',17.55,4.0,'Azul Neon',73,'2025-02-16',1),
('SS235','Botas impermeables para niños',10.00,4.5,'Verde',80,'2025-02-16',2),
('ZD234','Zapato deportivo mujer',18.70,9.0,'Rosa',97,'2025-02-17',7),
('ZO-12','Zapato de vestir para hombre',20.99,12.0,'Café',90,'2025-02-20',3),
('zp-05','Zapato deportivo para niños',10.00,4.0,'rojo',30,'2025-07-01',1),
('ZP-5511','Sandalias playeras unisex',8.00,10.0,'Blanco',89,'2025-02-20',9),
('zp11','Zapato',10.00,12.0,'gris',35,'2025-03-30',4),
('zp34','Zapato de mujer',10.00,8.0,'negro',47,'2025-04-12',2),
('ZPL-43','Zapato con dibujo animado',6.70,6.0,'rojo',55,'2025-07-10',5),
('ZT-001','Tacón bajo',19.99,8.0,'Negro',118,'2025-02-20',5);
/*!40000 ALTER TABLE `Productos` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Proveedor`
--

DROP TABLE IF EXISTS `Proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Proveedor` (
  `ID_Proveedor` int(11) NOT NULL,
  `Proveedor` varchar(50) NOT NULL,
  `P_Contacto` varchar(65) NOT NULL,
  `Correo` varchar(55) NOT NULL,
  `Telefono` varchar(25) NOT NULL,
  `Direccion_Proveedor` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID_Proveedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Proveedor`
--

LOCK TABLES `Proveedor` WRITE;
/*!40000 ALTER TABLE `Proveedor` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Proveedor` VALUES
(1,'Calzado del Pacífico','Marta López','mlopez@cdpacifico.com','78112233','Calle La Reforma, #12, San Salvador'),
(2,'Distribuciones Luna','Carlos Martínez','cmartinez@dluna.com','72233445','Av. Las Gardenias, pol. B, Santa Tecla'),
(3,'Zapatex S.A.','Laura Jiménez','ljimenez@zapatex.com','75566789','Col. Miralvalle, San Salvador'),
(4,'FootStyle Import','José González','jgonzalez@footstyle.com','76889900','Colonia San Francisco, Soyapango'),
(5,'Mega Calzado','Erika Figueroa','erika@megacalzado.com','73445566','Residencial Altavista, Ilopango'),
(6,'Importadora Centro','Andrés Mejía','amejia@importcentro.com','71239084','Av. Roosevelt, San Miguel'),
(7,'Pasos Seguros','Daniela Herrera','dherrera@pseguro.com','79980011','Calle Central, Santa Ana'),
(8,'Calzado y Moda','Mauricio Pérez','mperez@calymoda.com','72003456','Calle Rubén Darío, Mejicanos'),
(9,'Estilo Urbano','Sofía Ramírez','sramirez@urbano.com','71330099','Colonia Escalón, San Salvador'),
(10,'Zapatería Moderna','Iván Torres','itorres@zmoderna.com','78881234','Calle a Merliot, Antiguo Cuscatlán');
/*!40000 ALTER TABLE `Proveedor` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `Usuario` (
  `ID_Usuario` smallint(6) unsigned NOT NULL,
  `nombreUsuario` varchar(60) NOT NULL,
  `password` varchar(100) NOT NULL,
  `tipoUsuario` varchar(20) NOT NULL,
  PRIMARY KEY (`ID_Usuario`),
  UNIQUE KEY `NombreUsuario_UNIQUE` (`nombreUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `Usuario` VALUES
(1,'usuario1','password123','cliente'),
(2,'usuario2','password123','administrador'),
(3,'1','1','Cliente'),
(4,'2','2','Administrador');
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedido` (
  `ID_Pedido` int(11) NOT NULL AUTO_INCREMENT,
  `num_Detalle` int(11) NOT NULL,
  `ID_Productos` varchar(30) NOT NULL,
  `cantidad_pares` int(11) NOT NULL,
  `subtotal` decimal(6,2) DEFAULT 0.00,
  PRIMARY KEY (`ID_Pedido`,`num_Detalle`),
  KEY `detalle_pedido_ibfk_2` (`ID_Productos`),
  CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`ID_Pedido`) REFERENCES `Pedido` (`ID_Pedido`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`ID_Productos`) REFERENCES `Productos` (`ID_Productos`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedido`
--

LOCK TABLES `detalle_pedido` WRITE;
/*!40000 ALTER TABLE `detalle_pedido` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `detalle_pedido` VALUES
(1,1,'CS-327',2,36.50),
(1,2,'CS-327',1,18.25),
(2,1,'DZ-005',2,38.00),
(2,2,'ZT-001',1,19.99),
(4,1,'SN254',1,17.55),
(5,1,'SN254',1,17.55),
(6,1,'DZ-005',2,38.00),
(6,2,'ZD234',1,18.70),
(7,1,'SH8991',1,8.90),
(7,2,'CS-327',2,36.50),
(9,1,'ZT-001',2,39.98),
(10,1,'ZD234',1,18.70),
(11,1,'SN254',1,17.55),
(13,1,'SS235',1,10.00),
(14,1,'SN254',1,17.55),
(15,1,'SS235',3,30.00),
(16,1,'SS235',1,10.00),
(17,1,'SH2001',12,54.00),
(19,1,'SS235',1,10.00),
(20,1,'SS235',2,20.00),
(21,1,'SS235',1,10.00),
(22,1,'SS235',3,30.00),
(24,1,'SN254',1,17.55),
(24,2,'SN254',5,87.75),
(25,1,'ZD234',1,18.70),
(26,1,'CS-327',1,18.25),
(27,1,'ZD234',1,18.70);
/*!40000 ALTER TABLE `detalle_pedido` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Dumping routines for database 'Distribuidora'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-07-22 20:06:46
