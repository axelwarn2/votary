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
  `birth_date` date DEFAULT NULL,
  `is_on_sick_leave` tinyint(1) NOT NULL DEFAULT '0',
  `is_on_vacation` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Employee` (`id`, `surname`, `name`, `lastname`, `email`, `password`, `role`, `birth_date`, `is_on_sick_leave`, `is_on_vacation`) VALUES
(1,	'Пятков',	'Константин',	'Владиславович',	'722shock722@mail.ru',	'$2b$12$mcaLB13KznkOyezuyaIzc.5CkQa0AKbpjm/Jyzy/Th85B9Jb1Kj3u',	'руководитель',	NULL,	0,	0),
(2,	'Андреев',	'Андрей',	'Андреевич',	'test@mail.ru',	'$2b$12$tLrQazp9xrXnqfWagQ9FC.6d0GXSZivSmzcQO6uhDvZBA7K/Rmr7W',	'исполнитель',	NULL,	0,	0),
(3,	'Евгеньев',	'Евгений',	'Евгеньевич',	'axelwarn@gmail.com',	'$2b$12$3v7li3C1LWPpUsizxcd.G.DgI/SRbQzwwoNtayEjAONcTd.zJxHO6',	'исполнитель',	NULL,	0,	0),
(4,	'Афанасьеф ',	'Михаил',	'Всеволодович',	'sigon@gmail.com',	'$2b$12$9yZS7jrwIzNWwp/StYl2FOk8e1R8kOKdvyRSBwUNEyuoNNG5ZgWn.',	'исполнитель',	NULL,	0,	0),
(5,	'Стражков',	'Всеволод',	'Денисович',	'mabenesu@mail.ru',	'$2b$12$syqfnZnKxbTHNCuSeFW9wOASniNQvxVys2Hdsz2.Q0iGGv4QIlDSq',	'исполнитель',	NULL,	0,	0),
(6,	'Емшанов',	'Максим',	'Денисович',	'jiwigino@gmail.com',	'$2b$12$R2QzOvQ9/TIUARsxJEswWeq0I73Kfl5vZ/9EhhIHzCFM6ia1ZID5O',	'исполнитель',	NULL,	0,	0),
(7,	'Надарян',	'Гор',	'Давитович',	'nadaryan@mail.ru',	'$2b$12$6lk6dwcLJA2A0YOosVd4xultMWYoq0aRIGX.gNj8P9GSCl7AAZa7m',	'исполнитель',	NULL,	0,	0),
(8,	'Калугина',	'Полина',	'Евгеньевна',	'kalugin@gmail.com',	'$2b$12$j9tR0jTzEe2fvpfn83cjkeAfFYLIqE3Hjo3bxeYkWe6kWLJ2XSs0a',	'исполнитель',	NULL,	0,	0),
(9,	'Домнина',	'Елизавета',	'Максимовна',	'dom72@mail.ru',	'$2b$12$A9J4ss8g2hTP1IZvjGuq8OBs.SI.VwsrqGZnnangHwrmzaO0RQnLi',	'исполнитель',	NULL,	0,	0);

DROP TABLE IF EXISTS `EmployeeEfficiency`;
CREATE TABLE `EmployeeEfficiency` (
  `id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int unsigned NOT NULL,
  `efficiency` float NOT NULL,
  `count_task` int NOT NULL,
  `complete` int NOT NULL,
  `expired` int NOT NULL,
  `calculated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `EmployeeEfficiency_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `Keyword`;
CREATE TABLE `Keyword` (
  `id` int NOT NULL AUTO_INCREMENT,
  `word` varchar(50) NOT NULL,
  `action` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `word` (`word`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `Keyword` (`id`, `word`, `action`) VALUES
(1,	'стоп',	'stop'),
(2,	'stop',	'stop'),
(3,	'стап',	'stop'),
(4,	'стоб',	'stop'),
(5,	'дополнить',	'append'),
(6,	'изменить',	'update'),
(7,	'удалить',	'delete');

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
(7,	'2025-06-02 12:46:48',	'12:46:48',	'12:47:10',	'Добрый день, начинаем наше собрание. Подскажите, пожалуйста, кто из вас кручит всех? Андреев, Андрей, нажмите кнопку Г и отправьте мне отчет до завтра о том, как правильно чистить рыбу. Стоп, можно завершать наше собрание.',	'/app/backend/upload/Собрание от 2025-06-02 12-46-47.wav');

DROP TABLE IF EXISTS `Project`;
CREATE TABLE `Project` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` varchar(1000) DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


DROP TABLE IF EXISTS `Task`;
CREATE TABLE `Task` (
  `id` int unsigned NOT NULL AUTO_INCREMENT COMMENT 'уникальный идентификатор',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'дата создания задачи',
  `deadline` datetime DEFAULT NULL COMMENT 'срок выполнения задачи',
  `description` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'описание задачи',
  `status` enum('выполняется','выполнена') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'статус задачи (в работе/выполнена)',
  `employee_id` int unsigned NOT NULL COMMENT 'ID сотрудника, ответственного за задачу',
  `meeting_id` int unsigned NOT NULL COMMENT 'ID собрания, на котором поставлена задача',
  `leader_id` int unsigned NOT NULL COMMENT 'ID руководителя, поставившего задачу',
  `project_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_task_employee` (`employee_id`),
  KEY `fk_task_meeting` (`meeting_id`),
  KEY `fk_task_leader` (`leader_id`),
  KEY `fk_project_id` (`project_id`),
  CONSTRAINT `fk_project_id` FOREIGN KEY (`project_id`) REFERENCES `Project` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_task_employee` FOREIGN KEY (`employee_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_leader` FOREIGN KEY (`leader_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_meeting` FOREIGN KEY (`meeting_id`) REFERENCES `Meeting` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Task` (`id`, `date_created`, `deadline`, `description`, `status`, `employee_id`, `meeting_id`, `leader_id`, `project_id`) VALUES
(16,	'2025-06-02 12:47:43',	'2025-06-03 19:00:01',	'Андреев, Андрей, нажмите кнопку Г и отправьте мне отчет до завтра о том, как правильно чистить рыбу.',	'выполняется',	2,	7,	1,	NULL);
