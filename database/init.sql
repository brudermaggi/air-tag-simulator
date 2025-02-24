CREATE TABLE `airtags`.`tags` (
  `id` INT NOT NULL,
  `name` MEDIUMTEXT NULL,
  `lon` FLOAT ZEROFILL NULL,
  `lat` FLOAT ZEROFILL NULL,
  PRIMARY KEY (`id`));
