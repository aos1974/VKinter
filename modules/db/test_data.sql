test_dict = {'id': 20910114, 'bdate': '21.11.1991', 'city': {'id': 110, 'title': 'Пермь'}, 'sex': 2, 'screen_name': 'mgarbuzenko', 'first_name': 'Михаил', 'last_name': 'Гарбузенко', 'can_access_closed': True, 'is_closed': False}

# новая вставка
INSERT INTO vk_users (vk_id,first_name,last_name,bdate,gender,city_id,city_title,vkdomain,last_visit) VALUES
	(20910114,'Михаил','Гарбузенко','21.11.1991',2,110,'Пермь','https://vk.com/mgarbuzenko','2022-06-27 15:00:53');

UPDATE vk_users SET last_visit = '2022-06-27 15:18:53'
	WHERE vk_id = 20910114; 

SELECT * FROM vk_users WHERE vk_id = 20910114;

# выгрузка таблицы
INSERT INTO u420606_vkinder.vk_users (vk_id,first_name,last_name,bdate,gender,city_id,city_title,vkdomain,last_visit) VALUES
	 (37584229,'Елизавета','Титаренко','29.6.1999',1,222,'Казань','https://vk.com/id695117549',NULL),
	 (695117549,'Екатерина','Кабаева','15.2.1999',1,345,'Самара','https://vk.com/id695117549',NULL);

# тест повторной вставки
INSERT INTO vk_users (vk_id,first_name,last_name,bdate,gender,city_id,city_title,vkdomain,last_visit) VALUES
	(37584229,'Елизавета','Титаренко','29.6.1999',1,222,'Казань','https://vk.com/id695117549',NULL);


