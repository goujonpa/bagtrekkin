-- phpMyAdmin SQL Dump
-- version 3.4.11.1deb2+deb7u1
-- http://www.phpmyadmin.net
--
-- Client: localhost
-- Généré le: Sam 16 Mai 2015 à 03:34
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
  `id_company` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id_company`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `employees`
--

DROP TABLE IF EXISTS `employees`;
CREATE TABLE IF NOT EXISTS `employees` (
  `id_employee` int(11) NOT NULL,
  `cpf` varchar(255) NOT NULL,
  `function` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `unity` varchar(255) NOT NULL,
  `id_company` int(11) NOT NULL,
  PRIMARY KEY (`id_employee`),
  UNIQUE KEY `cpf` (`cpf`),
  KEY `id_company` (`id_company`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `etickets`
--

DROP TABLE IF EXISTS `etickets`;
CREATE TABLE IF NOT EXISTS `etickets` (
  `id_eticket` int(11) NOT NULL,
  `ticket_number` varchar(255) NOT NULL,
  `id_passenger` int(11) NOT NULL,
  `summary` varchar(255) NOT NULL,
  PRIMARY KEY (`id_eticket`),
  UNIQUE KEY `id_passenger` (`id_passenger`),
  UNIQUE KEY `ticket_number` (`ticket_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `flights`
--

DROP TABLE IF EXISTS `flights`;
CREATE TABLE IF NOT EXISTS `flights` (
  `id_flight` int(11) NOT NULL,
  `aircraft` varchar(255) NOT NULL,
  `airline` varchar(255) NOT NULL,
  `departure_loc` varchar(255) NOT NULL,
  `departure_time` time NOT NULL,
  `arrival_loc` varchar(255) NOT NULL,
  `arrival_time` time NOT NULL,
  `id_company` int(11) NOT NULL,
  `flight_date` date NOT NULL,
  PRIMARY KEY (`id_flight`),
  KEY `id_company` (`id_company`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `logs`
--

DROP TABLE IF EXISTS `logs`;
CREATE TABLE IF NOT EXISTS `logs` (
  `id_log` int(11) NOT NULL,
  `horodator` datetime NOT NULL,
  `id_employee` int(11) NOT NULL,
  `id_luggage` int(11) NOT NULL,
  `id_flight` int(11) NOT NULL,
  `localisation` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_log`),
  KEY `id_employee` (`id_employee`),
  KEY `id_luggage` (`id_luggage`),
  KEY `id_flight` (`id_flight`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `luggages`
--

DROP TABLE IF EXISTS `luggages`;
CREATE TABLE IF NOT EXISTS `luggages` (
  `id_luggage` int(11) NOT NULL,
  `material_number` int(11) NOT NULL,
  `id_passenger` int(11) NOT NULL,
  PRIMARY KEY (`id_luggage`),
  UNIQUE KEY `id_luggage` (`id_luggage`),
  UNIQUE KEY `material_number` (`material_number`),
  KEY `id_passenger` (`id_passenger`),
  KEY `index_luggages` (`id_luggage`,`material_number`,`id_passenger`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Structure de la table `passengers`
--

DROP TABLE IF EXISTS `passengers`;
CREATE TABLE IF NOT EXISTS `passengers` (
  `id_user` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `pnr` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id_user`),
  UNIQUE KEY `pnr` (`pnr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
