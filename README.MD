# CAR HIRE MANAGEMENT SYSTEM

## How To Deploy

### Option 1

#### Start up MySQL

1. Run the mysql container

- `docker run --name mysql-server --publish 127.0.0.1:3307:3306 -e MYSQL_ROOT_PASSWORD=password123 -e MYSQL_PASSWORD=password123 -d mysql:latest`
  - substutite `127.0.0.1` with your host

2. Exec into container

- `docker exec -it mysql-server mysql -u root -p`

#### Start up PHP My Admin to access database via GUI

1. Run the phpmyadmin and link mysql-server container
   `docker run --name some-phpmyadmin -d --link mysql-server:db -p 8080:80 phpmyadmin/phpmyadmin`

2. Navigate to phpmyadmin by going to `localhost:8080`

3. Login using mysql credentials

4. create new database

- `DROP DATABASE IF_EXISTS CAR_HIRE_MANAGEMENT;`
- `CREATE DATABASE CAR_HIRE_MANAGEMENT;`

5. Copy contents in directory `queries/CUSTOMER_TABLE.sql`

6. Execute code to create `CUSTOMER` table

#### Set up Application locally

1. Create a virtual environment and activiate it

- `python3 -m venv venv`
- `source venv/bin/activate`

2. Navigate to `src/` directory

3. Copy the contents of .env.example into .env

- `cp .env.example .env`

4. Set the values in your .env files to connect to MySQL

```bash
  MYSQL_HOST=localhost
  MYSQL_USER={root_user} # change if another user is created
  MYSQL_ROOT_PASSWORD={root_password}
  MYSQL_PASSWORD={root_password} # change another user with password is created
  MYSQL_DB=CAR_HIRE_MANAGEMENT # change if another Database name is used
```

5. Install the requirements from `src/requirements.txt`

- `pip install src/requirements.txt`

6. Run the Flask Application

- Options
  - `python app.py`
  - `export FLASK_APP=app.py FLASK_ENV=development FLASK_RUN_PORT=5000 FLASK_RUN_DEBUG=1 && flask run`
    - `FLASK_RUN_DEBUG` and `FLASK_RUN_PORT` are optional

### Option 2 Use Docker Image

#### Start up MySQL

1. Run the mysql container

- `docker run --name mysql-server --publish 127.0.0.1:3307:3306 -e MYSQL_ROOT_PASSWORD=password123 -e MYSQL_PASSWORD=password123 -d mysql:latest`
  - substutite `127.0.0.1` with your host

2. Exec into container

- `docker exec -it mysql-server mysql -u root -p`

2. Navigate to `src/` directory

3. Copy the contents of .env.example into .env

- `cp .env.example .env`

4. Set the values in your .env files to connect to MySQL

```bash
  MYSQL_HOST=host.docker.internal
  MYSQL_USER={root_user} # change if another user is created
  MYSQL_ROOT_PASSWORD={root_password}
  MYSQL_PASSWORD={root_password} # change another user with password is created
  MYSQL_DB=CAR_HIRE_MANAGEMENT # change if another Database name is used
```

#### Start up PHP My Admin to access database via GUI

1. Run the phpmyadmin and link mysql-server container
   `docker run --name some-phpmyadmin -d --link mysql-server:db -p 8080:80 phpmyadmin/phpmyadmin`

2. Navigate to phpmyadmin by going to `localhost:8080`

3. Login using mysql credentials

4. create new database

- `DROP DATABASE IF EXISTS CAR_HIRE_MANAGEMENT;`
- `CREATE DATABASE CAR_HIRE_MANAGEMENT;`

5. Copy contents in directory `queries/CUSTOMER_TABLE.sql`

6. Execute code to create `CUSTOMER` table

#### Build and Run Docker Image

1. Navigate to `src/` directory
2. build docker image

- `docker build -t car_hire_management:latest .`

3. run docker image

- `docker run -p 5000:5000 -e FLASK_DEBUG=0 abhi94n/car_hire_management:latest`
  - `FLASK_DEBUG=0` - for production using gunicron
  - `FLASK_DEBUG=1` - for debugging and development

### Option 3 Docker Compose

1. Navigate to `docker/` directory

2. Start up docker compose

- `docker compose up`

3. Stop and remove containers

- `docker compose down`
