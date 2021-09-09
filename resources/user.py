from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='este espacio no puede ir en blanco')
    parser.add_argument('password', type=str, required=True, help='este espacio no puede ir en blanco')

    def post(self):
        data = self.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'Este nombre de usuario ya existe'}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {'message': 'usuario creado'}, 201  # 201 es paa creado
