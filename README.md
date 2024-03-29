# Capstone - Final Project

Final project of Udacity full stack web developer nanodegree program.
This project objective is to build a REST API including an authentication & authorization in [Flask](https://flask.palletsprojects.com/en/2.0.x/), role-based control design patterns using [Auth0](https://www.auth0.com), hosted and in [Heroku](http://www.heroku.com/).

API URL: (https://starter-capstone.herokuapp.com/).

List of contents taught by the [Nanodegree course](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044) within its 5 modules/projects:

- Python 3
- Relational Database Architecture
- Modeling Data Objects with SQLAlchemy
- Internet protocols and communication
- Developing a Flask API
- Authentication and Access
- Authentication with Auth0
- Authentication in Flask
- Role-Based Access Control (RBAC)
- Testing Flask Applications
- Deploying applications using AWS and Heroku

## Tech Stack (Dependencies)

- **virtualenv** as a tool to create isolated Python environments
- [Python 3.6](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
- [Python-jose](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)

## Running the App locally

1. Clone this Repository
2. Initialize and activate a virtualenv: 
```
pip3 install virtualenv
python -m virtualenv env
```

3. Install all dependencies: 
```
pip3 install requirements.txt
``` 

5. Start server by running:

On Linux:
```
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```
On Windows:
```
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

## Running the App in Heroku

1. Deploy the App locally
2. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Create Heroku app

```
heroku create name_of_your_application
```

4. Add git remote for Heroku to local repository

```
git remote add heroku heroku_git_url
```

5. Add Postgresql add on for our database

```
heroku addons:create heroku-postgresql:hobby-dev --app name_of_your_application
heroku config --app name_of_your_application
```

6. Push application to Heroku

```
git push heroku master
```

7. Run migrations

```
heroku run python manage.py db upgrade --app name_of_your_application
```


## API Reference - Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Roles:

The authentication is made using [Auth0](https://www.auth0.com). Three different Roles are provided:

1. Casting Assistant
    - Can view actors and movies



2. Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies


3. Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database


To generate a new token for testing purposes (in case its already expired):

https://dev-2ao8q5no.us.auth0.com/authorize?audience=castingagency&response_type=token&client_id=CeSkJrV2n68oeHK4g152CLBIbLWxMdog&redirect_uri=https://localhost:8080/login-results


## Models:
- Movies with attributes title and release year
- Actors with attributes name, age and gender

## Endpoints:


### GET '/'

- Returns a simple message to confirm server is running.

Sample:

```
{
"message": "Healthy!",
"success": true
}
```

### GET '/actors'

- Returns a list of all actors from the database

Sample:

```
{
    "actors": [
        {
            "age": 68,
            "gender": "Fem",
            "id": 1,
            "name": "Fernanda Montenegro"
        }
    ],
    "success": true
}
```

### GET '/movies'

- Returns a list of all movies from the database. Requires access authorization (Casting assistant, Casting director or Executive Producer)

Sample:

```
{
    "movies": [
        {
            "id": 1,
            "release_date": "1994",
            "title": "Pulp Fiction"
        }
    ],
    "success": true
}
```

### DELETE '/actors/<int:actor_id>'

- Deletes a specific actor from the database. Requires specific access (Casting director or Executive Producer)
- Returns the deleted actor information (id, name, age, gender)

Sample:

```
{
    "deleted": {
        "age": 78,
        "gender": "Masc",
        "id": 2,
        "name": "Morgan Freeman"
    },
    "success": true
}
```

### DELETE '/movies/<int:movie_id>'

- Deletes a specific movie from the database. Requires specific access (Executive Producer only)
- Returns the deleted movie information (id, title, release date)

Sample:

```
{
    "deleted": {
        "id": 2,
        "release_date": "1997",
        "title": "Titanic"
    },
    "success": true
}
```

### POST '/actors'

- Create a new actor. Requires specific access (Casting director or Executive Producer)
- Returns the created actor information (id, name, age, gender)

Sample:

```
{
    "created actor": {
        "age": 78,
        "gender": "Masc",
        "id": 2,
        "name": "Morgan Freeman"
    },
    "success": true
}
```

### POST '/movies'

- Creates a new movie. Requires specific access (Executive Producer only)
- Returns the created movie information (id, title, release date)

Sample:

```
{
    "created movie": {
        "id": 2,
        "release_date": "1997",
        "title": "Titanic"
    },
    "success": true
}
```

### PATCH '/actors/<int:actor_id>'

- Updates the values from a specific actor register. Requires specific access (Casting director or Executive Producer)
- Returns the modified actor information (id, name, age, gender)

Sample:

```
{
    "actor": {
        "age": 69,
        "gender": "Fem",
        "id": 1,
        "name": "Fernanda Montenegro"
    },
    "success": true
}
```

### PATCH '/movies/<int:movie_id>'

- Updates the values from a specific movie register. Requires specific access (Casting director or Executive Producer)
- Returns the modified actor information (id, title, release date)

Sample:

```
{
    "movie": {
        "id": 1,
        "release_date": "1995",
        "title": "Pulp Fiction"
    },
    "success": true
}
```

## Tests:

- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role

How to run the tests:

```
python test_app.py
```