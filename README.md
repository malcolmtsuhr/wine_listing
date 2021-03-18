# Wine Listing App

## Introduction

This is my capstone project for the [Udacity Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).
It's an app allowing wine makers and distributors to publicly list data about vintners and their wines.

### Overview

The front end "Vino Cellar" has a public face to view vintner and wine data, with an Auth0 authenticated access to add, edit, and delete data based on roles.
The app lists vintners categorized by area, and wines categorized by type.
Each is accessible by list view with search filtering, and a detailed profile page to view specific data; wines can also be accessed from their vintners listing page.
Once logged in, vintners can be added from the index or vintner list pages, while wines can only be added from their vintners profile page.
Data is referentially linked, and pages are dynamically populated from the current database instance.

Future iterations of the app will expand to provide wine reviews covering tasting notes and food pairings.

The database schema includes tables for:
 * vintners: RBAC access to create, update, and delete
 * wines: RBAC access to create, update, and delete
 * areas: backend auto-populated and case-normalized to group vintners
 * types: pre-populated for normalized descriptive wine categories

### Heroku Hosted Access:
(https://vino-cellar.herokuapp.com/)

<img src="/static/img/Vino_Cellar_index.png">

## Full Stack Web Development Skills utilized
 * Coding in Python 3
 * Relational database architecture
 * Modeling data objects with SQLAlchemy
 * Internet protocols and communication
 * Developing a Flask API
 * RESTful API development
 * Authentication and access with Auth0
 * Authentication in Flask
 * Role-based access control (RBAC)
 * Testing Flask applications
 * Frontend development with Bootstrap & Jinja
 * Deploying applications

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Our tech stack will include the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** as our ORM library
 * **PostgreSQL** as our database management system
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** and **Flask-Script** for creating and running schema migrations

#### Developed with Python 3.9

#### Github repo setup **Create an empty repository in your Github account online. To change the remote repository path in your local repository, use the commands below:**
```
git remote -v
git remote remove origin
git remote add origin <https://github.com/<USERNAME>/<REPO_NAME>.git>
git branch -M master
```
Once you have finished editing your code, you can push the local repository to your Github account using the following commands.
```
git add . --all   
git commit -m "your comment"
git push -u origin main
```

#### Virtual Enviornment

Navigate to the working directory & Install:
```
python3 -m pip install --user virtualenv
```

Create Virtual Environment:
```
python3 -m venv env
```

Activate Virtual Environment:
```
source env/bin/activate
```

Once you have your virtual environment setup and running, install `pip3` dependencies and environment variables by running:
```
source setup.sh
```

### 2. Frontend Dependencies
Our frontend tech stack will include the following:
 * **HTML**
 * **Jinja2**
 * **CSS**
 * **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/)
Bootstrap can be installed by Node Package Manager (NPM). Therefore, if not already, download and install the [Node.js](https://nodejs.org/en/download/).
Alternatively, use Homebrew to install with ```brew install node```
Windows users must run the executable as an Administrator, and restart the computer after installation.
After successfully installing the Node, verify the installation as shown below.
```
node -v
npm -v
```
Install [Bootstrap 3](https://getbootstrap.com/docs/3.3/getting-started/) for the website's frontend, from the working directory:
```
npm init -y
npm install bootstrap@3
```


### 3. Database Migration Manager
Initialize the database schema, and run to migrate and upgrade the database:
```
python3 manage.py db init
python3 manage.py db migrate
python3 manage.py db upgrade
```

## Testing
To run the tests, navigate to the active working directory venv, and run:
```
dropdb vino_test && createdb vino_test
psql vino_test < vino.psql
python3 test_app.py
```

## API Endpoints
Users are able to access the home page and data records anonymously. The create, edit, and delete functionality is limited to authenticated users with role based permissions.

### Roles and Permissions
Login from any page with the ```Manager Log In``` Button in the header bar
Once logged in, user will see ```Manager Dashboard``` Button in the header bar instead.
The Manager Dashboard will list user info, and the ```Logout``` Button.

####**Managers**
```
Cellar Manager login credentials for assessment review
User: manager@email.com
Password: AuthPass123!
```
Managers have access to create and update data, with these permissions:
  * get:vintners-edit
  * get:vintners-create
  * post:vintners-edit
  * post:vintners-create
  * get:wines-edit
  * post:wines-edit
  * post:wines-create
  * get:wines-create
  * get:auth

####**Admin**
```
Cellar Admin login credentials for assessment review
User: admin@email.com
Password: AuthPass123!
```
Admin have access to create, update, and delete data, with these permissions:
  * get:vintners-edit
  * get:vintners-create
  * post:vintners-edit
  * post:vintners-create
  * get:wines-edit
  * post:wines-edit
  * post:wines-create
  * get:wines-create
  * get:auth
  * delete:wines
  * delete:vintners

### Public Endpoints

#### GET ```/``` Index
  * Fetches landing page, with 10 most recent vintners & wines added.
  * Request Arguments: None
  * Auth: Public
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/```

#### GET ```/vintners```
  * Fetches all vintners, grouped by associated area.
  * Request Arguments: None
  * Auth: Public
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/vintners```

#### POST ```/vintners/search```
  * Fetches all vintners who's name, country, region, or appellation match search term.
  * Request Arguments: ```search_term```
  * Auth: Public
  * Returns: Dynamically populated html rendering
  * Sample: ```curl -d "search_term=angel" -X POST http://127.0.0.1:8080/vintners/search```

#### GET ```/vintners/<int:vintner_id>```
  * Fetches specific vintner, with all detailed data and their associated wines.
  * Request Arguments: vintner id
  * Auth: Public
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/vintners/2```

#### GET ```/wines```
  * Fetches all wines, grouped by associated type.
  * Request Arguments: None
  * Auth: Public
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/wines```

#### POST ```/wines/search```
  * Fetches all vintners who's name, country, region, or appellation match search term.
  * Request Arguments: ```search_term```
  * Auth: Public
  * Returns: Dynamically populated html rendering
  * Sample: ```curl -d "search_term=red" -X POST http://127.0.0.1:8080/wines/search```

#### GET ```/wines/<int:vino_id>```
  * Fetches specific wine, with all detailed data and its vintner.
  * Request Arguments: vino id
  * Auth: Public
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/wines/2```

#### GET ```/login```
  * Fetches log in page redirect, provided by Auth0.
  * Request Arguments: None
  * Auth: Public
  * Returns: link to Auth0 hosted login page
  * Sample: ```curl http://127.0.0.1:8080/login```

#### GET ```/callback```
  * Handles the response from the Auth0 authorization, parsing token and populating session data.
  * Request Arguments: None
  * Auth: Public
  * Returns: populated session data, index page re-route
  * Sample: ```curl http://127.0.0.1:8080/callback```


### Authenticated Access Only Endpoints 🛂

#### GET ```/dashboard```
  * Fetches dashboard page listing user info & logout button.
  * Request Arguments: None
  * Auth: Manager & Admin Roles
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/dashboard```

#### GET ```/logout```
  * Handles the logout from the Auth0 authorization, ending user session.
  * Request Arguments: None
  * Auth: Manager & Admin Roles
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/logout```

#### GET ```/vintners/create```
  * Fetches create vintners from.
  * Request Arguments: None
  * Auth: Manager & Admin Roles
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/vintners/create```

#### POST ```/vintners/create```
  * Persists new create vintner entry to the database.
  * Request Arguments: form data
  * Auth: Manager & Admin Roles
  * Returns: Dynamically populated html rendering
  * Sample: ```curl -d "name=Angeline&creation_date=2021-02-28 21:15:54&country=United States&region=California" -X POST http://127.0.0.1:8080/vintners/create```

#### GET ```/vintners/<int:vintner_id>/edit```
  * Fetches edit vintners from, pre-populated with existing data.
  * Request Arguments: vintner id
  * Auth: Manager & Admin Roles
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/vintners/2/edit```

#### POST ```/vintners/<int:vintner_id>/edit```
  * Persists edit vintner entry to the database.
  * Request Arguments: form data
  * Auth: Manager & Admin Roles
  * Returns: Dynamically populated html rendering
  * Sample: ```curl -d "name=Angeline&country=United States&region=California" -X POST http://127.0.0.1:8080/vintners/2/edit```

#### DELETE ```/vintners/<vintner_id>```
  * Persists delete vintner entry to the database.
  * Request Arguments: None
  * Auth: ONLY Admin Role
  * Returns: Redirect to index page
  * Sample: ```curl -X DELETE http://127.0.0.1:8080/vintners/2```


#### GET ```/vintners/<int:vintner_id>/vino/create```
  * Fetches create wine from, accessed from the associated vintner detail page.
  * Request Arguments: parent vintner id
  * Auth: Manager & Admin Roles
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/vintners/1/vino/create```

#### POST ```/vintners/<int:vintner_id>/vino/create```
  * Persists new create wine entry to the database.
  * Request Arguments: form data
  * Auth: Manager & Admin Roles
  * Returns: Dynamically populated html rendering
  * Sample: ```curl -d "name=Chardonnay&year=2010&abv=11.11&style=Bold&varietal={Zinfandel}&type=1&creation_date=2021-02-28 21:15:54" -X POST http://127.0.0.1:8080/vintners/1/vino/create```

#### GET ```/wines/<int:vino_id>/edit```
  * Fetches edit wine from, pre-populated with existing data.
  * Request Arguments: wine id
  * Auth: Manager & Admin Roles
  * Returns: Dynamically populated html rendering
  * Sample: ```curl http://127.0.0.1:8080/wines/2/edit```

#### POST ```/wines/<int:vino_id>/edit```
  * Persists edit vintner entry to the database.
  * Request Arguments: form data
  * Auth: Manager & Admin Roles
  * Returns: Dynamically populated html rendering
  * Sample: ```curl -d "name=Chardonnay&year=2010&abv=11.11&style=Bold&varietal={Zinfandel}&type=1" -X POST http://127.0.0.1:8080/wines/2/edit```

#### DELETE ```/wines/<vino_id>```
  * Persists delete wine entry to the database.
  * Request Arguments: None
  * Auth: ONLY Admin Role
  * Returns: Redirect to index page
  * Sample: ```curl -X DELETE http://127.0.0.1:8080/wines/2```

### Error handling
The error codes currently handled:
  * AuthError: Auth0 error
  * 400: Bad request
  * 401: Unauthorized
  * 404: Resource not found
  * 409: Duplicate resource
  * 422: Not processable
  * 500: Server error


## Authors
Malcolm T Suhr - capstone student project for Udacity Full Stack Web Developer Nanodegree

## Acknowledgements
Thank you to the Udacity community!
