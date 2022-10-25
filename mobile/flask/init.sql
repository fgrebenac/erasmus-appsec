create databse mob_app;

create table app_user (id serial primary key, username varchar(20) UNIQUE, password varchar(255), email varchar(90));

create table post (id serial primary key, title varchar(255), content text, user_id integer, constraint fk_use foreign key(user_id) references app_user(id));
