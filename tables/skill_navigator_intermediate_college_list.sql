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
-- Table structure for table `intermediate_college_list`
--

DROP TABLE IF EXISTS `intermediate_college_list`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `intermediate_college_list` (
  `s_no` int DEFAULT NULL,
  `college_code` int DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `college_name` text,
  `district_name` text,
  `college_nature_type` text,
  `college_type` varchar(50) DEFAULT 'intermediate',
  `hostel_availability` text,
  `sections` text,
  `college_address` text,
  `email_id` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `intermediate_college_list`
--

LOCK TABLES `intermediate_college_list` WRITE;
/*!40000 ALTER TABLE `intermediate_college_list` DISABLE KEYS */;
INSERT INTO `intermediate_college_list` VALUES (1,9305,'AP','KGBV JUNIOR COLLEGE - 09305','ANNAMAYYA','Government College','Girls','NO','','VAGALLA (V P),K. V. PALLE ( M ) CHITTOOR DISTRICT','S2954273@gmail.com'),(2,8234,'AP','GOVT JR COLLEGE - 08234','TIRUPATI','Government College','Co-Education','NO','','BESIDE M.R.O. OFFICE, NAIDUPET','gjcnaidupet@gmail.com'),(3,11132,'AP','KGBV VOCATIONAL JUNIOR COLLEGE - 11132','SRI SATHYA SAI','Government College','','NO','','.CHILAMATHUR (VILLAGE MANDAL) ANANTAPURAM DISTRICT','kgbvsochilamathur@gmail.com'),(4,24025,'AP','MODEL SCHOOL JUNIOR COLLEGE - 24025','VIZIANAGARAM','Government College','','NO','','NH-16,BHOGAPURAM,VIZIANAGARAM (DIST)','bhogapurammodelschool@gmail.co'),(5,111220,'AP','KGBV VOCATIONAL JUNIOR COLLEGE - 111220','SRI SATHYA SAI','Government College','','NO','','.NALLAMADA (VILLAGE MANDAL) ANANTAPURAMU DISTRICT','kgbvnallamada@gmail.com'),(6,11302,'AP','GOVT JUNIOR COLLEGE - 11302','ANANTHAPURAMU','Government College','Co-Education','NO','','Revenue colny atp road, kalayandurg','principal.kld@gmail.com'),(7,9501,'AP','KGBV VOCATIONAL JUNIOR COLLEGE - 09501','ANNAMAYYA','Government College','Girls','YES','','.SIDDAVARAM (VILLAGE POST ) PEDDAMANDYAM, GURRAMKONDA (SO ) CHITTOOR DISTRICT','kgbvpeddamandyam@gmail.com'),(8,11127,'AP','KGBV VOCATIONAL JUNIOR COLLEGE - 11127','SRI SATHYA SAI','Government College','','NO','','LEPAKSHI (VILLAGE MANDAL) ANANTAPURAMU DISTRICT.','solepakshi@gmail.com'),(9,10158,'AP','A P MODEL SCHOOL JR.COLLEGE-10158','NANDYAL','Government College','Co-Education','YES','','BETAMCHARLA, KURNOOL DIST.','apms.bethamcherla@gmail.com'),(10,2414,'AP','GOVT JUNIOR COLLEGE - 02414','ALLURI SITHARAMA RAJU','Government College','Co-Education','NO','','UPPER SILERU VILL POSTVISAKHAPATNAM DIST','principalgjcsileru@gmail.com'),(11,9250,'AP','KGBV VOCATIONAL JUNIOR COLLEGE - 09250','CHITTOOR','Government College','Girls','NO','','KUPPAM, VILLAGE, PARAMA SAMUDRAM, CHITTOOR DISTRICT.','kgbvkuppam@gmail.com'),(12,3518,'AP','GOVT JUNIOR COLLEGE - 03518','ALLURI SITHARAMA RAJU','Government College','Co-Education','NO','','Govt Junior College, Addateegala','gjcadt@gmail.com'),(13,24155,'AP','GOVT JUNIOR COLLEGE - 24155','VIZIANAGARAM','Government College','Co-Education','NO','','near S.C colony BADANGI','pplgjcbdn@gmail.com'),(14,26024,'AP','GOVT JR COLLEGE - 26024','BAPATLA','Government College','','NO','','Municipal High School Campus, Bapatla','gjcbapatla.new@gmail.com'),(15,8253,'AP','GOVT JR COLLEGE - 08253','TIRUPATI','Government College','Co-Education','NO','','NEAR RTC BUS STAND, BAPUJI STREET, SULLURPET.','prlgjcspet08253@gmail.com'),(16,NULL,'AP','K.G.B.V.JUNIOR COLLEGE','ANAKAPALLI','Government College','','NO','','NEAR WATER TANK, VANGALI ROAD, SABBAVARAM VILLAGE, VISAKHAPATNAM DIST.','sandya16.02@gmail.com'),(17,1281,'AP','GOVT JUNIOR COLLEGE FOR GIRLS - 01281','SRIKAKULAM','Government College','Girls','NO','','HOSPITAL ROAD','gjcgichapuram@gmail.com'),(18,10171,'AP','MODEL SCHOOL JUNIOR COLLEGE - 10171','NANDYAL','Government College','','NO','','Near APSWER SCHOOL,DHONE','apms.dhone@gmail.com'),(19,NULL,'AP','KGBV JUNIOR COLLEGE','BAPATLA','Government College','Girls','NO','','.Mandal complex,Chinnaganjam','kgbvchinaganjam@gmail.com'),(20,12053,'AP','MODEL SCHOOL JUNIOR COLLEGE - 12053','Y.S.R.','Government College','','NO','','Gangayapalli,Vallur','apms.vallur@gmail.com'),(21,10152,'AP','MODEL SCHOOL JUNIOR COLLEGE - 10152','NANDYAL','Government College','','NO','','Near KGBV School, Pamulapadu','sudhakardeo7@gmail.com'),(22,2364,'AP','GOVT JR COLLEGE - 02364','ALLURI SITHARAMA RAJU','Government College','Co-Education','NO','','MAIN ROAD','gjcdumbriguda@gmail.com'),(23,9472,'AP','GOVT JUNIOR COLLEGE - 09472','CHITTOOR','Government College','Co-Education','NO','','Bommasamudram Road, Mitta Indlu, Dhakshina Brahmana Palle,Bommasamudram (Vil. P.O.)','gjc.09472@gmail.com'),(24,9499,'AP','GOVT JR COLLEGE FOR GIRLS - 09499','ANNAMAYYA','Government College','Girls','NO','','kadapa road,gurramkonda.','gjcum09499@yahoo.com');
/*!40000 ALTER TABLE `intermediate_college_list` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-19 21:50:49
