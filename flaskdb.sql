

CREATE DATABASE IF NOT EXISTS `flaskdb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `flaskdb`;



CREATE TABLE IF NOT EXISTS `usertable` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`username` varchar(50) NOT NULL,
`password` varchar(255) NOT NULL,
`email` varchar(100) NOT NULL , 
PRIMARY KEY (`id`)
);



SELECT * FROM usertable;
ALTER TABLE usertable AUTO_INCREMENT=1;

DELETE FROM usertable WHERE id= 7;
SET SQL_SAFE_UPDATES = 0;

