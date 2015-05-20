-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2+deb7u1
-- http://www.phpmyadmin.net
--
-- Client: localhost
-- Généré le: Jeu 21 Mai 2015 à 00:44
-- Version du serveur: 5.5.41
-- Version de PHP: 5.4.4-14+deb7u11

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données: `bagtrekkin`
--

-- --------------------------------------------------------

--
-- Structure de la table `compagnies`
--

DROP TABLE IF EXISTS `compagnies`;
CREATE TABLE IF NOT EXISTS `compagnies` (
  `id_company` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id_company`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=4 ;

--
-- Contenu de la table `compagnies`
--

INSERT INTO `compagnies` (`id_company`, `name`) VALUES
(1, 'TAP'),
(2, 'TAM'),
(3, 'British Airways');

-- --------------------------------------------------------

--
-- Structure de la table `employees`
--

DROP TABLE IF EXISTS `employees`;
CREATE TABLE IF NOT EXISTS `employees` (
  `id_employee` int(11) NOT NULL AUTO_INCREMENT,
  `cpf` varchar(255) NOT NULL,
  `function` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `id_company` int(11) NOT NULL,
  `district` varchar(255) NOT NULL,
  PRIMARY KEY (`id_employee`),
  UNIQUE KEY `cpf` (`cpf`),
  KEY `id_company` (`id_company`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- RELATIONS POUR LA TABLE `employees`:
--   `id_company`
--       `compagnies` -> `id_company`
--

--
-- Contenu de la table `employees`
--

INSERT INTO `employees` (`id_employee`, `cpf`, `function`, `name`, `password`, `status`, `token`, `id_company`, `district`) VALUES
(1, '710.831.318-68', 'check-in', 'Arthur Raimbaud', '0a75f6cb015fd589b71b757f6cf2f5e9', 'active', 'f4cfbd4d244e690924bcef7ca171a665', 1, 'Paris, France - Orly'),
(2, '710.831.320-25', 'check-in', 'Pierre Verger', '0a75f6cb015fd589b71b757f6cf2f5e9', 'active', '5011b7b19a1908f080bef30c406909d4', 2, 'Paris, France - Orly');

-- --------------------------------------------------------

--
-- Structure de la table `etickets`
--

DROP TABLE IF EXISTS `etickets`;
CREATE TABLE IF NOT EXISTS `etickets` (
  `id_eticket` int(11) NOT NULL AUTO_INCREMENT,
  `ticket_number` varchar(255) NOT NULL,
  `id_passenger` int(11) NOT NULL,
  `summary` varchar(255) NOT NULL,
  PRIMARY KEY (`id_eticket`),
  UNIQUE KEY `id_passenger` (`id_passenger`),
  UNIQUE KEY `ticket_number` (`ticket_number`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- RELATIONS POUR LA TABLE `etickets`:
--   `id_passenger`
--       `passengers` -> `id_user`
--

--
-- Contenu de la table `etickets`
--

INSERT INTO `etickets` (`id_eticket`, `ticket_number`, `id_passenger`, `summary`) VALUES
(1, '047-6535417938', 1, 'Paris - Recife'),
(2, '047-2159354990', 2, 'Paris - Recife');

-- --------------------------------------------------------

--
-- Structure de la table `flights`
--

DROP TABLE IF EXISTS `flights`;
CREATE TABLE IF NOT EXISTS `flights` (
  `id_flight` int(11) NOT NULL AUTO_INCREMENT,
  `id_eticket` int(11) NOT NULL,
  `duration` time NOT NULL,
  `aircraft` varchar(255) NOT NULL,
  `airline` varchar(255) NOT NULL,
  `departure_loc` varchar(255) NOT NULL,
  `departure_time` time NOT NULL,
  `arrival_loc` varchar(255) NOT NULL,
  `arrival_time` time NOT NULL,
  `id_company` int(11) NOT NULL,
  `flight_date` date NOT NULL,
  PRIMARY KEY (`id_flight`),
  KEY `id_company` (`id_company`),
  KEY `id_eticket` (`id_eticket`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- RELATIONS POUR LA TABLE `flights`:
--   `id_eticket`
--       `etickets` -> `id_eticket`
--   `id_company`
--       `compagnies` -> `id_company`
--

--
-- Contenu de la table `flights`
--

INSERT INTO `flights` (`id_flight`, `id_eticket`, `duration`, `aircraft`, `airline`, `departure_loc`, `departure_time`, `arrival_loc`, `arrival_time`, `id_company`, `flight_date`) VALUES
(1, 1, '02:25:00', 'Airbus Industrie A319', 'TAP Portugal TP421', 'Paris, France - Orly, terminal W', '13:15:00', 'Lisbon, Portugal - Airport, terminal 1', '14:40:00', 1, '2015-02-25'),
(2, 1, '07:45:00', 'Airbus Industrie A330-200', 'TAP Portugal TP015', 'Lisbon, Portugal - Airport, terminal 1', '16:35:00', 'Recife, Brazil - Guararapes International', '21:20:00', 1, '2015-02-25'),
(3, 2, '07:45:00', 'Airbus Industrie A330-200', 'TAP Portugal TP015', 'Lisbon, Portugal - Airport, terminal 1', '16:35:00', 'Recife, Brazil - Guararapes International', '21:20:00', 1, '2015-02-19'),
(4, 2, '02:25:00', 'Airbus Industrie A319', 'TAP Portugal TP421', 'Paris, France - Orly, terminal W', '13:15:00', 'Lisbon, Portugal - Airport, terminal 1', '14:40:00', 1, '2015-02-19');

-- --------------------------------------------------------

--
-- Structure de la table `logs`
--

DROP TABLE IF EXISTS `logs`;
CREATE TABLE IF NOT EXISTS `logs` (
  `id_log` int(11) NOT NULL AUTO_INCREMENT,
  `horodator` datetime NOT NULL,
  `id_employee` int(11) NOT NULL,
  `id_luggage` int(11) NOT NULL,
  `id_flight` int(11) NOT NULL,
  `localisation` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_log`),
  KEY `id_employee` (`id_employee`),
  KEY `id_luggage` (`id_luggage`),
  KEY `id_flight` (`id_flight`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- RELATIONS POUR LA TABLE `logs`:
--   `id_employee`
--       `employees` -> `id_employee`
--   `id_luggage`
--       `luggages` -> `id_luggage`
--   `id_flight`
--       `flights` -> `id_flight`
--

--
-- Contenu de la table `logs`
--

INSERT INTO `logs` (`id_log`, `horodator`, `id_employee`, `id_luggage`, `id_flight`, `localisation`) VALUES
(1, '2015-02-19 12:00:00', 1, 1, 3, 'Paris, France - Orly, terminal W'),
(2, '2015-02-20 12:01:00', 1, 2, 3, 'Paris, France - Orly, terminal W'),
(3, '2015-02-25 12:49:00', 2, 5, 1, 'Paris, France - Orly, terminal W'),
(4, '2015-02-25 12:51:00', 2, 6, 1, 'Paris, France - Orly, terminal W');

-- --------------------------------------------------------

--
-- Structure de la table `luggages`
--

DROP TABLE IF EXISTS `luggages`;
CREATE TABLE IF NOT EXISTS `luggages` (
  `id_luggage` int(11) NOT NULL AUTO_INCREMENT,
  `material_number` bigint(20) NOT NULL,
  `id_passenger` int(11) NOT NULL,
  PRIMARY KEY (`id_luggage`),
  UNIQUE KEY `material_number` (`material_number`),
  KEY `id_passenger` (`id_passenger`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- RELATIONS POUR LA TABLE `luggages`:
--   `id_passenger`
--       `passengers` -> `id_user`
--

--
-- Contenu de la table `luggages`
--

INSERT INTO `luggages` (`id_luggage`, `material_number`, `id_passenger`) VALUES
(1, 1637492938, 1),
(2, 2147483647, 1),
(5, 5683478203, 2),
(6, 9374829103, 2);

-- --------------------------------------------------------

--
-- Structure de la table `passengers`
--

DROP TABLE IF EXISTS `passengers`;
CREATE TABLE IF NOT EXISTS `passengers` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `pnr` varchar(255) NOT NULL,
  `tel` varchar(255) NOT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `pnr` (`pnr`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Contenu de la table `passengers`
--

INSERT INTO `passengers` (`id_user`, `email`, `first_name`, `last_name`, `full_name`, `pnr`, `tel`) VALUES
(1, 'hr2@cin.ufpe.br', 'Hugo', 'Rodde', 'Hugo Rodde', 'x9jjb5', '+558147802343'),
(2, 'pjmg@cin.ufpe.br', 'Paul Jean Michel', 'Goujon', 'Paul Jean Michel Goujon', 'ysvi82', '+558189328925');

--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `employees`
--
ALTER TABLE `employees`
  ADD CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`id_company`) REFERENCES `compagnies` (`id_company`);

--
-- Contraintes pour la table `etickets`
--
ALTER TABLE `etickets`
  ADD CONSTRAINT `etickets_ibfk_1` FOREIGN KEY (`id_passenger`) REFERENCES `passengers` (`id_user`);

--
-- Contraintes pour la table `flights`
--
ALTER TABLE `flights`
  ADD CONSTRAINT `flights_ibfk_2` FOREIGN KEY (`id_eticket`) REFERENCES `etickets` (`id_eticket`),
  ADD CONSTRAINT `flights_ibfk_1` FOREIGN KEY (`id_company`) REFERENCES `compagnies` (`id_company`);

--
-- Contraintes pour la table `logs`
--
ALTER TABLE `logs`
  ADD CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`id_employee`) REFERENCES `employees` (`id_employee`),
  ADD CONSTRAINT `logs_ibfk_2` FOREIGN KEY (`id_luggage`) REFERENCES `luggages` (`id_luggage`),
  ADD CONSTRAINT `logs_ibfk_3` FOREIGN KEY (`id_flight`) REFERENCES `flights` (`id_flight`);

--
-- Contraintes pour la table `luggages`
--
ALTER TABLE `luggages`
  ADD CONSTRAINT `luggages_ibfk_1` FOREIGN KEY (`id_passenger`) REFERENCES `passengers` (`id_user`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
