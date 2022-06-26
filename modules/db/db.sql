CREATE DATABASE vkusers;
CREATE USER vkdbadmin WITH PASSWORD 'vk2022boT!!!'
ALTER DATABASE vkusers OWNER TO vkdbadmin;

CREATE TABLE IF NOT EXISTS vk_users (
	vk_id INTEGER PRIMARY KEY,
	first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40),
    bdate VARCHAR(40),
    gender INTEGER,
    city_id INTEGER,
    city_title VARCHAR(60),
    vkdomain VARCHAR(100),
    last_visit VARCHAR(40)
);

CREATE TABLE IF NOT EXISTS favorites (
	vk_id INTEGER NOT NULL,
	fav_id INTEGER NOT NULL,
	CONSTRAINT favorites_pk PRIMARY KEY (vk_id, fav_id)
);

CREATE TABLE IF NOT EXISTS black_list (
	vk_id INTEGER NOT NULL,
	blk_id INTEGER NOT NULL,
	CONSTRAINT black_list_pk PRIMARY KEY (vk_id, blk_id)
);

CREATE TABLE IF NOT EXISTS last_search (
	vk_id INTEGER NOT NULL,
	lst_id INTEGER NOT NULL,
    srch_number INTEGER,
	CONSTRAINT last_search_pk PRIMARY KEY (vk_id, lst_id)
);

CREATE TABLE IF NOT EXISTS settings (
	vk_id INTEGER NOT NULL UNIQUE,
	access_token VARCHAR (100),
	srch_offset INTEGER,
	age_from INTEGER,
	age_to INTEGER,
	last_command VARCHAR(100)
);
