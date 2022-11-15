create database web_app;

\c web_app

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

create table app_user (id uuid primary key DEFAULT uuid_generate_v4(), username varchar(20) UNIQUE, password varchar(255), email varchar(90), jwt varchar(255), is_admin boolean DEFAULT false);

create table post (id uuid primary key  DEFAULT uuid_generate_v4(), title varchar(255), content text, user_id uuid, constraint fk_user foreign key(user_id) references app_user(id) ON DELETE CASCADE);



create table comment (id uuid primary key DEFAULT uuid_generate_v4(), content text, user_id uuid, constraint fk_user foreign key(user_id) references app_user(id) ON DELETE CASCADE, post_id uuid, constraint fk_post foreign key(post_id) references post(id) ON DELETE CASCADE);

