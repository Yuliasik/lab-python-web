from flask import request, jsonify, current_app, make_response
from flask_restful import Resource, Api, fields, marshal_with
from functools import wraps

from ..posts.models import Post
from ..auth.models import User
from . import categories
from .. import db

import jwt

resourse_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'image': fields.String,
    'created': fields.DateTime,
    'is_enabled': fields.Boolean,
    'user_id': fields.Integer,
    'category_id': fields.Integer
}


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithm="HS256")
            current_user = User.query.filter_by(username=data['username']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)
    return decorator


@categories.route('/register', methods=['GET', 'POST'])
def signup_user():
    data = request.get_json()

    new_user = User(username=data['username'],
                    password=data['password'],
                    email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registered successfully'})


@categories.route('/login', methods=['GET', 'POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify 1', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(username=auth.username).first()

    if user.verify_password(auth.password):
        token = jwt.encode({'username': user.username}, current_app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({'token': token})

    return make_response('could not verify 2', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


class PostApi(Resource):
    @token_required
    @marshal_with(resourse_fields)
    def get(self, id):
        return Post.query.get_or_404(id)

    @marshal_with(resourse_fields)
    def post(self, id):
        data = request.get_json()['post']
        post_new = Post(
            title=data['title'],
            description=data['description'],
            image=data['image'],
            created=db.func.now(),
            is_enabled=data['is_enabled'],
            user_id=data['user_id'],
            category_id=data['category_id']
        )

        db.session.add(post_new)
        db.session.commit()
        return post_new

    @marshal_with(resourse_fields)
    def put(self, id):
        data = request.get_json()['post']
        post_old = Post.query.get_or_404(id)
        post_new = Post(
            title=data['title'],
            description=data['description'],
            image=data['image'],
            user_id=data['user_id'],
            category_id=data['category_id']
        )
        post_old.title = post_new.title
        post_old.description = post_new.description
        post_old.image = post_new.image
        post_old.user_id = post_new.user_id
        post_old.category_id = post_new.category_id

        db.session.commit()
        return post_old

    def delete(self, id):
        post_old = Post.query.get_or_404(id)
        db.session.delete(post_old)
        db.session.commit()
        return jsonify({'message': 'The post has been deleted!'})


class PostsApi(Resource):
    @marshal_with(resourse_fields)
    def get(self):
        return Post.query.all()


api = Api(current_app)
api.add_resource(PostApi, "/api/v2/<int:id>")
api.add_resource(PostsApi, "/api/v2/all")
