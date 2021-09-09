from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from db import db
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'thekey'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

#app.config['JWT_AUTH_URL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity)

# configuración de JWT para expirar en 30 min
#app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# configuración de JWT para que la clave de autorización sea 'email' en lugar de la default 'username'
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

# personalizar JWT auth response, inclur el id usuario en el cuerpo de la respuesta
#@jwt.auth_response_handler
#def customized_response_handler(access_token, identity):
#    return jsonify({
#                        'access_token': access_token.decode('utf-8'),
#                        'user_id': identity.id
#                   })

#def customized_error_handler(error):
#    return jsonify({
#                       'message': error.description,
#                       'code': error.status_code
#                   }), error.status_code

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
