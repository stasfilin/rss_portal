# RSS Portal
RSS Portal.

Backend:
* Django
* Python
* Redis
* PostgreSQL
* Celery

Frontend:
* Vue.js

The project can automated fetch RSS feeds using celery or triggered manually from Frontend dashboard


## Project Setup
### Docker
You need to install `docker-compose`. Run command
```shell script
pip install docker-compose
```

After that you can run commands

```shell script
docker-compose build
docker-compose up -d
```

After that you can run `docker-compose ps`. You will see

```shell script
        Name                       Command                 State             Ports
------------------------------------------------------------------------------------------
rss_portal_backend_1    sh -c sh runserver.sh            Up           8000/tcp
rss_portal_celery_1     celery -A backend worker - ...   Up
rss_portal_data_1       true                             Restarting
rss_portal_frontend_1   docker-entrypoint.sh sh -c ...   Up           8080/tcp
rss_portal_nginx_1      /usr/sbin/nginx                  Up           0.0.0.0:8000->80/tcp
rss_portal_postgres_1   docker-entrypoint.sh postgres    Up           5432/tcp
rss_portal_redis_1      docker-entrypoint.sh redis ...   Up           6379/tcp
```

You can open `0.0.0.0:8000`

### Without Docker
You need to create environment with `Python 3.8`

After that you need to run commands.

#### Backend
```shell script
cd backend
pip install -r requirements/base.txt
pip install -r requirements/development.txt
python manage.py migrate
python manage.py createsu
python manage.py runserver
```
#### Frontend
```shell script
cd frontend
yarn
yarn serve
```

## After Setup
* YOU NEED RUN SERVER
* Open [http://0.0.0.0:8000][http://0.0.0.0:8000]
* Register new user or you can use `admin`/`admin123456`
#### 


## API Documentation
* [http://0.0.0.0:8000/doc/redoc/][http://0.0.0.0:8000/doc/redoc/]
* [http://0.0.0.0:8000/doc/swagger/][http://0.0.0.0:8000/doc/swagger/]

## Testing

### Without docker
```shell script
cd backend/
python manage.py test
```
### From Docker
```shell script
docker-compose exec backend python manage.py test
```

## USERS
### Admin
```shell script
Username:     admin
Password:     admin123456
```

## Contribution

Any help is appreciated. Or feel free to create a Pull Request.

[http://0.0.0.0:8000/doc/redoc/]: http://0.0.0.0:8000/doc/redoc/

[http://0.0.0.0:8000/doc/swagger/]: http://0.0.0.0:8000/doc/swagger/

[http://0.0.0.0:8000]: http://0.0.0.0:8000