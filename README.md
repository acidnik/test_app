Run app
-------

```
docker-compose build
docker-compose up
```

App will be available at http://localhost:8000

Tests
-----

```
docker-compose run api pytest
```

Test data
---------
edit app/db.py (sample_data)


API
---
авторизация на портале используя связку логин — пароль от лица одного из пользователей;

GET `/api/v1/user/login?login=aaa&password=bbb`  
Ответ:  
`{"session": "session_key"}`


получение данных пользователя (имя, адрес эл. Почты и т.п.)

GET `/api/v1/user/:user_id`  
Ответ:  
`{"user": {"id": 1, "login": "user", "email": "user@email"}}`


просмотр истории заказов пользователя; (для текущего авторизованного пользователя, можно дописать для любого)

GET `/api/v1/orders -H 'Authorization: session_key'`  
Ответ:  
`[{"book": {"id": 2, "author": "Лев Толстой", "title": "Война и мир"}, "shop": {"id": 1, "name": "Boson"}, "id": 2, "amount": 1}, {"book": {"id": 1, "author": "Венедикт Ерофеев", "title": "Москва-Петушки"}, "shop": {"id": 1, "name": "Boson"}, "id": 1, "amount": 1}]`


добавление нового заказа (N книг каждая из которых в M количестве);

POST `/api/v1/order -d '[{'book_id': 1, 'shop_id': 1, 'amount': 5}, {...}]'`  

Ответ:  
`[{"book": {"id": 1, "author": "Венедикт Ерофеев", "title": "Москва-Петушки"}, "shop": {"id": 1, "name": "Boson"}, "id": 1, "amount": 2}]`


просмотр ассортимента определенного магазина;

GET `/api/v1/shop/1` (без авторизации)  
Ответ:  
`[{"book_id": 1, "title": "Москва-Петушки", "author": "Венедикт Ерофеев"}, {"book_id": 2, "title": "Война и мир", "author": "Лев Толстой"}, {"book_id": 3, "title": "Евгений Онегин', 'author': 'Александр Пушкин'}]`

деавторизация.

POST `/api/v1/user/logout -H 'Authorization: session_key'`  

Ответ:  
`{}`


