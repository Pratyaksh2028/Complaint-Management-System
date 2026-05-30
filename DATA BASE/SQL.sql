-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: cms_project_db
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `activity_audit`
--

DROP TABLE IF EXISTS `activity_audit`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity_audit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `action_details` varchar(255) NOT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `activity_audit_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `activity_audit`
--

LOCK TABLES `activity_audit` WRITE;
/*!40000 ALTER TABLE `activity_audit` DISABLE KEYS */;
INSERT INTO `activity_audit` VALUES (1,2,'User logged in','127.0.0.1','2026-04-19 10:29:35'),(2,2,'Filed complaint: Network Connectivity issue','127.0.0.1','2026-04-19 10:32:12'),(3,2,'User logged out','127.0.0.1','2026-04-19 10:32:35'),(4,2,'User logged in','127.0.0.1','2026-04-19 11:02:26'),(5,2,'User logged out','127.0.0.1','2026-04-19 11:26:44'),(6,3,'User logged in','127.0.0.1','2026-04-19 11:27:58'),(7,3,'User logged out','127.0.0.1','2026-04-19 11:42:25'),(8,3,'User logged in','127.0.0.1','2026-04-19 11:42:39'),(9,3,'User logged out','127.0.0.1','2026-04-19 11:49:54'),(10,3,'User logged in','127.0.0.1','2026-04-19 11:50:19'),(11,3,'User logged out','127.0.0.1','2026-04-19 11:56:41'),(12,2,'User logged in','127.0.0.1','2026-04-19 11:57:19'),(13,2,'User logged out','127.0.0.1','2026-04-19 12:29:20'),(14,2,'User logged in','127.0.0.1','2026-04-19 12:29:36'),(15,2,'Filed complaint: My system area Light is flickering','127.0.0.1','2026-04-19 12:48:09'),(16,2,'User logged out','127.0.0.1','2026-04-19 12:48:28'),(17,3,'User logged in','127.0.0.1','2026-04-19 12:48:50'),(18,3,'User logged out','127.0.0.1','2026-04-19 13:56:26'),(19,2,'User logged in','127.0.0.1','2026-04-19 13:56:42');
/*!40000 ALTER TABLE `activity_audit` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaints`
--

DROP TABLE IF EXISTS `complaints`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaints` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `category` varchar(100) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `status` enum('Pending','In Progress','Resolved','Rejected') DEFAULT 'Pending',
  `priority` enum('Low','Medium','High','Critical') DEFAULT 'Medium',
  `admin_remark` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `complaints_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaints`
--

LOCK TABLES `complaints` WRITE;
/*!40000 ALTER TABLE `complaints` DISABLE KEYS */;
INSERT INTO `complaints` VALUES (1,2,'Technical','Network Connectivity issue','My system network is very slow can\'t do anything like this ','In Progress','Critical','Alright we are looking into that ASAP','2026-04-19 10:32:12','2026-04-19 11:56:15'),(2,2,'Workstation','My system area Light is flickering','The light  near my cabin light is flickering its so irritating i can\'t focus on my work like this ','Resolved','High','Sorry for your inconvenience we fixed that light  ','2026-04-19 12:48:09','2026-04-19 12:49:33');
/*!40000 ALTER TABLE `complaints` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `message` varchar(255) NOT NULL,
  `is_read` tinyint(1) DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
INSERT INTO `notifications` VALUES (1,2,'Update on Complaint #1: Status is now In Progress',1,'2026-04-19 11:56:15'),(2,2,'Update on Complaint #2: Status is now Resolved',1,'2026-04-19 12:49:33');
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fullname` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `profile_pic` varchar(255) DEFAULT 'default.png',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Super Admin','admin@cms.com','admin123',NULL,'admin','default.png','2026-04-19 09:28:15'),(2,'Pratyaksh','pratyaksh12345@gmail.com','scrypt:32768:8:1$iGgFPJsYT0IA5QkC$db793ebb0806e94a6aeea581096c6a18dcfbc5c23cb4d3b594762f5c5c3ad5c9c995bd9fc4b0f15c4dbe9c0d98e3579d3b103197093460b30126959544181ef4','7788995674','user','default.png','2026-04-19 10:29:22'),(3,'Sanjay Singh','sanjay12345@gmail.com','scrypt:32768:8:1$bRWuf8blXq2q8D26$ec31243e71b419cca0d9571813ca8fd480a1fcc2dadd8cbe45fe67efaf0f19f39fbe7482f2b852301584332dae0b5681638be77baadf47171328ecad4a95a4df','7889800765','admin','default.png','2026-04-19 11:27:44');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-19 19:45:47
