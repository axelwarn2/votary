SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

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
(1,	'Пятков',	'Константин',	'Владиславович',	'722shock722@mail.ru',	'qwerty123',	'руководитель'),
(2,	'Андреев',	'Андрей',	'Андреевич',	'shock@mail.ru',	'qwerty123!',	'исполнитель');

DROP TABLE IF EXISTS `Meeting`;
CREATE TABLE `Meeting` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'уникальный идентификатор',
  `date_event` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'дата проведения собрания',
  `time_start` time NOT NULL COMMENT 'время начала собрания',
  `time_end` time NOT NULL COMMENT 'время окончания собрания',
  `text` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'текст собрания',
  `audio_path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'путь к аудиозаписи собрания',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Meeting` (`id`, `date_event`, `time_start`, `time_end`, `text`, `audio_path`) VALUES
(1,	'2025-05-08 10:03:18',	'10:03:18',	'10:04:08',	'Доброе утро уважаемые коллеги, начинаем нашу запись. Андреев Андрей, вам необходимо поменять мышку. Стоп. Продолжаем. Мы в середину получаются записи. Пятков Константин. Нажмите клаву вешу. Е. Стоп. Заканчиваем наше собрание.',	NULL);

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
  CONSTRAINT `fk_task_leader` FOREIGN KEY (`leader_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_meeting` FOREIGN KEY (`meeting_id`) REFERENCES `Meeting` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Task` (`id`, `date_created`, `deadline`, `description`, `mark`, `status`, `employee_id`, `meeting_id`, `leader_id`) VALUES
(1,	'2025-05-08 10:04:08',	'2025-05-15 10:04:08',	'Пятков Константин. Нажмите клаву вешу. Е.',	NULL,	'выполняется',	1,	5,	1);
