--  nickname（昵称，具有唯一性）、follow_num（关注数）、follower_num（粉丝数）
-- 、weibo_num（微博数），以及每个用户发布的所有微博信息，其中包括微博的content（内容，只需考虑文本内容）、
-- post_time（发布时间）
-- 、repost_num（转发数）、comment_num（评论数）、like_num（点赞数）

create database if not exists `test` default character set utf8mb4;

-- 用户表
create table wb_user (
    `id` int primary key AUTO_INCREMENT,
    `nickmame` varchar(64) unique,
    `follow_num` int null comment '关注数',
    `follower_num` int null comment '粉丝数',
    `weibo_num` int null comment '微博数')
-- 微博信息表
create table wb_info (
    `id` int primary key auto_increment,
    `post_time` datetime null comment '发布时间',
    `repost_num` int null comment '转发数',
    `comment_num` int null comment '评论数',
    `like_num` int null comment '点赞数',
    `user_id` int,
    `content` text,
    CONSTRAINT FK_Name FOREIGN key (`user_id`) REFERENCES `wb_user`(id) 
    on delete cascade on update cascade
)


--在已爬取的数据中，如果要统计用户（昵称：PPlabs2019）历史微博的总点赞数，请你写出对应的 SQL 查询语句。
select sum(like_num)  from 
    wb_user As A 
    left join wb_info as B on A.id=B.user_id 
    where A.nickname='PPlabs2019';

-- 在已爬取的数据中，需要按用户历史微博的总点
--赞数进行倒序排序，选出前 50 名用户，并显示其昵称、关注数、粉丝数。请你写出对应的 SQL 查询语句。
select sum(like_num) as t, nickname from 
    wb_user as A left join wb_info B on A.id=B.user_id 
    group by nickname 
    order by t desc 
    limit 50;  
-- 数据量较大时，请合理地建立索引来优化你在第 2、3 个问题中给出的 SQL 语句查询效率。
 select A.nickname, A.follower_num, A.follow_num, sum(like_num) as t
    from wb_user as A left join wb_info B 
    on A.id=B.user_id 
    group by A.nickname 
    order by t desc limit 50;

#  group by 语句报错需要所有字段必须聚合时添加至配置文件
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION

-- 当数据量较大时，请合理地建立索引来优化你在第 2、3 个问题中给出的 SQL 语句查询效率。
create index like_num_index on wb_info(like_num)