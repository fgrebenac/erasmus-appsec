create databse mob_app;

create table app_user (id uuid primary key DEFAULT uuid_generate_v4(), username varchar(20) UNIQUE, password varchar(255), email varchar(90), jwt varchar(255));

create table post (id uuid primary key  DEFAULT uuid_generate_v4(), title varchar(255), content text, user_id uuid, constraint fk_use foreign key(user_id) references app_user(id));

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

