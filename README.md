python manage.py create_users

docker-compose exec backend python manage.py migrate --noinput
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py import_ingredients data/ingredients.csv

docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py create_users
