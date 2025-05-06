-- Adminer 5.2.1 MySQL 8.0.42 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

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
(6,	'Пятков',	'Константин',	'Владиславович',	'722shock722@mail.ru',	'qwerty123',	'руководитель'),
(7,	'Андреев',	'Андрей',	'Андреевич',	'shock@mail.ru',	'qwerty123!',	'исполнитель'),
(8,	'Собакова',	'Собака',	'Собаковна',	'123sobaka123@mail.ru',	'qwerty123!',	'исполнитель'),
(9,	'HInjdsfosd',	'fpkmpsdg',	'Fnjsdngiuosdg',	'dfas@jkdofasf',	'qwerty123!',	'исполнитель')
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
(1,	'2025-04-28 14:12:19',	'19:00:21',	'20:00:54',	'Доброе утро, уважаемые коллеги. В первую очередь, хочу поблагодарить каждого из вас за то, что нашли время встретиться сегодня. Наша встреча очень важна для дальнейшего развития нашей компании в условиях стремительно меняющегося рынка информационных технологий. Я хотел бы обсудить текущие проблемы, поделиться нашими целями на ближайшее будущее и обратить внимание на некоторые ключевые аспекты, которые помогут нам укрепить наши позиции на рынке.'),
(2,	'2025-04-28 14:13:01',	'20:07:00',	'20:53:00',	'На пути к улучшению существующих процессов важно наладить командное взаимодействие. Мы должны создать атмосферу сотрудничества между различными отделами. Регулярные встречи не только внутри команд, но и с другими подразделениями позволят снизить барьеры, сделать общение более открытым и эффективным.\r\n\r\nСоздание межфункциональных команд для работы над проектами может стать важным шагом в решении этой проблемы. Это позволит взглянуть на одну и ту же задачу с разных сторон и найти более эффективные способы ее реализации. Кроме того, такое сотрудничество создает дополнительные возможности для роста и развития каждого члена команды.')
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
  PRIMARY KEY (`id`),
  KEY `fk_task_employee` (`employee_id`),
  KEY `fk_task_meeting` (`meeting_id`),
  CONSTRAINT `fk_task_employee` FOREIGN KEY (`employee_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_meeting` FOREIGN KEY (`meeting_id`) REFERENCES `Meeting` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Task` (`id`, `date_created`, `deadline`, `description`, `mark`, `status`, `employee_id`, `meeting_id`) VALUES
(1,	'2025-04-29 13:44:13',	'2025-05-31 00:00:00',	'Нужно написать API, которая будет отдавать джейсонину на фронт',	NULL,	'выполнена',	7,	2),
(2,	'2025-04-29 13:46:33',	'2025-05-25 00:00:00',	'Напиши функцию, которая принимает строку, содержащую числа и слова (например, \"a1b2c3\"), и возвращает сумму всех чисел в этой строке.',	NULL,	'выполняется',	8,	1),
(3,	'2025-04-29 13:47:06',	'2025-05-05 00:00:00',	'Напиши функцию, которая проверяет, можно ли сделать строку палиндромом, удалив не более одного символа.',	NULL,	'выполняется',	9,	2)
ON DUPLICATE KEY UPDATE `id` = VALUES(`id`), `date_created` = VALUES(`date_created`), `deadline` = VALUES(`deadline`), `description` = VALUES(`description`), `mark` = VALUES(`mark`), `status` = VALUES(`status`), `employee_id` = VALUES(`employee_id`), `meeting_id` = VALUES(`meeting_id`);

-- 2025-05-06 12:35:13 UTC