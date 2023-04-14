# Проект YaMDb

API для YaMDb.

## Описание

Проект YaMDb собирает отзывы (Review) и оценки пользователей на произведения(Title) а также комментарии (Cooment) к отзывам.
Произведения делятся на категории (Category) и жанры (Genres).
Настроены следующие системы:
1. регистрации и аутентификации через JWT-токены
2. подтверждения через email
3. права доступа
4. импортирование данных в БД через csv файлы 

## Установка


Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/vzbdr/api_final_yatube.git
cd yatube_api
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

```
http://127.0.0.1:8000/redoc/
```


## Документация

Документация проекта представлена в формате Redoc.

```
http://127.0.0.1:8000/redoc/`
```