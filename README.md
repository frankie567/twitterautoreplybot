docker-compose run django python manage.py syncdb
docker-compose run django python manage.py makemigrations
docker-compose run django python manage.py migrate
