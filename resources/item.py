from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Este espacio no puede estar en blanco')

    parser.add_argument('store_id', type=int, required=True, help='Todos los items necesitan un id_store')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'item no encontrado'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "El item de nombre '{}' ya existe".format(
                name)}, 400  # 400 es el codigo para bad request

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'Ocurrió un error al insertar el item'}, 500  # 500 internal server error

        return item.json(), 201

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'item eliminado: {}'.format(name)}
        return {'message': 'item no encontrado: {}'.format(name)}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
