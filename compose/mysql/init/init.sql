 -- compose/mysql/init/init.sql
 GRANT ALL PRIVILEGES ON blog.* TO sam@"%" IDENTIFIED BY "123456";
 FLUSH PRIVILEGES;
 alter database blog character set utf8mb4;