import os
import sys
import requests
from flask import (
    Flask, render_template, request, abort, session,
    Response, flash, jsonify, redirect, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_wtf import Form, FlaskForm
from forms import *
from models import *
from config import SECRET_KEY
from auth.auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth
from sqlalchemy import func
import simplejson as json
from six.moves.urllib.parse import urlencode

AUTH0_CALLBACK_URL = os.getenv('AUTH0_CALLBACK_URL')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_BASE_URL = os.getenv('AUTH0_BASE_URL')
AUTH0_AUDIENCE = os.getenv('AUTH0_AUDIENCE')

# ----------------------------------------------------------------------------#
# Initialize App
# ----------------------------------------------------------------------------#


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )

    '''
    Use the after_request decorator to set Access-Control-Allow.
    '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,PATCH,DELETE,OPTIONS')
        return response

    # ------------------------------------------------------------------------#
    # Functions.
    # ------------------------------------------------------------------------#
    # Query|Create Area: takes form country|region|appellation data,
    # Object of vinter

    def query_create_area(form, newObject):
        if form.region.data:
            if Area.query.filter_by(
                    country=form.country.data,
                    region=form.region.data.lower(),
                    appellation=form.appellation.data.lower()).count() > 0:
                # if country + region + appellation match form input then:
                this_area = Area.query.filter_by(
                    country=form.country.data,
                    region=form.region.data.lower(),
                    appellation=form.appellation.data.lower()).first()
                newObject.area_id = this_area.id
                objects = [newObject]
            elif db.session.query(db.func.max(Area.id)).scalar():
                # else populate new Area with area combo & generate uuid
                area_uuid = db.session.query(db.func.max(Area.id)).scalar() + 1
                newArea = Area(
                    id=area_uuid,
                    country=form.country.data,
                    region=form.region.data.lower(),
                    appellation=form.appellation.data.lower())
                newObject.area_id = newArea.id
                objects = [newObject, newArea]
            else:
                # else populate first Area with area combo & generate id 1
                area_uuid = 1
                newArea = Area(
                    id=area_uuid,
                    country=form.country.data,
                    region=form.region.data.lower(),
                    appellation=form.appellation.data.lower())
                newObject.area_id = newArea.id
                objects = [newObject, newArea]
        return objects

    # ------------------------------------------------------------------------#
    # Controllers.
    # ------------------------------------------------------------------------#

    #  ----------------------------------------------------------------
    #  INDEX Home Page
    #      populate home page with 10 recent vintner|vino listings
    #  ----------------------------------------------------------------

    @app.route('/')
    @cross_origin()
    def index():
        recent_vintners = Vintner.query.order_by(
                        db.desc(Vintner.creation_date)).limit(10).all()
        recent_wines = Vino.query.order_by(
                        db.desc(Vino.creation_date)).limit(10).all()
        return render_template(
            'pages/home.html', vintners=recent_vintners, wines=recent_wines)

    #  ----------------------------------------------------------------
    #  Auth0 Routes
    #  ----------------------------------------------------------------

    #  LOGIN Authorization
    #  ----------------------------------------------------------------

    @app.route('/login')
    @cross_origin()
    def login():
        # print('Audience: {}'.format(AUTH0_AUDIENCE))
        return auth0.authorize_redirect(
            redirect_uri=AUTH0_CALLBACK_URL,
            audience=AUTH0_AUDIENCE
            )

    #  CALLBACK Authorization
    #  ----------------------------------------------------------------

    @app.route('/callback', methods=['GET'])
    @cross_origin()
    def callback_handling():
        token = auth0.authorize_access_token()
        session['token'] = token['access_token']
        print("callback_A: " + session['token'])

        resp = auth0.get('userinfo')
        userinfo = resp.json()

        session['jwt_payload'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'picture': userinfo['picture']
        }
        print("callback_B: " + userinfo['name'])
        return redirect(url_for('index'))

    #  DASHBOARD Authorization
    #  ----------------------------------------------------------------

    @app.route('/dashboard', methods=['GET'])
    @cross_origin()
    def dashboard():
        return render_template('pages/dashboard.html',
                               userinfo=session['profile'],
                               userinfo_pretty=json.dumps(
                                session['jwt_payload'], indent=4))

    #  LOGOUT Authorization
    #  ----------------------------------------------------------------

    @app.route('/logout')
    def logout():
        # Clear session stored data
        session.clear()
        # Redirect user to logout endpoint
        params = {'returnTo': url_for(
            'index', _external=True), 'client_id': AUTH0_CLIENT_ID}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    #  ----------------------------------------------------------------
    #  VINTNERS Controllers Section
    #  ----------------------------------------------------------------

    #  LIST Vintners
    #  ----------------------------------------------------------------

    @app.route('/vintners')
    def vintners():
        try:
            areas = Area.query.join(
                Area.vintners).order_by('country', 'region', 'appellation')
            error = False

            def comp_data(area):
                vintners = Vintner.query.filter_by(area_id=area.id).all()

                def comp_vintners(vintner):
                    their_vino = Vino.query.join(Vintner).filter(
                        Vino.vintner_id == vintner.id).all()
                    return {
                        "id": vintner.id,
                        "name": vintner.name,
                        "num_wines": len(their_vino)
                        }
                return {
                    "country": area.country,
                    "region": area.region,
                    "appellation": area.appellation,
                    "vintners": [comp_vintners(
                        vintner=vintner) for vintner in vintners]
                    }
            area_data = [comp_data(area=area) for area in areas]
        except Exception:
            error = True
        return render_template('pages/vintners.html', areas=area_data)

    #  SEARCH Vintners
    #  ----------------------------------------------------------------

    @app.route('/vintners/search', methods=['POST', 'GET'])
    def search_vintners():
        search_term = request.form.get('search_term', '')
        vintners = Vintner.query.all()
        search_vintners = [vintner for vintner in vintners
                           if search_term.lower() in vintner.name.lower()
                           or search_term.lower() in
                           Area.query.get(vintner.area_id).country
                           + ", " +
                           Area.query.get(vintner.area_id).region.lower()
                           + ", " +
                           Area.query.get(vintner.area_id).appellation.lower()]

        def comp_vintners(vintner):
            their_vino = Vino.query.join(Vintner).filter(
                Vino.vintner_id == vintner.id).all()
            return {
                "id": vintner.id,
                "name": vintner.name,
                "num_wines": len(their_vino)
                }
    # Search on vintners with partial string search; Case-insensitive.
        response = {
          "count": len(search_vintners),
          "data": [comp_vintners(
            vintner=vintner) for vintner in search_vintners]
        }
        return render_template(
            'pages/search_vintners.html',
            results=response, search_term=search_term)

    #  SHOW Vintner Details
    #  ----------------------------------------------------------------

    @app.route('/vintners/<int:vintner_id>')
    def show_vintner(vintner_id):
        this_vintner = Vintner.query.get(vintner_id)
        ref_area = Area.query.get(this_vintner.area_id)
        their_vino = Vino.query.join(Vintner).filter(
            Vino.vintner_id == vintner_id).all()

        def comp_wines(vino):
            this_vino = Vino.query.get(vino.id)
            return {
                "vino_id": this_vino.id,
                "vino_name": this_vino.name,
                "vino_image_link": this_vino.image_link
                }

        data = {
          "id": this_vintner.id,
          "name": this_vintner.name,
          "country": ref_area.country,
          "region": ref_area.region,
          "appellation": ref_area.appellation,
          "website": this_vintner.website,
          "image_link": this_vintner.image_link,
          "wines": [comp_wines(vino=vino) for vino in their_vino],
          "wines_count": len(their_vino)
        }
        return render_template('pages/show_vintner.html', vintner=data)

    #  CREATE Vintner GET|POST
    #  ----------------------------------------------------------------

    @app.route('/vintners/create', methods=['GET'])
    @requires_auth('get:vintners-create')
    def create_vintner_form(payload):
        form = VintnerForm()
        return render_template('forms/new_vintner.html', form=form)

    @app.route('/vintners/create', methods=['POST'])
    @requires_auth('post:vintners-create')
    def create_vintner_submission(payload):
        form = VintnerForm(request.form, meta={"csrf": False})
        error = False
        try:
            newVintner = Vintner(
                name=form.name.data,
                website=form.website.data,
                image_link=form.image_link.data,
                creation_date=form.creation_date.data,
                area_id='')
# function querys existing areas compared to form input; else generate new area
            objects = query_create_area(form, newVintner)

            db.session.add_all(objects)
            db.session.commit()
            flash('Vintner ' + request.form['name'] +
                  ' was successfully listed!')
        except Exception:
            db.session.rollback()
            error = True
            flash('An error occurred. Vintner ' + request.form['name'] +
                  ' could not be listed.')
            # print(sys.exc_info())
        finally:
            db.session.close()
        return render_template('pages/home.html')

    #  EDIT Vintner GET|POST
    #  ----------------------------------------------------------------

    @app.route('/vintners/<int:vintner_id>/edit', methods=['GET'])
    @requires_auth('get:vintners-edit')
    def edit_vintner(payload, vintner_id):
        form = VintnerForm()
        this_vintner = Vintner.query.get(vintner_id)
        ref_area = Area.query.get(this_vintner.area_id)
        vintner = {
            "id": this_vintner.id,
            "name": this_vintner.name,
            "country": ref_area.country,
            "region": ref_area.region,
            "appellation": ref_area.appellation,
            "website": this_vintner.website,
            "image_link": this_vintner.image_link
            }
        form.country.data = ref_area.country
        return render_template(
            'forms/edit_vintner.html',
            form=form, vintner=vintner)

    @app.route('/vintners/<int:vintner_id>/edit', methods=['POST'])
    @requires_auth('post:vintners-edit')
    def edit_vintner_submission(payload, vintner_id):
        form = VintnerForm(request.form, meta={"csrf": False})
        editVintner = Vintner.query.get(vintner_id)
        error = False
        try:
            editVintner.name = form.name.data
            editVintner.website = form.website.data
            editVintner.image_link = form.image_link.data
# function querys existing areas compared to form input; else generate new area
            objects = query_create_area(form, editVintner)

            db.session.add_all(objects)
            db.session.commit()
            flash('Vintner ' + request.form['name'] +
                  ' was successfully edited!')
        except Exception:
            db.session.rollback()
            error = True
            flash('An error occurred. Vintner ' + request.form['name'] +
                  ' could not be edited.')
            # print(sys.exc_info())
        finally:
            db.session.close()
        return redirect(url_for('show_vintner', vintner_id=vintner_id))

    #  DELETE Vintner
    #  ----------------------------------------------------------------

    @app.route('/vintners/<vintner_id>', methods=['DELETE'])
    @requires_auth('delete:vintners')
    def delete_vintner(payload, vintner_id):
        error = False
        try:
            this_vintner = Vintner.query.get(vintner_id)
            db.session.delete(this_vintner)
            db.session.commit()
        except Exception:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
        return redirect(url_for('index'))

    #  ----------------------------------------------------------------
    #  VINO Controllers Section
    #  ----------------------------------------------------------------

    #  LIST Vino
    #  ----------------------------------------------------------------

    @app.route('/wines')
    def wines():
        types = Type.query.join(Type.wines).order_by('type').all()

        def comp_data(type):
            wines = Vino.query.filter_by(
                type_id=type.id).order_by('year').all()

            def comp_wines(vino):
                return {
                    "id": vino.id,
                    "name": vino.name,
                    "year": vino.year
                    }
            return {
                "type": type.type,
                "wines": [comp_wines(
                    vino=vino) for vino in wines]
                }
        type_data = [comp_data(type=type) for type in types]
        return render_template('pages/wines.html', types=type_data)

    #  SEARCH Vino
    #  ----------------------------------------------------------------

    @app.route('/wines/search', methods=['POST'])
    def search_wines():
        search_term = request.form.get('search_term', '')
        wines = Vino.query.all()
        search_wines = [vino for vino in wines
                        if search_term.lower() in vino.name.lower()
                        or [varietal.lower() for varietal in vino.varietal
                            if search_term.lower() in varietal.lower()]
                        or search_term.lower() in
                        Type.query.get(vino.type_id).type.lower()]

        def comp_wines(vino):
            the_type = Type.query.get(vino.type_id)
            return {
                "id": vino.id,
                "name": vino.name,
                "year": vino.year,
                "type": the_type.type
                }
        response = {
          "count": len(search_wines),
          "data": [comp_wines(vino=vino) for vino in search_wines]
        }
        return render_template(
            'pages/search_wines.html',
            results=response, search_term=search_term)

    #  SHOW Vino Details
    #  ----------------------------------------------------------------

    @app.route('/wines/<int:vino_id>', methods=['GET'])
    def show_vino(vino_id):
        this_vino = Vino.query.get(vino_id)
        the_vintner = Vintner.query.get(this_vino.vintner_id)
        the_type = Type.query.get(this_vino.type_id)

        data = {
          "id": this_vino.id,
          "name": this_vino.name,
          "year": this_vino.year,
          "type": the_type.type,
          "varietal": this_vino.varietal,
          "style": this_vino.style,
          "abv": this_vino.abv,
          "image_link": this_vino.image_link,
          "vintner_id": this_vino.vintner_id,
          "vintner_name": the_vintner.name
        }
        return render_template('pages/show_vino.html', vino=data)

    #  EDIT Vino GET|POST
    #  ----------------------------------------------------------------

    @app.route('/wines/<int:vino_id>/edit', methods=['GET'])
    @requires_auth('get:wines-edit')
    def edit_vino(payload, vino_id):
        form = VinoForm()
        this_vino = Vino.query.get(vino_id)
        the_vintner = Vintner.query.get(this_vino.vintner_id)
        vino = {
            "id": this_vino.id,
            "name": this_vino.name,
            "year": this_vino.year,
            "type_id": this_vino.type_id,
            "varietal": this_vino.varietal,
            "style": this_vino.style,
            "abv": this_vino.abv,
            "image_link": this_vino.image_link,
            "vintner_id": this_vino.vintner_id,
            "vintner_name": the_vintner.name
            }
        form.varietal.data = this_vino.varietal
        types = Type.query.order_by('id').all()
        return render_template(
            'forms/edit_vino.html',
            form=form, vino=vino, types=types)

    @app.route('/wines/<int:vino_id>/edit', methods=['POST'])
    @requires_auth('post:wines-edit')
    def edit_vino_submission(payload, vino_id):
        form = VinoForm(request.form, meta={"csrf": False})
        editVino = Vino.query.get(vino_id)
        error = False
        try:
            editVino.id = vino_id
            editVino.name = form.name.data
            editVino.year = form.year.data
            editVino.type_id = form.type.data
            editVino.varietal = form.varietal.data
            editVino.style = form.style.data
            editVino.abv = form.abv.data
            editVino.image_link = form.image_link.data

            objects = [editVino]

            db.session.add_all(objects)
            db.session.commit()
            flash('Vino ' + request.form['name'] + ' was successfully edited!')
        except Exception:
            db.session.rollback()
            error = True
            flash('An error occurred. Vino ' + request.form['name'] +
                  ' could not be edited.')
            # print(sys.exc_info())
        finally:
            db.session.close()
        return redirect(url_for('show_vino', vino_id=vino_id))

    #  Create Vino GET|POST
    #  ----------------------------------------------------------------

    @app.route('/vintners/<int:vintner_id>/vino/create', methods=['GET'])
    @requires_auth('get:wines-create')
    def create_vino_form(payload, vintner_id):
        form = VinoForm()
        vintner_id = vintner_id
        types = Type.query.order_by('id').all()
        return render_template(
            'forms/new_vino.html',
            vintner_id=vintner_id, form=form, types=types)

    @app.route('/vintners/<int:vintner_id>/vino/create', methods=['POST'])
    @requires_auth('post:wines-create')
    def create_vino_submission(payload, vintner_id):
        form = VinoForm(request.form, meta={"csrf": False})
        error = False
        try:
            newVino = Vino(
                name=form.name.data,
                year=form.year.data,
                type_id=form.type.data,
                varietal=form.varietal.data,
                style=form.style.data,
                abv=form.abv.data,
                image_link=form.image_link.data,
                vintner_id=vintner_id,
                creation_date=form.creation_date.data)

            objects = [newVino]

            db.session.add_all(objects)
            db.session.commit()
            flash('Vino ' + request.form['name'] + ' was successfully listed!')
        except Exception:
            db.session.rollback()
            error = True
            flash('An error occurred. Vino ' + request.form['name'] +
                  ' could not be listed.')
            # print(sys.exc_info())
        finally:
            db.session.close()
        return render_template('pages/home.html')

    #  DELETE Vino
    #  ----------------------------------------------------------------

    @app.route('/wines/<vino_id>', methods=['DELETE'])
    @requires_auth('delete:wines')
    def delete_vino(payload, vino_id):
        error = False
        try:
            this_vino = Vino.query.get(vino_id)
            db.session.delete(this_vino)
            db.session.commit()
        except Exception:
            db.session.rollback()
            error = True
        finally:
            db.session.close()
        return redirect(url_for('index'))

    #  ----------------------------------------------------------------
    #  ERROR Route Handler Controllers Section.
    #  ----------------------------------------------------------------

    @app.errorhandler(AuthError)
    def authentification_error(AuthError):
        return render_template('errors/autherror.html'), AuthError.status_code

    @app.errorhandler(400)
    def bad_request_error(error):
        return render_template('errors/400.html'), 400

    @app.errorhandler(401)
    def bad_request_error(error):
        return render_template('errors/401.html'), 401

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(409)
    def duplicate_resource_error(error):
        return render_template('errors/409.html'), 409

    @app.errorhandler(422)
    def not_processable_error(error):
        return render_template('errors/422.html'), 422

    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500

    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(
            Formatter('%(asctime)s %(levelname)s:' +
                      ' %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
