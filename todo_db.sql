CREATE DATABASE todo_db;

USE todo_db;

CREATE TABLE todos (
id INT auto_increment PRIMARY KEY,
title VARCHAR(50) NOT NULL,
description TEXT,
completed BOOLEAN DEFAULT FALSE
)
