export AUTH0_DOMAIN="MY_DOMAIN"
export API_AUDIENCE="ball"
export ALGORITHMS=["RS256"]
export DATABASE_URL="postgres://localhost:5432/ball"
export TEST_AUTH=""

pip3 install -r requirements.txt
service postgresql start
su - postgres bash -c "psql < /home/workspace/backend/setup.sql"
su - postgres bash -c "psql bookshelf < /home/workspace/backend/books.psql"
