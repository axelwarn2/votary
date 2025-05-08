SET NAMES utf8mb4;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

DROP DATABASE IF EXISTS `votary_db`;
CREATE DATABASE `votary_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `votary_db`;

DROP TABLE IF EXISTS `Employee`;
CREATE TABLE `Employee` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'уникальный идентификатор',
  `surname` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'фамилия',
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'имя',
  `lastname` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'отчество',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'корпоративная почта',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'пароль',
  `role` enum('руководитель','исполнитель') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'роль (руководитель/исполнитель)',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Employee` (`id`, `surname`, `name`, `lastname`, `email`, `password`, `role`) VALUES
(1, 'Пятков', 'Константин', 'Владиславович', '722shock722@mail.ru', 'qwerty123', 'руководитель'),
(2, 'Андреев', 'Андрей', 'Андреевич', 'shock@mail.ru', 'qwerty123!', 'исполнитель'),
(3, 'Собакова', 'Собака', 'Собаковна', '123sobaka123@mail.ru', 'qwerty123!', 'исполнитель'),
(4, 'HInjdsfosd', 'fpkmpsdg', 'Fnjsdngiuosdg', 'dfas@jkdofasf', 'qwerty123!', 'исполнитель')
ON DUPLICATE KEY UPDATE `id` = VALUES(`id`), `surname` = VALUES(`surname`), `name` = VALUES(`name`), `lastname` = VALUES(`lastname`), `email` = VALUES(`email`), `password` = VALUES(`password`), `role` = VALUES(`role`);

DROP TABLE IF EXISTS `Meeting`;
CREATE TABLE `Meeting` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'уникальный идентификатор',
  `date_event` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'дата проведения собрания',
  `time_start` time NOT NULL COMMENT 'время начала собрания',
  `time_end` time NOT NULL COMMENT 'время окончания собрания',
  `text` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'текст собрания',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Meeting` (`id`, `date_event`, `time_start`, `time_end`, `text`) VALUES
(3, '2025-05-08 09:11:25', '14:10:00', '15:10:41', 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolorem odit distinctio esse tenetur delectus eligendi quia repudiandae alias culpa architecto minima laudantium, enim ducimus? Numquam corrupti quidem quasi debitis voluptatum.'),
(4, '2025-05-09 10:00:00', '10:00:00', '11:00:00', 'Обсуждение новых проектов и распределение задач.')
ON DUPLICATE KEY UPDATE `id` = VALUES(`id`), `date_event` = VALUES(`date_event`), `time_start` = VALUES(`time_start`), `time_end` = VALUES(`time_end`), `text` = VALUES(`text`);

DROP TABLE IF EXISTS `Task`;
CREATE TABLE `Task` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'уникальный идентификатор',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'дата создания задачи',
  `deadline` datetime DEFAULT NULL COMMENT 'срок выполнения задачи',
  `description` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'описание задачи',
  `mark` tinyint unsigned DEFAULT NULL COMMENT 'оценка выполнения задачи',
  `status` enum('выполняется','выполнена') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'статус задачи (в работе/выполнена)',
  `employee_id` int unsigned NOT NULL COMMENT 'ID сотрудника, ответственного за задачу',
  `meeting_id` int unsigned NOT NULL COMMENT 'ID собрания, на котором поставлена задача',
  `leader_id` int unsigned NOT NULL COMMENT 'ID руководителя, поставившего задачу',
  PRIMARY KEY (`id`),
  KEY `fk_task_employee` (`employee_id`),
  KEY `fk_task_meeting` (`meeting_id`),
  KEY `fk_task_leader` (`leader_id`),
  CONSTRAINT `fk_task_employee` FOREIGN KEY (`employee_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_meeting` FOREIGN KEY (`meeting_id`) REFERENCES `Meeting` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_leader` FOREIGN KEY (`leader_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Task` (`id`, `date_created`, `deadline`, `description`, `mark`, `status`, `employee_id`, `meeting_id`, `leader_id`) VALUES
(2, '2025-05-08 09:11:35', '2025-05-15 00:00:00', 'Просто текст для примера, вообще любой набор случайных букв, которые складываются в слова', NULL, 'выполняется', 3, 3, 1),
(3, '2025-05-09 10:30:00', '2025-05-16 00:00:00', 'Разработать API для нового модуля', NULL, 'выполняется', 2, 4, 1),
(4, '2025-05-09 10:35:00', '2025-05-20 00:00:00', 'Протестировать новый функционал', NULL, 'выполняется', 4, 4, 1)
ON DUPLICATE KEY UPDATE `id` = VALUES(`id`), `date_created` = VALUES(`date_created`), `deadline` = VALUES(`deadline`), `description` = VALUES(`description`), `mark` = VALUES(`mark`), `status` = VALUES(`status`), `employee_id` = VALUES(`employee_id`), `meeting_id` = VALUES(`meeting_id`), `leader_id` = VALUES(`leader_id`);