DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS vendor;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    first_name varchar(50),
    last_name VARCHAR(50),
    password TEXT NOT NULL
);

CREATE TABLE vendor (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    first_name varchar(50),
    last_name VARCHAR(50),
    password TEXT NOT NULL
);