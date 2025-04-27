-- Таблица сотрудников
CREATE TABLE IF NOT EXISTS `Employee` (
  `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'уникальный идентификатор',
  `surname` varchar(40) NOT NULL COMMENT 'фамилия',
  `name` varchar(30) NOT NULL COMMENT 'имя',
  `lastname` varchar(40) NULL COMMENT 'отчество',
  `email` varchar(50) NOT NULL COMMENT 'корпоративная почта',
  `password` varchar(100) NOT NULL COMMENT 'пароль',
  `role` enum('руководитель', 'исполнитель') NOT NULL COMMENT 'роль (руководитель/исполнитель)'
) COLLATE='utf8mb4_unicode_ci';

-- Таблица собраний
CREATE TABLE IF NOT EXISTS `Meeting` (
  `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'уникальный идентификатор',
  `date_event` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'дата проведения собрания',
  `time_start` time NOT NULL COMMENT 'время начала собрания',
  `time_end` time NOT NULL COMMENT 'время окончания собрания',
  `text` mediumtext NOT NULL COMMENT 'текст собрания'
) COLLATE='utf8mb4_unicode_ci';

-- Таблица задач
CREATE TABLE IF NOT EXISTS `Task` (
  `id` int unsigned NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT 'уникальный идентификатор',
  `date_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'дата создания задачи',
  `deadline` datetime NULL COMMENT 'срок выполнения задачи',
  `description` varchar(1000) NOT NULL COMMENT 'описание задачи',
  `mark` tinyint unsigned NULL COMMENT 'оценка выполнения задачи',
  `статус` enum('в работе', 'выполнена') NOT NULL COMMENT 'статус задачи (в работе/выполнена)',

  `employee_id` int unsigned NOT NULL COMMENT 'ID сотрудника, ответственного за задачу',
  `meeting_id` int unsigned NOT NULL COMMENT 'ID собрания, на котором поставлена задача',

  CONSTRAINT `fk_task_employee` FOREIGN KEY (`employee_id`) REFERENCES `Employee` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_task_meeting` FOREIGN KEY (`meeting_id`) REFERENCES `Meeting` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) COLLATE='utf8mb4_unicode_ci';
