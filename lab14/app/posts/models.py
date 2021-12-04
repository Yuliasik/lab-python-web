import enum
from .. import db


post_tags_connector = db.Table(
    'post_tags_connector',
    db.Column('tags', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)


class PostType(enum.Enum):
    News = 'News'
    Publication = 'Publication'
    Other = 'Other'


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    posts = db.relationship("Post", back_populates="category")


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(20), nullable=False, default='default.png')
    created = db.Column(db.DateTime, default=db.func.now())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=False)
    category = db.relationship("Category", back_populates="posts")
    tags = db.relationship("Tag", secondary=post_tags_connector)
    is_enabled = db.Column(db.Boolean, default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


db.create_all()
