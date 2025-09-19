-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: momo_visualizer
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `category`
--

CREATE DATABASE IF NOT EXISTS momo_data_visualizer;

USE momo_data_visualizer;

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `transaction_type` enum('DEBIT','CREDIT') NOT NULL,
  `payment_type` enum('CASH','MoMoPay','Airtime') NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `uq_category` (`transaction_type`,`payment_type`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category`
--

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `message_id` int NOT NULL AUTO_INCREMENT,
  `transaction_id` int NOT NULL,
  `is_read` tinyint(1) DEFAULT '0',
  `subject` varchar(100) DEFAULT NULL,
  `body` varchar(800) DEFAULT NULL,
  `sms_protocol` varchar(20) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `contact_name` varchar(100) DEFAULT NULL,
  `sub_id` int DEFAULT NULL,
  PRIMARY KEY (`message_id`),
  UNIQUE KEY `transaction_id` (`transaction_id`),
  CONSTRAINT `fk_message_transaction` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`transaction_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_logs`
--

DROP TABLE IF EXISTS `system_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_logs` (
  `log_id` int NOT NULL AUTO_INCREMENT,
  `log_text` text NOT NULL,
  `log_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`log_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_logs`
--

LOCK TABLES `system_logs` WRITE;
/*!40000 ALTER TABLE `system_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction_category`
--

DROP TABLE IF EXISTS `transaction_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction_category` (
  `transaction_id` int NOT NULL,
  `category_id` int NOT NULL,
  PRIMARY KEY (`transaction_id`,`category_id`),
  KEY `fk_tc_category` (`category_id`),
  CONSTRAINT `fk_tc_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`category_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_tc_transaction` FOREIGN KEY (`transaction_id`) REFERENCES `transaction` (`transaction_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction_category`
--

LOCK TABLES `transaction_category` WRITE;
/*!40000 ALTER TABLE `transaction_category` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaction_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transaction` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `transaction_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `toa` varchar(50) DEFAULT NULL COMMENT 'Type of account',
  `sc_toa` varchar(50) DEFAULT NULL COMMENT 'Service center to account info',
  `readable_date` date DEFAULT NULL,
  `amount` decimal(12,2) NOT NULL,
  `status` enum('COMPLETED','FAILED','PENDING') NOT NULL,
  `service_center_number` varchar(20) DEFAULT NULL,
  `sender_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_status` (`status`),
  CONSTRAINT `fk_transaction_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(20) NOT NULL,
  `old_balance` decimal(12,2) DEFAULT '0.00',
  `current_balance` decimal(12,2) NOT NULL DEFAULT '0.00',
  `user_type` enum('personal','merchant','agent') NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (user_id, phone_number, old_balance, current_balance, user_type) VALUES
(6,'0781110001',5000.00,15000.00,'personal'),
(7,'0781110002',2000.00,5000.00,'merchant'),
(8,'0781110003',10000.00,8000.00,'agent'),
(9,'0781110004',0.00,2500.00,'personal'),
(10,'0781110005',7500.00,12500.00,'merchant');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `category` WRITE;
/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` (category_id, transaction_type, payment_type) VALUES
(1,'DEBIT','CASH'),
(2,'CREDIT','CASH'),
(3,'DEBIT','MoMoPay'),
(4,'CREDIT','MoMoPay'),
(5,'DEBIT','Airtime');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
INSERT INTO `transaction` (transaction_id, user_id, transaction_date, toa, sc_toa, readable_date, amount, status, service_center_number, sender_name) VALUES
(1,6,'2024-05-10 16:30:51','wallet','sc1','2024-05-10',2000.00,'COMPLETED','+250788110381','M-Money'),
(2,7,'2024-05-11 09:15:22','wallet','sc2','2024-05-11',1000.00,'COMPLETED','+250788110382','M-Money'),
(3,8,'2024-05-12 18:45:13','wallet','sc3','2024-05-12',500.00,'FAILED','+250788110383','M-Money'),
(4,9,'2024-05-13 12:05:44','wallet','sc4','2024-05-13',3000.00,'COMPLETED','+250788110384','M-Money'),
(5,10,'2024-05-14 20:10:59','wallet','sc5','2024-05-14',1500.00,'PENDING','+250788110385','M-Money');
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` (message_id, transaction_id, is_read, subject, body, sms_protocol, address, contact_name, sub_id) VALUES
(1,1,1,NULL,'You have received 2000 RWF from Jane.','0','M-Money','(Unknown)',6),
(2,2,1,NULL,'Your payment of 1000 RWF to Shop Ltd is complete.','0','M-Money','Shop Ltd',6),
(3,3,0,NULL,'Transaction of 500 RWF failed.','0','M-Money','(Unknown)',6),
(4,4,1,NULL,'You have received 3000 RWF from John.','0','M-Money','John Doe',6),
(5,5,0,NULL,'Your payment of 1500 RWF is pending.','0','M-Money','(Unknown)',6);
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `transaction_category` WRITE;
/*!40000 ALTER TABLE `transaction_category` DISABLE KEYS */;
INSERT INTO `transaction_category` (transaction_id, category_id) VALUES
(1,2),
(2,1),
(3,3),
(4,2),
(5,5);
/*!40000 ALTER TABLE `transaction_category` ENABLE KEYS */;
UNLOCK TABLES;

LOCK TABLES `system_logs` WRITE;
/*!40000 ALTER TABLE `system_logs` DISABLE KEYS */;
INSERT INTO `system_logs` (log_id, log_text, log_time) VALUES
(1,'Parsed transaction 1','2024-05-10 16:31:00'),
(2,'Parsed transaction 2','2024-05-11 09:16:00'),
(3,'Transaction 3 failed','2024-05-12 18:46:00'),
(4,'Transaction 4 credited','2024-05-13 12:06:00'),
(5,'Transaction 5 pending','2024-05-14 20:11:00');
/*!40000 ALTER TABLE `system_logs` DISABLE KEYS */;
UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-19 10:45:03
