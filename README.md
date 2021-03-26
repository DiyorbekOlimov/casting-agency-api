# Capstone - Casting Agency

## About

The Casting Agency API supports a basic agency by allowing users manage their movies and actors. There are three different user roles:

- Casting Assistant - `assistant@capstone.com`
- Casting Director - `director@capstone.com`
- Casting Producer - `producer@capstone.com`

> All roles password is `Lorem123`

Role based permissions:

Casting Assistant:

- `get:actors`
- `get:movies`

Casting Director:

- `get:actors`
- `get:movies`
- `post:actors`
- `patch:actors`
- `patch:movies`
- `delete:actors`

Casting Director:

- `get:actors`
- `get:movies`
- `post:actors`
- `post:movies`
- `patch:actors`
- `patch:movies`
- `delete:actors`
- `delete:movies`

## Getting Started

### Installing Dependencies

#### Clone the repo

Clone the repo to your local directory using this code

```bash
git clone https://github.com/diyor-bek/casting-agency.git
```

#### Python 3.x

Follow instructions to install the latest version of python for your platform in the python docs for [unix-like systems](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) or [windows os](https://docs.python.org/3/using/windows.html#the-full-installer)

#### PIP Dependencies

In the cloned casting-agency directory, run the following code to install all necessary dependencies:

```bash
pip install -r requirements.txt
```

This will install all of the required packages.

> It is recommended to install through [venv](https://docs.python.org/3/library/venv.html)

## Database setup

### Create database

Create database with name `capstone` using Psql CLI:

```psql
create database capstone;
```

### Initialize database

Initiate and migrate the database with the following commands in command line

```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

> Note: run the following code before running server

```bash
export DATABASE_URL=postgresql://<USERNAME>:<PASSWORD>@<POSTGRES_SERVER_URL default "localhost:5432">/capstone
```

## Running the server

To run the API server on a local development environmental the following commands must be additionally executed:

### Linux and mac users

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

### Windows users

```bash
set FLASK_APP=app.py
set FLASK_ENV=development
```

### Run the development API server

```bash
flask run
```

## API Architecture

### Endpoints

> NOTE: All requests must have an Authorization header. Sample response

```bash
curl -H 'Authorization: Bearer <YOUR_JWT_TOKEN>' http://127.0.0.1:5000/actors
```

#### GET `/actors`

- Fetches a dictionary includes actors
- Request arguments: page - page of actors list index, every page has a 5 actors
- Returns: a JSON object with three keys: `success`, `actors` and `all_actors` = count of all actors

Sample curl request:

```bash
curl http://127.0.0.1:5000/actors
```

Sample response:

```json
{
  "actors": [
    {
      "age": 25,
      "gender": "male",
      "id": 1,
      "name": "John Doe"
    },
    {
      "age": 24,
      "gender": "female",
      "id": 2,
      "name": "Jane Doe"
    }
  ],
  "all_actors": 2,
  "success": true
}
```

#### GET `/actors/<id>`

- Fetches detailed information about a actor by actor id
- Request arguments: None
- Returns: a JSON object with following keys: `success` and detailed information of actor

Sample curl request:

```bash
curl http://127.0.0.1:5000/actors/1
```

Sample response:

```json
{
  "age": 25,
  "gender": "male",
  "id": 1,
  "name": "John Doe",
  "success": true
}
```

#### POST `/actors`

- Creates a new actor in the database
- Request arguments: a JSON formatted object with required keys: `name`, `age` and `gender`
- Returns: a JSON object with `success` and `id` of created actor

Sample curl request:

```bash
curl -X POST -H 'Content-Type: application/json' -D '{"name": "James Smith", "age": 31, "gender": "male"}' http://127.0.0.1:5000/actors
```

Sample response:

```json
{
  "id": 3,
  "success": true
}
```

#### PATCH `/actors/<id>`

- Update the existing actor in database
- Request arguments: a JSON formatted object with optional keys: `name`, `age` and `gender`
- Returns: a JSON object with `success`

Sample curl request:

```bash
curl -X PATCH -H 'Content-Type: application/json' -D '{"age": 32}' http://127.0.0.1:5000/actors/3
```

Sample response:

```json
{
  "success": true
}
```

#### DELETE `/actors/<id>`

- Delete the existing actor from database
- Request arguments: None
- Returns: a JSON object with `success`

Sample curl request:

```bash
curl -X DELETE http://127.0.0.1:5000/actors/3
```

Sample response:

```json
{
  "success": true
}
```

#### GET `/movies`

- Fetches a dictionary includes movies
- Request arguments: page - page of movies list index, every page has a 5 movies
- Returns: a JSON object with three keys: `success`, `movies` and `all_movies` = count of all movies

Sample curl request:

```bash
curl http://127.0.0.1:5000/movies
```

Sample response:

```json
{
  "all_movies": 1,
  "movies": [
    {
      "id": 1,
      "release_date": "2025-01-01",
      "title": "Titanic"
    }
  ],
  "success": true
}
```

#### GET `/movies/<id>`

- Fetches detailed information about a movie by movie id
- Request arguments: None
- Returns: a JSON object with following keys: `success` and detailed information of movie

Sample curl request:

```bash
curl http://127.0.0.1:5000/movies/1
```

Sample response:

```json
{
  "id": 1,
  "release_date": "2025-01-01",
  "success": true,
  "title": "Titanic"
}
```

#### POST `/movies`

- Creates a new movie in the database
- Request arguments: a JSON formatted object with required keys: `title`, and `release_date`
- Returns: a JSON object with `success` and `id` of created movie

Sample curl request:

```bash
curl -X POST -H 'Content-Type: application/json' -D '{"title": "The Adventures of Udacity Student", "release_date": "2021-04-01"}' http://127.0.0.1:5000/movies
```

Sample response:

```json
{
  "id": 2,
  "success": true
}
```

#### PATCH `/movies/<id>`

- Update the existing movie in database
- Request arguments: a JSON formatted object with optional keys: `title`, and `release_date`
- Returns: a JSON object with `success`

Sample curl request:

```bash
curl -X PATCH -H 'Content-Type: application/json' -D '{"release_date": "2021-03-30"}' http://127.0.0.1:5000/movies/2
```

Sample response:

```json
{
  "success": true
}
```

#### DELETE `/movies/<id>`

- Delete the existing movie from database
- Request arguments: None
- Returns: a JSON object with `success`

Sample curl request:

```bash
curl -X DELETE http://127.0.0.1:5000/movies/1
```

Sample response:

```json
{
  "success": true
}
```

### Errors

> The API returned this errors

- 400 - bad request
- 401 - unauthorized + description
- 404 - not found
- 405 - method not allowed

## Testing

> You can test the API in 3 different methods.

### 1. CURL

Sample curl test:

```bash
curl -X GET -H 'Authorization: Bearer <JWT_TOKEN>' http://127.0.0.1:5000/actors
```

Response:

```json
{
  "actors": [
    {
      "age": 25,
      "gender": "male",
      "id": 1,
      "name": "John Doe"
    },
    {
      "age": 24,
      "gender": "female",
      "id": 2,
      "name": "Jane Doe"
    }
  ],
  "all_actors": 2,
  "success": true
}
```

> Note: you can find more endpoints from [endpoints section](#endpoints)

### 2. UnitTest

I have written a test on python `unittest` framework for endpoints. It can be found in the `test_app.py` file

Before running the test, create `capstone_test` database using Psql CLI:

```bash
create database capstone_test;
```

Use the following code to run the test:

```bash
python test_app.py
```

> Note: each time before testing, run the following code in Psql CLI

```bash
drop database capstone_test; create database capstone_test;
```

### 3. Postman

**Note**: Install the [**Postman**](https://getpostman.com/) app to your computer to use a postman test collection

1. Open the postman and import the test collection.
2. Change values of variables `URL`, `ASSISTANT_TOKEN`, `DIRECTOR_TOKEN` and `PRODUCER_TOKEN`.
3. Run the test.

## Deployment

**Note**: I deployed application to [heroku](https://heroku.com)

[Deployed application link](https://diyorbek-casting-agency.herokuapp.com)

### Deploy to heroku

1. Register to [heroku](https://signup.heroku.com).
2. Install [heroku cli](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).
3. Create heroku app. Open cloned directory and run the following code in terminal.

```bash
heroku create <YOUR_APP_NAME>
```

4. Add git remote for Heroku to local repository

```bash
git remote add heroku https://git.heroku.com/<YOUR_APP_NAME>.git

```

5. Add postgresql add on for database

```bash
heroku addons:create heroku-postgresql:hobby-dev --app <YOUR_APP_NAME>
```

6. Push to heroku

```bash
git push heroku master
```

7. Run migrations

```bash
heroku run python manage.py db init
heroku run python manage.py db migrate
heroku run python manage.py db upgrade
```

8. Check the **server is working**

```bash
curl <YOUR_APP_NAME>.herokuapp.com/
```

If server returned `server is working` server is worked!
