export DATABASE_URL='postgresql://malcolmsuhr@localhost:5432/vino'
export AUTH0_CLIENT_ID='n1rJVCtvkXZUjYiFypLGp206po8MFmsS'
export AUTH0_DOMAIN='mtsuhr2021.us.auth0.com'
export AUTH0_BASE_URL='https://mtsuhr2021.us.auth0.com'
export AUTH0_AUDIENCE='http://0.0.0.1:8080'
export AUTH0_CALLBACK_URL='http://0.0.0.0:8080/callback'
export ENV='development'
export FLASK_APP=app.py
export FLASK_DEBUG=True
export ALGORITHMS=['RS256']
export AUTH0_CLIENT_SECRET='1haTrpczKaX_nvrs7jgQyAxDBdYAbxwPpyKevNxrjEfoOyaz7Z7sER2i0EzYV2c0'

pip3 install -r requirements.txt
