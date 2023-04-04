CREATE DATABASE IF NOT EXISTS ChronAmWords;
SHOW DATABASES;
USE ChronAmWords;
CREATE TABLE IF NOT EXISTS token (
    `string` VARCHAR(50),
    `count` INT
);

CREATE TABLE IF NOT EXISTS occurrence (
    `string` VARCHAR(50),
    `date` DATE,
    `newspaper_id` VARCHAR(20),
    `ed` TINYINT,
    `seq` SMALLINT,
    `snippet` VARCHAR(250)
);

CREATE TABLE IF NOT EXISTS newspaper (
    `id` VARCHAR(20),
    `name` VARCHAR(100),
    `place` VARCHAR(100)
);