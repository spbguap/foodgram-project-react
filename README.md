## О проекте:

Приложение "Продуктовый помощник"

## Запуск проекта

Клонировать репозиторий:

```
git clone git@github.com:spbguap/foodgram-project-react.git
```

создать в папке с клонированным проектом файл .env со следующим содержимым:

```
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
POSTGRES_DB=foodgram
DB_HOST=db_host
DB_PORT=5432
SECRET_KEY=django_secret_key_from_settings.py
DEFAULT_USER_PASSWORD='123456'
```

перейти в папку infra и выполнить команду

```
docker compose up -d
```

Выполнить команды для инициализации базы данных

```
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic
docker compose exec backend python manage.py import_ingredients data/ingredients.csv
```

Теперь можно перейти по адресу
http://127.0.0.1/
и начать использовать приложение
