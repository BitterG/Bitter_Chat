-- 创建数据库
create database Bitter_chat;

-- 切换数据库
use Bitter_chat;

CREATE TABLE users(
    user_id int unsigned primary key auto_increment not null,
    user_name varchar(30) not null,
    user_password varchar(30) not null,
    user_nickname varchar(20) not null
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

-- 添加账号
insert into users values(0, 苦瓜, '123456', '10001');
insert into users values(0, 'user1', '123456', '10002');
select * from user;
