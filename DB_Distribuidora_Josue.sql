CREATE DATABASE IF NOT EXISTS Distribuidora;
USE Distribuidora;

DROP TABLE IF EXISTS `detalle_pedido`;
DROP TABLE IF EXISTS `Usuario`;
DROP TABLE IF EXISTS `Productos`;
DROP TABLE IF EXISTS `Pedido`;
DROP TABLE IF EXISTS `Estado`;
DROP TABLE IF EXISTS `Cliente`;
DROP TABLE IF EXISTS `Proveedor`;

CREATE TABLE `Cliente` (
  `ID_Cliente` int(11) NOT NULL,
  `Nombre` varchar(60) NOT NULL,
  `Correo` varchar(60) NOT NULL,
  `Telefono` varchar(25) NOT NULL,
  `Direccion` varchar(100) NOT NULL,
  PRIMARY KEY (`ID_Cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Cliente` VALUES
(1,'Wendy Sofia Rodriguez Salazar','analopez43.prueba@correo.com','12345678','calle2'),
(23,'Max','maxito','pruba34fcnejvretv','jdscniserfvn'),
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

CREATE TABLE `Estado` (
  `id_estado` tinyint(4) NOT NULL AUTO_INCREMENT,
  `estado` varchar(25) NOT NULL,
  PRIMARY KEY (`id_estado`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

INSERT INTO `Estado` VALUES
(1,'Pagado'),
(2,'Pendiente'),
(3,'Pagado parcialmente');

CREATE TABLE `Pedido` (
  `ID_Pedido` int(11) NOT NULL AUTO_INCREMENT,
  `ID_Cliente` int(11) NOT NULL,
  `fecha_hora` datetime NOT NULL,
  `total` decimal(7,2) DEFAULT 0.00,
  `id_estado` tinyint(4) NOT NULL,
  `pendiente_pagar` decimal(7,2) DEFAULT 0.00,
  `plazo_dias` int(11) DEFAULT NULL CHECK (`plazo_dias` <= 30),
  PRIMARY KEY (`ID_Pedido`),
  FOREIGN KEY (`ID_Cliente`) REFERENCES `Cliente` (`ID_Cliente`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`id_estado`) REFERENCES `Estado` (`id_estado`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4;

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
(12,12345,'2025-07-16 17:02:20',10.00,1,0.00,0),
(13,54,'2025-07-16 17:35:34',17.55,1,0.00,0),
(14,54,'2025-07-16 17:36:03',30.00,2,30.00,1),
(15,54,'2025-07-16 17:48:24',10.00,1,0.00,0),
(16,51,'2025-07-16 18:11:20',54.00,3,25.00,2),
(17,12345,'2025-07-16 20:53:06',10.00,1,0.00,0),
(18,12345,'2025-07-16 20:54:38',20.00,1,0.00,0),
(19,57,'2025-07-16 20:55:02',10.00,1,0.00,0),
(20,12345,'2025-07-16 20:55:24',30.00,1,0.00,0),
(21,12345,'2025-07-17 10:30:26',105.30,1,0.00,0),
(22,12345,'2025-07-17 14:20:03',18.70,1,0.00,0),
(23,58,'2025-07-18 15:24:32',18.25,1,0.00,0),
(24,3454,'2025-07-22 08:49:50',27.00,1,0.00,0),
(25,58,'2025-07-26 16:56:26',19.00,1,0.00,0),
(26,233,'2025-07-27 11:32:14',10.00,1,0.00,0),
(27,3454,'2025-07-27 18:31:45',17.00,1,0.00,0),
(28,51,'2025-07-27 18:57:51',10.00,1,0.00,0);

CREATE TABLE `Proveedor` (
  `ID_Proveedor` int(11) NOT NULL,
  `Proveedor` varchar(50) NOT NULL,
  `P_Contacto` varchar(50) NOT NULL,
  `Correo` varchar(55) NOT NULL,
  `Telefono` varchar(25) NOT NULL,
  `Direccion` varchar(100),
  PRIMARY KEY (`ID_Proveedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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

CREATE TABLE `Productos` (
  `ID_Productos` varchar(30) NOT NULL,
  `descripcion` varchar(50) NOT NULL,
  `precio` decimal(5,2) NOT NULL DEFAULT 0.00,
  `talla` decimal(4,1) NOT NULL,
  `color` varchar(50),
  `stockActual` int(11) DEFAULT 0,
  `fecha_ingreso` date,
  `ID_Proveedor` int(11),
  PRIMARY KEY (`ID_Productos`),
  FOREIGN KEY (`ID_Proveedor`) REFERENCES `Proveedor` (`ID_Proveedor`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Productos` VALUES
('bt-94','Botas de cuero para hombre',17.00,12.0,'café',6,'2025-07-03',3),
('CS-327','Tenis casuales para hombre',18.25,11.0,'Negro',97,'2025-02-15',10),
('DZ-005','Zapato deportivo para hombre',19.00,12.0,'Azul',117,'2025-02-15',6),
('SH-34','Tenis con broche ',9.30,9.0,'blanco',70,'2025-07-10',4),
('SH2001','Sandalia de hule niños',4.50,5.0,'Rojo',88,'2025-02-15',8),
('SH8991','Sandalia para mujer',8.90,7.0,'Beige',91,'2025-02-15',4),
('SN254','Sneakers con luces para niños',17.55,4.0,'Azul Neon',73,'2025-02-16',1),
('SS235','Botas impermeables para niños',10.00,4.5,'Verde',79,'2025-02-16',2),
('ZD234','Zapato deportivo mujer',18.70,9.0,'Rosa',98,'2025-02-17',7),
('ZO-12','Zapato de vestir para hombre',20.99,12.0,'Café',90,'2025-02-20',3),
('zp-05','Zapato deportivo para niños',10.00,4.0,'rojo',3,'2025-07-01',1),
('ZP-5511','Sandalias playeras unisex',8.00,10.0,'Blanco',89,'2025-02-20',9),
('zp11','Zapato',10.00,12.0,'gris',0,'2025-03-30',4),
('zp34','Zapato de mujer',10.00,8.0,'negro',46,'2025-04-12',2),
('ZPL-43','Zapato con dibujo animado',6.70,6.0,'rojo',55,'2025-07-10',5),
('ZT-001','Tacón bajo',19.99,8.0,'Negro',118,'2025-02-20',5);

CREATE TABLE `Usuario` (
  `ID_Usuario` smallint(6) unsigned NOT NULL,
  `nombreUsuario` varchar(60) NOT NULL,
  `password` varchar(100) NOT NULL,
  `tipoUsuario` varchar(20) NOT NULL,
  PRIMARY KEY (`ID_Usuario`),
  UNIQUE (`nombreUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO `Usuario` VALUES
(1,'usuario1','password123','cliente'),
(2,'usuario2','password123','administrador'),
(3,'1','1','Cliente'),
(4,'2','2','Administrador');

CREATE TABLE `detalle_pedido` (
  `ID_Pedido` int(11) NOT NULL,
  `num_Detalle` int(11) NOT NULL,
  `ID_Productos` varchar(30) NOT NULL,
  `cantidad_pares` int(11) NOT NULL,
  `subtotal` decimal(6,2) DEFAULT 0.00,
  PRIMARY KEY (`ID_Pedido`,`num_Detalle`),
  FOREIGN KEY (`ID_Pedido`) REFERENCES `Pedido` (`ID_Pedido`) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`ID_Productos`) REFERENCES `Productos` (`ID_Productos`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(12,1,'SS235',1,10.00),
(13,1,'SN254',1,17.55),
(14,1,'SS235',3,30.00),
(15,1,'SS235',1,10.00),
(16,1,'SH2001',12,54.00),
(17,1,'SS235',1,10.00),
(18,1,'SS235',2,20.00),
(19,1,'SS235',1,10.00),
(20,1,'SS235',3,30.00),
(21,1,'SN254',1,17.55),
(21,2,'SN254',5,87.75),
(22,1,'ZD234',1,18.70),
(23,1,'CS-327',1,18.25),
(25,1,'DZ-005',1,19.00),
(26,1,'SS235',1,10.00),
(27,1,'bt-94',1,17.00),
(28,1,'zp34',1,10.00);
