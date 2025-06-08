SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `votary_db`;
CREATE DATABASE `votary_db` 
USE `votary_db`;

DROP TABLE IF EXISTS `Employee`;
CREATE TABLE `Employee` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'Идентификатор сотрудника',
  `surname` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Фамилия',
  `name` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Имя',
  `lastname` varchar(40) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Отчество',
  `email` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Корпоративная почта',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Захэшированный пароль',
  `role` enum('руководитель','исполнитель') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Роль',
  `is_on_sick_leave` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Статус больничного',
  `is_on_vacation` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'Статус отпуска',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Employee` (`id`, `surname`, `name`, `lastname`, `email`, `password`, `role`, `is_on_sick_leave`, `is_on_vacation`) VALUES
(1,	'Пятков',	'Константин',	'Владиславович',	'722shock722@mail.ru',	'$2b$12$mcaLB13KznkOyezuyaIzc.5CkQa0AKbpjm/Jyzy/Th85B9Jb1Kj3u',	'руководитель',	0,	0),
(2,	'Андреев',	'Андрей',	'Андреевич',	'test@mail.ru',	'$2b$12$tLrQazp9xrXnqfWagQ9FC.6d0GXSZivSmzcQO6uhDvZBA7K/Rmr7W',	'исполнитель',	0,	0),
(3,	'Евгеньев',	'Евгений',	'Евгеньевич',	'axelwarn@gmail.com',	'$2b$12$3v7li3C1LWPpUsizxcd.G.DgI/SRbQzwwoNtayEjAONcTd.zJxHO6',	'исполнитель',	0,	0),
(4,	'Афанасьеф',	'Михаил',	'Всеволодович',	'sigon@gmail.com',	'$2b$12$9yZS7jrwIzNWwp/StYl2FOk8e1R8kOKdvyRSBwUNEyuoNNG5ZgWn.',	'исполнитель',	0,	0),
(5,	'Стражков',	'Всеволод',	'Денисович',	'mabenesu@mail.ru',	'$2b$12$syqfnZnKxbTHNCuSeFW9wOASniNQvxVys2Hdsz2.Q0iGGv4QIlDSq',	'исполнитель',	0,	0),
(6,	'Емшанов',	'Максим',	'Денисович',	'jiwigino@gmail.com',	'$2b$12$R2QzOvQ9/TIUARsxJEswWeq0I73Kfl5vZ/9EhhIHzCFM6ia1ZID5O',	'исполнитель',	0,	0),
(7,	'Надарян',	'Гор',	'Давитович',	'nadaryan@mail.ru',	'$2b$12$6lk6dwcLJA2A0YOosVd4xultMWYoq0aRIGX.gNj8P9GSCl7AAZa7m',	'исполнитель',	0,	0),
(8,	'Калугина',	'Полина',	'Евгеньевна',	'kalugin@gmail.com',	'$2b$12$j9tR0jTzEe2fvpfn83cjkeAfFYLIqE3Hjo3bxeYkWe6kWLJ2XSs0a',	'исполнитель',	0,	0),
(9,	'Домнина',	'Елизавета',	'Максимовна',	'dom72@mail.ru',	'$2b$12$A9J4ss8g2hTP1IZvjGuq8OBs.SI.VwsrqGZnnangHwrmzaO0RQnLi',	'исполнитель',	0,	0)
ON DUPLICATE KEY UPDATE `id` = VALUES(`id`), `surname` = VALUES(`surname`), `name` = VALUES(`name`), `lastname` = VALUES(`lastname`), `email` = VALUES(`email`), `password` = VALUES(`password`), `role` = VALUES(`role`), `is_on_sick_leave` = VALUES(`is_on_sick_leave`), `is_on_vacation` = VALUES(`is_on_vacation`);

DROP TABLE IF EXISTS `EmployeeEfficiency`;
CREATE TABLE `EmployeeEfficiency` (
  `employee_id` int unsigned NOT NULL COMMENT 'Идентификатор сотрудника',
  `efficiency` float NOT NULL COMMENT 'Процент эффективности',
  `count_task` int NOT NULL COMMENT 'Общее количество поручений',
  `completed` int NOT NULL COMMENT 'Количество выполненных поручений',
  `expired` int NOT NULL COMMENT 'Количество просроченных поручений',
  `calculated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата вычисления',
  PRIMARY KEY (`employee_id`),
  CONSTRAINT `fk_efficiency_employee` FOREIGN KEY (`employee_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `Keyword`;
CREATE TABLE `Keyword` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'Идентификатор ключевого слова',
  `word` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Слово',
  `action` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Действие',
  PRIMARY KEY (`id`),
  UNIQUE KEY `word` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Keyword` (`id`, `word`, `action`) VALUES
(1,	'стоп',	'stop'),
(2,	'stop',	'stop'),
(3,	'стап',	'stop'),
(4,	'стоб',	'stop'),
(5,	'дополнить',	'append'),
(6,	'изменить',	'update'),
(7,	'удалить',	'delete')
ON DUPLICATE KEY UPDATE `id` = VALUES(`id`), `word` = VALUES(`word`), `action` = VALUES(`action`);

DROP TABLE IF EXISTS `Meeting`;
CREATE TABLE `Meeting` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'Идентификатор собрания',
  `date_event` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата проведения',
  `time_start` time NOT NULL COMMENT 'Время начала',
  `time_end` time NOT NULL COMMENT 'Время окончания',
  `text` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Текст собрания',
  `audio_path` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Путь к аудиозаписи',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `Project`;
CREATE TABLE `Project` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'Идентификатор проекта',
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Название',
  `description` varchar(1000) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Описание',
  `created_at` datetime NOT NULL COMMENT 'Дата создания',
  `updated_at` datetime NOT NULL COMMENT 'Дата обновления',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Project` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES
(1,	'clubtort.ru',	'Проект, посвященный выполнению задач партнера clubtort',	'2025-04-10 00:00:00',	'2025-06-02 16:52:31'),
(2,	'megacvet.ru',	'Проект, посвященный выполнению задач партнера megacvet',	'2025-03-25 00:00:00',	'2025-06-02 16:53:29'),
(3,	'1cardioclinic.ru',	'Проект, посвященный выполнению задач партнера 1cardioclinic',	'2025-05-01 00:00:00',	'2025-05-21 00:00:00'),
(4,	'Теплоресурс',	'Проект, посвященный выполнению задач партнера teploresurs',	'2024-12-28 00:00:00',	'2024-12-31 00:00:00'),
(5,	'ishop72',	'Проект, посвященный выполнению задач партнера ishop',	'2025-01-20 00:00:00',	'2025-06-02 16:56:29')
ON DUPLICATE KEY UPDATE `id` = VALUES(`id`), `name` = VALUES(`name`), `description` = VALUES(`description`), `created_at` = VALUES(`created_at`), `updated_at` = VALUES(`updated_at`);

DROP TABLE IF EXISTS `Task`;
CREATE TABLE `Task` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'Идентификатор поручения',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Дата создания',
  `deadline` datetime DEFAULT NULL COMMENT 'Срок выполнения',
  `description` varchar(1000) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Описание',
  `status` enum('выполняется','выполнена') COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'Статус',
  `urgency` enum('да','нет') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'нет' COMMENT 'Срочность',
  `employee_id` int unsigned NOT NULL COMMENT 'Сотрудник (исполнитель)',
  `meeting_id` int unsigned NOT NULL COMMENT 'Собрание',
  `leader_id` int unsigned NOT NULL COMMENT 'Сотрудник (руководитель)',
  `project_id` int unsigned DEFAULT NULL COMMENT 'Проект',
  PRIMARY KEY (`id`),
  KEY `fk_task_employee` (`employee_id`),
  KEY `fk_task_meeting` (`meeting_id`),
  KEY `fk_task_leader` (`leader_id`),
  KEY `fk_task_project` (`project_id`),
  CONSTRAINT `fk_task_employee` FOREIGN KEY (`employee_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_task_leader` FOREIGN KEY (`leader_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_task_meeting` FOREIGN KEY (`meeting_id`) REFERENCES `Meeting` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_task_project` FOREIGN KEY (`project_id`) REFERENCES `Project` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


DROP TABLE IF EXISTS `TaskKeyword`;
CREATE TABLE `TaskKeyword` (
  `task_id` int unsigned NOT NULL COMMENT 'Поручение',
  `keyword_id` int unsigned NOT NULL COMMENT 'Ключевое слово',
  PRIMARY KEY (`task_id`,`keyword_id`),
  KEY `fk_keyword_id` (`keyword_id`),
  CONSTRAINT `fk_keyword_id` FOREIGN KEY (`keyword_id`) REFERENCES `Keyword` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_task_id` FOREIGN KEY (`task_id`) REFERENCES `Task` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
