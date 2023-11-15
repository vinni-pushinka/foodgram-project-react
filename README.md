# Проект Foodgram

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

### Ссылка: 
Проект доступен по ссылке: vinnifoodgram.myftp.org

### Технологии:
Python, Django, Django REST Framework, JWT, SQLite3.

### Как запустить проект:
1. Клонировать репозиторий:
```git clone https://github.com/vinni-pushinka/foodgram-project-react.git```
2. Перейти в него в командной строке:
```cd foodgram-project-react/backend/foodgram ```
3. Cоздать и активировать виртуальное окружение:
```python -m venv venv```
```venv/Scripts/activate```
4. Установить зависимости из файла requirements.txt:
```python -m pip install --upgrade pip```
```pip install -r requirements.txt```
5. Выполнить миграции:
```python manage.py makemigrations```
```python manage.py migrate```
6. Создать суперпользователя:
```python3 manage.py createsuperuser```
7. Запустить проект:
```python manage.py runserver```
8.  Загрузить базу из файла:  
```python manage.py load_data_from_csv```

### Документация:
Документация API доступна по адресу `http://127.0.0.1:8000/redoc/`.

### Команда проекта:
[Valeria Goran](https://github.com/vinni-pushinka)

> Written with [StackEdit](https://stackedit.io/).