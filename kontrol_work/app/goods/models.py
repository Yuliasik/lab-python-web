from .. import db


class CategoryGoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    goods = db.relationship("Goods", back_populates="category")


class Goods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(12), unique=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_goods.id'),
                            nullable=False)
    category = db.relationship("CategoryGoods", back_populates="goods")
    is_available = db.Column(db.Boolean, default=True, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)


db.create_all()
