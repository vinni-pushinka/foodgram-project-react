# Проект Foodgram

### Доступ: 
Проект доступен по ссылке: vinnifoodgram.myftp.org
Данные администратора:
e-mail: v-0903@rambler.ru
password: For_Review_2023

### Описание проекта:
Проект Foodgram позволяет:
 
 - авторизованным пользователям:
   1) публиковать собственные рецепты;
   2) подписываться на других авторов;
   3) добавлять рецепты других авторов в избранное;
   4) добавлять ингредиенты из рецептов в список покупок и выгружать его в формате .txt;

 - неавторизованным пользователям:
    1) просматривать рецепты различных авторов.
     
Рецепты можно фильтровать по тегам, которые присваиваются при создании или редактировании рецепта. Помимо тегов каждый рецепт содержит следующую информацию:
 - название;
 - автора, добавившего рецепт;
 - время приготовления;
 - список ингредиентов (предустановлен);
 - описание процедуры приготовления;
 - изображение готового блюда;

### Технологии:
Python, Django, Django REST Framework, JWT, SQLite3, PostgreSQL.

### Как запустить проект локально:
1. Клонировать репозиторий:
```git clone https://github.com/vinni-pushinka/foodgram-project-react.git```
2. Перейти в него в командной строке:
```cd foodgram-project-react/infra ```
3. Запустить проект:
```docker-compose up --build```
4. Создать суперпользователя (пароль сохранить в переменной окружения DJANGO_SUPERUSER_PASSWORD):
```docker exec -it infra-backend-1 python manage.py createsuperuser --noinput --username your_username --email your@email.com --first_name Name --last_name Surname```
5.  Загрузить базу ингредиентов из файла:  
```docker exec -it infra-backend-1 python manage.py load_data_from_csv```
6. Вручную в админке добавить теги в разделе "Теги"

### Как запустить проект на сервере:
1. Проект можно развернуть с использованием workflow:
```.github\workflows\main.yml``
2. Создать суперпользователя (пароль сохранить в .env DJANGO_SUPERUSER_PASSWORD):
```docker exec -it infra-backend-1 python manage.py createsuperuser --noinput --username your_username --email your@email.com --first_name Name --last_name Surname```
3.  Загрузить базу ингредиентов из файла:  
```docker exec -it infra-backend-1 python manage.py load_data_from_csv```
4. Вручную в админке добавить теги в разделе "Теги"

### Документация:
Документация API доступна по адресу `http://127.0.0.1:8000/redoc/`.

### Команда проекта:
[Valeria Goran](https://github.com/vinni-pushinka)

> Written with [StackEdit](https://stackedit.io/).