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
(1,	'Пятков',	'Константин',	'Владиславович',	'722shock722@mail.ru',	'$2b$12$mcaLB13KznkOyezuyaIzc.5CkQa0AKbpjm/Jyzy/Th85B9Jb1Kj3u',	'руководитель'),
(2,	'Андреев',	'Андрей',	'Андреевич',	'test@mail.ru',	'$2b$12$tLrQazp9xrXnqfWagQ9FC.6d0GXSZivSmzcQO6uhDvZBA7K/Rmr7W',	'исполнитель'),
(3,	'Евгеньев',	'Евгений',	'Евгеньевич',	'axelwarn@gmail.com',	'$2b$12$3v7li3C1LWPpUsizxcd.G.DgI/SRbQzwwoNtayEjAONcTd.zJxHO6',	'исполнитель'),
(4,	'Афанасьеф ',	'Михаил',	'Всеволодович',	'sigon@gmail.com',	'$2b$12$9yZS7jrwIzNWwp/StYl2FOk8e1R8kOKdvyRSBwUNEyuoNNG5ZgWn.',	'исполнитель'),
(5,	'Стражков',	'Всеволод',	'Денисович',	'mabenesu@mail.ru',	'$2b$12$syqfnZnKxbTHNCuSeFW9wOASniNQvxVys2Hdsz2.Q0iGGv4QIlDSq',	'исполнитель'),
(6,	'Емшанов',	'Максим',	'Денисович',	'jiwigino@gmail.com',	'$2b$12$R2QzOvQ9/TIUARsxJEswWeq0I73Kfl5vZ/9EhhIHzCFM6ia1ZID5O',	'исполнитель'),
(7,	'Надарян',	'Гор',	'Давитович',	'nadaryan@mail.ru',	'$2b$12$6lk6dwcLJA2A0YOosVd4xultMWYoq0aRIGX.gNj8P9GSCl7AAZa7m',	'исполнитель'),
(8,	'Калугина',	'Полина',	'Евгеньевна',	'kalugin@gmail.com',	'$2b$12$j9tR0jTzEe2fvpfn83cjkeAfFYLIqE3Hjo3bxeYkWe6kWLJ2XSs0a',	'исполнитель'),
(9,	'Домнина',	'Елизавета',	'Максимовна',	'dom72@mail.ru',	'$2b$12$A9J4ss8g2hTP1IZvjGuq8OBs.SI.VwsrqGZnnangHwrmzaO0RQnLi',	'исполнитель')
ON DUPLICATE KEY UPDATE `id` = VALUES(`id`), `surname` = VALUES(`surname`), `name` = VALUES(`name`), `lastname` = VALUES(`lastname`), `email` = VALUES(`email`), `password` = VALUES(`password`), `role` = VALUES(`role`);

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
(1,	'2025-05-13 14:02:32',	'14:02:32',	'14:02:54',	'Доброе утро, коллеги! Сегодня начинаем наше собрание. Пятков Константин, вам необходимо до завтра сделать мне кофе и принести в офис. Стоп! Андреев Андрей, подготовьте отчёт о ресурсах компании через неделю. Стоп! Афанасьеф Михаил, протестируйте обновление ПО завтра. Стоп! Стражков Всеволод, проверьте данные по поставкам в следующую пятницу. Стоп! Собрание завершено.',	'/app/backend/upload/Собрание от 2025-05-13 14-02-32.wav'),
(2,	'2025-05-11 12:05:03',	'12:05:03',	'12:05:44',	'Добрый день уважаемые коллеги! Сегодня на повестке дня у нас описание наших бизнес-процессов всех. Андреев, тебе необходимо завтра сделать отсчет о том, как правильно используются ресурсы нашей компании. Стоп! Продолжаем наше собрание, что-нибудь обговариваем. Пятков Константин, тебе необходимо до 31 июня 2025 сделать отсчет о том, как правильно фотографировать природу. Стоп!',	'/app/backend/upload/Собрание от 2025-05-11 12-05-03.wav'),
(3,	'2025-05-18 11:00:00',	'11:00:00',	'11:40:00',	'Доброе утро, коллеги! Сегодня обсуждаем маркетинговую стратегию. Калугина Полина, разработайте план рекламной кампании сегодня. Стоп! Евгеньев Евгений, проанализируйте данные по целевой аудитории через неделю. Стоп! Надарян Гор, подготовьте отчёт по KPI в следующую пятницу. Стоп! Собрание завершено.',	'/app/backend/upload/Собрание от 2025-05-18 11-00-00.wav'),
(4,	'2025-05-19 14:30:00',	'14:30:17',	'15:15:51',	'Здравствуйте! На повестке дня — оптимизация процессов. Афанасьеф Михаил, протестируйте новую CRM-систему. Стоп Домнина Елизавета, составьте руководство пользователя для CRM. Стоп! Стражков Всеволод, проверьте актуальность данных по клиентам. Стоп! До следующего раза.',	'/app/backend/upload/Собрание от 2025-05-19 14-30-00.wav'),
(5,	'2025-05-20 09:30:00',	'09:34:31',	'10:08:08',	'Всем добрый день! Обсуждаем итоги квартала. Надарян Гор, подготовьте отчёт по KPI Стоп. Андреев Андрей, проверьте финансовые показатели Стоп! Калугина Полина, организуйте встречу с партнёрами. Стоп! Собрание окончено.',	'/app/backend/upload/Собрание от 2025-05-20 09-30-00.wav'),
(6,	'2025-05-15 10:00:00',	'11:11:58',	'11:39:45',	'Здравствуйте, коллеги! На повестке дня — улучшение процессов. Емшанов Максим, подготовьте план обучения сотрудников завтра. Стоп! Домнина Елизавета, составьте инструкцию для новой системы через неделю. Стоп! Калугина Полина, организуйте тренинг для команды сегодня. Стоп! Собрание завершено.',	'/app/backend/upload/Собрание от 2025-05-15 10-00-00.wav')
ON DUPLICATE KEY UPDATE `id` = VALUES(`id`), `date_event` = VALUES(`date_event`), `time_start` = VALUES(`time_start`), `time_end` = VALUES(`time_end`), `text` = VALUES(`text`), `audio_path` = VALUES(`audio_path`);

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
  PRIMARY KEY (`id`),
  KEY `fk_task_employee` (`employee_id`),
  KEY `fk_task_meeting` (`meeting_id`),
  KEY `fk_task_leader` (`leader_id`),
  CONSTRAINT `fk_task_employee` FOREIGN KEY (`employee_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_leader` FOREIGN KEY (`leader_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_meeting` FOREIGN KEY (`meeting_id`) REFERENCES `Meeting` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `Task` (`id`, `date_created`, `deadline`, `description`, `status`, `employee_id`, `meeting_id`, `leader_id`) VALUES
(1,	'2025-05-13 14:03:37',	'2025-05-14 00:00:00',	'Константин, вам необходимо до завтра сделать мне кофе и принести в офис',	'выполнена',	1,	1,	1),
(2,	'2025-05-13 14:05:00',	'2025-05-20 00:00:00',	'Андреев Андрей, подготовьте отчёт о ресурсах компании через неделю.',	'выполняется',	2,	1,	1),
(3,	'2025-05-13 14:05:00',	'2025-05-14 00:00:00',	'Афанасьеф Михаил, протестируйте обновление ПО завтра.',	'выполняется',	4,	1,	1),
(4,	'2025-05-13 14:05:00',	'2025-05-20 00:00:00',	'Стражков Всеволод, проверьте данные по поставкам в следующую пятницу.',	'выполняется',	5,	1,	1),
(5,	'2025-05-18 11:05:00',	'2025-05-18 00:00:00',	'Калугина Полина, разработайте план рекламной кампании сегодня.',	'выполняется',	8,	3,	1),
(6,	'2025-05-18 11:05:00',	'2025-05-25 00:00:00',	'Евгеньев Евгений, проанализируйте данные по целевой аудитории через неделю.',	'выполняется',	3,	3,	1),
(7,	'2025-05-18 11:05:00',	'2025-05-23 00:00:00',	'Надарян Гор, подготовьте отчёт по KPI в следующую пятницу.',	'выполняется',	7,	3,	1),
(8,	'2025-05-15 10:05:00',	'2025-05-16 00:00:00',	'Емшанов Максим, подготовьте план обучения сотрудников завтра.',	'выполняется',	6,	6,	1),
(9,	'2025-05-15 10:05:00',	'2025-05-22 00:00:00',	'Домнина Елизавета, составьте инструкцию для новой системы через неделю.',	'выполняется',	9,	6,	1),
(10,	'2025-05-18 15:48:16',	'2025-05-31 00:00:00',	'Расскажите сказку',	'выполнена',	4,	4,	1),
(11,	'2025-05-18 15:50:46',	'2025-06-30 00:00:00',	'Расскажите о том, что вы любите на работе больше всего',	'выполняется',	6,	6,	1),
(12,	'2025-05-18 15:51:59',	'2025-06-25 00:00:00',	'Почините ноутбук до 25 июня 2025 года',	'выполнена',	6,	5,	1),
(13,	'2025-05-17 00:00:00',	'2025-05-31 00:00:00',	'Константин, сделай через 2 недели архитектуру приложения',	'выполняется',	1,	4,	1),
(14,	'2025-04-29 15:54:02',	'2025-06-30 00:00:00',	'Пятков Константин, тебе необходимо после завтра сделать отсчет о том, как правильно фотографировать природу',	'выполнена',	1,	2,	1),
(15,	'2025-05-18 16:00:01',	'2025-05-20 00:00:00',	'Константин выполните очистку своего рабочего места до послезавтра',	'выполняется',	1,	5,	1)
ON DUPLICATE KEY UPDATE `id` = VALUES(`id`), `date_created` = VALUES(`date_created`), `deadline` = VALUES(`deadline`), `description` = VALUES(`description`), `status` = VALUES(`status`), `employee_id` = VALUES(`employee_id`), `meeting_id` = VALUES(`meeting_id`), `leader_id` = VALUES(`leader_id`);
