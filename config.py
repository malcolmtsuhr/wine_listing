import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True

auth0_config = {
    "AUTH0_DOMAIN" : "mtsuhr2021.us.auth0.com",
    "ALGORITHMS" : ["RS256"],
    "API_AUDIENCE" : "http://0.0.0.1:8080"
}
