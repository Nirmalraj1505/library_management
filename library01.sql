-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 25, 2024 at 03:27 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `library01`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`email`, `password`) VALUES
('nm7970@srmist.edu.in', 'nm7970');

-- --------------------------------------------------------

--
-- Table structure for table `bookdatabase`
--

CREATE TABLE `bookdatabase` (
  `bname` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `isbn` varchar(255) NOT NULL,
  `quantity` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookdatabase`
--

INSERT INTO `bookdatabase` (`bname`, `author`, `isbn`, `quantity`) VALUES
('computer network', 'james', '1234', 0);

-- --------------------------------------------------------

--
-- Table structure for table `bookreserve`
--

CREATE TABLE `bookreserve` (
  `email` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `book` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `date&time` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookreserve`
--

INSERT INTO `bookreserve` (`email`, `name`, `book`, `author`, `date&time`) VALUES
('', '', '', '', ''),
('ak8989@srmist.edu.in', '', 'computer network', 'james', '2024-08-18 21:42:36'),
('ak8989@srmist.edu.in', '', 'computer network', 'james', '2024-08-18 22:06:12'),
('ak8989@srmist.edu.in', '', 'computer network', 'james', '2024-08-18 22:06:18'),
('ak8989@srmist.edu.in', '', 'computer network', 'james', '2024-08-18 22:06:42'),
('ak8989@srmist.edu.in', '', 'computer network', 'james', '2024-08-18 22:08:11'),
('ak8989@srmist.edu.in', '', 'computer network', 'james', '2024-08-18 22:08:48'),
('ak8989@srmist.edu.in', '', 'computer network', 'james', '2024-08-18 22:08:52'),
('ak8989@srmist.edu.in', '', 'computer network', 'james', '2024-08-18 22:23:14'),
('ak8989@srmist.edu.in', '', 'linux', 'nirmal', '2024-08-20 09:53:58'),
('ak8989@srmist.edu.in', '', 'computer network', 'james', '2024-08-20 10:19:53');

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`email`, `password`) VALUES
('ak8989@srmist.edu.in', 'ak8989');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
