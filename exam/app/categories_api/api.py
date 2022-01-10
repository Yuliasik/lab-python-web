from flask import request, jsonify, current_app
from functools import wraps

from . import categories
from .. import db
from ..posts.models import Category


def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == current_app.api_login \
           and auth.password == current_app.api_password:
            return f(*args, **kwargs)
        return jsonify({'message': 'Authentication failed!'}), 403
    return decorated


@categories.route('', methods=['GET'])
@protected
def find_all():
    categories = Category.query.all()

    values = [cat.to_dict() for cat in categories]

    return jsonify({'categories': values})


@categories.route('/<int:id>', methods=['GET'])
@protected
def find(id):
    category = Category.query.get_or_404(id)
    return jsonify({'category': category.to_dict()})


@categories.route('', methods=['POST'])
@protected
def create():
    new_name = request.get_json()['category']['name']

    for cat in Category.query.all():
        if cat.name == new_name:
            _ = f'The category {new_name} exists!'
            return jsonify({'message': _})

    new_category = Category(name=new_name)
    db.session.add(new_category)
    db.session.commit()

    return find(new_category.id)


@categories.route('/<int:id>', methods=['PUT', 'PATCH'])
@protected
def edit(id):
    new_name = request.get_json()['category']['name']

    for cat in Category.query.all():
        if cat.name == new_name:
            _ = f'The category {new_name} exists!'
            return jsonify({'message': _})

    category = Category.query.get_or_404(id)
    category.name = new_name
    db.session.commit()

    return find(category.id)


@categories.route('/<int:id>', methods=['DELETE'])
@protected
def delete(id):
    db.session.delete(Category.query.get(id))
    db.session.commit()
    return jsonify({'message': 'The category deleted!'})
