from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Tienda no encontrada'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Ya existe una tienda con ese nombre: {}'}.format(name), 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Ha ocurrido un error al crear la tienda'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete()
        return {'message': 'Tienda eliminada'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]} # list(map(lambda x: x.json(), StoreModel.query.all())
