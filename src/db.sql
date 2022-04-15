DROP TABLE IF EXISTS tbl_url CASCADE;

CREATE TABLE `shorturl`.`tbl_url` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `url` VARCHAR(4000) NULL,
  `url_short` VARCHAR(45) NULL,
  PRIMARY KEY (`id`));