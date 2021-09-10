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


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return{'message': 'Usuario no encontrado'}, 404
        return user.json()

    @classmethod
    def delete(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return{'Message': 'Usuario no encontrado'}, 404
        user.delete_from_db()
        return {'message': 'usuario con id: {} eliminado'.format(user_id)}
