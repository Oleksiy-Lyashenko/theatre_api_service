
# Theatre Service API

API service for the theatre management written on DRF

DB Structure:
![Website Interface](static/img/demo/db_structure.png)

1. All urls:
![Website Interface](static/img/demo/urls.png)

2. Actor detail:
![Website Interface](static/img/demo/actor.png)

3. Genre detail:
![Website Interface](static/img/demo/genre.png)

4. Play detail:
![Website Interface](static/img/demo/play_detail.png)

5. Play list:
![Website Interface](static/img/demo/plays.png)

6. Theatre detail:
![Website Interface](static/img/demo/theatre.png)

7. Performance detail:
![Website Interface](static/img/demo/performance_detail.png)

8. Performance list:
![Website Interface](static/img/demo/performances.png)

9. Reservation detail:
![Website Interface](static/img/demo/reservation_detail.png)

10. Reservation list:
![Website Interface](static/img/demo/reservations.png)


## Installation using GitHub

Install PostgreSQL and create db

```bash
git clone https://github.com/Oleksiy-Lyashenko/theatre_api_service
cd theatre_api_service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
set DB_HOST=<your db hostname>
set DB_NAME=<your db name>
set DB_USER=<your db username>
set DB_PASSWORD=<your db user password>
set SECRET_KEY=<your secret key>
python manage.py migrate
python manage.py runserver
```


    
## Run with Docker

Install Docker

```bash
docker-compose build
docker-compose up
```


## Getting access using API on PC

- create user via /api/user/register/(only for read data)
- create admin user(for add and change information)
```bash
python manage.py createsuperuser
```
- get access token via /api/user/token/



## Getting access using API with Docker

- create container
- create admin user in container
```bash
docker exec -it <container_name> bash
python manage.py createsuperuser
```
- get access token via /api/user/token/
