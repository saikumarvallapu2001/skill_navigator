CREATE DATABASE  IF NOT EXISTS `skill_navigator` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `skill_navigator`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: skill_navigator
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(512) NOT NULL,
  `full_name` varchar(100) DEFAULT NULL,
  `bio` text,
  `role` varchar(20) DEFAULT NULL,
  `profile_picture` varchar(200) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `email_updates` tinyint(1) DEFAULT NULL,
  `email_newsletter` tinyint(1) DEFAULT NULL,
  `email_marketing` tinyint(1) DEFAULT NULL,
  `skill_recommendations` tinyint(1) DEFAULT NULL,
  `career_suggestions` tinyint(1) DEFAULT NULL,
  `profile_visibility` tinyint(1) DEFAULT NULL,
  `show_skills` tinyint(1) DEFAULT NULL,
  `education` varchar(20) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin@example.com','pbkdf2:sha256:260000$oOcHo9ZVj8W1viXD$0395dacd830192c7de7aa4a94d3f8089cefeb5c67b1893272a237b6dd6abc653','Admin User',NULL,'admin',NULL,'2025-05-24 07:49:30','2025-06-06 06:14:18',1,1,0,1,1,1,1,NULL,'+917981550549'),(2,'user','user@example.com','scrypt:32768:8:1$gTXY8GYcZHRuwu6a$65945a4905abbc17f912a2c26542a39d31087ae71cc6492b300ed0dfc1787e52c86bbee5ea2fd627d74e11373d1064273ce0c6f88d724f69568888895b9b6e5f','Regular User',NULL,'user',NULL,'2025-05-24 07:49:30',NULL,1,1,0,1,1,1,1,NULL,NULL),(3,'Sai Kumar','saikumarvallapu2001@gmail.com','pbkdf2:sha256:260000$u1nfUaV4Pdb2C02t$daa28ef9de018d09057f799e0c7c63aebc8597089d23b9df699a25697a4c6682','Sai Kumar','python developer','user','PP_-_Copy.jpg','2025-05-24 08:21:40','2025-05-25 17:30:00',1,1,0,1,1,1,1,NULL,NULL),(5,'Eshwar','eshwar@gmail.com','pbkdf2:sha256:260000$tdac4VnBV0VSzxwk$9bdfdd27a981df1c35cec5aaa8db648252c81328477bf0abdd2ca7b9cb85c208','Eshwar',NULL,'user',NULL,'2025-05-24 19:26:56','2025-05-24 19:27:08',1,1,0,1,1,1,1,'intermediate',NULL),(6,'SaikumarVallapu','sai.19914422@gmail.com','pbkdf2:sha256:260000$UiFDonlhmclbALH5$255f275383addc7741a7722911cc408d2b58d3a938bfc0e6028f8dc67cd7589a','Sai Kumar','Full Stack Developer\r\n','user','6_PP_-_Copy.jpg','2025-05-27 03:09:03','2025-06-19 10:20:51',1,1,0,1,1,1,1,'school','+916301516308'),(7,'uttejmedarapu','uttejmedarapu511@gmail.com','pbkdf2:sha256:260000$b5HzDLPrP8Tc0xnr$1e56bd700a931d8d523492ed86a30917d75145f78b8f86729b871245a170dd8f','Uttej','Full stack developer','user',NULL,'2025-05-28 04:23:33','2025-05-28 05:46:02',1,1,0,1,1,1,1,'masters','+917386759345');
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

-- Dump completed on 2025-06-19 21:50:48
