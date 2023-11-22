-- Create quiz_db database_dev
CREATE DATABASE IF NOT EXISTS quiz_db;
CREATE USER IF NOT EXISTS 'quizify'@'localhost' IDENTIFIED BY 'quizify_pwd';
GRANT ALL PRIVILEGES ON `quiz_db`.* TO 'quizify'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'quizify'@'localhost';
FLUSH PRIVILEGES;
