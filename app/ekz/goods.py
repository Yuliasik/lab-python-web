from flask import request, jsonify, current_app
from flask_restful import Resource, Api, fields, marshal_with

from ..goods.models import Goods
from .. import db

resourse_fields = {
    'id': fields.Integer,
    'code': fields.String,
    'name': fields.String,
    'category_id': fields.Integer,
    'is_available': fields.Boolean,
    'count': fields.Integer,
    'price': fields.Integer,
    'description': fields.String
}


class GoodApi(Resource):
    @marshal_with(resourse_fields)
    def get(self, id):
        return Goods.query.get_or_404(id)

    @marshal_with(resourse_fields)
    def put(self, id):
        data = request.get_json()['good']
        good_old = Goods.query.get_or_404(id)
        good_new = Goods(
            code=data['code'],
            name=data['name'],
            category_id=data['category_id'],
            is_available=data['is_available'],
            count=data['count'],
            price=data['price'],
            description=data['description']
        )
        good_old.code = good_new.code
        good_old.name = good_new.name
        good_old.category_id = good_new.category_id
        good_old.is_available = good_new.is_available
        good_old.count = good_new.count
        good_old.price = good_new.price
        good_old.description = good_new.description

        db.session.commit()
        return good_old

    def delete(self, id):
        good_old = Goods.query.get_or_404(id)
        db.session.delete(good_old)
        db.session.commit()
        return jsonify(
            {'message': f'The good has {good_old.name} been deleted!'})


class GoodsApi(Resource):
    @marshal_with(resourse_fields)
    def get(self):
        return Goods.query.all()

    @marshal_with(resourse_fields)
    def post(self):
        data = request.get_json()['good']
        good_new = Goods(
            code=data['code'],
            name=data['name'],
            category_id=data['category_id'],
            is_available=data['is_available'],
            count=data['count'],
            price=data['price'],
            description=data['description']
        )

        db.session.add(good_new)
        db.session.commit()
        return good_new


api = Api(current_app)
api.add_resource(GoodApi, "/api/dudii/goods/<int:id>")
api.add_resource(GoodsApi, "/api/dudii/goods")
