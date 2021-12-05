from flask_login import login_required
from flask import url_for, render_template, redirect,\
    flash
from . import goods
from .form import GoodsForm, CategoryGoodsForm
from .models import Goods, CategoryGoods
from .. import db, App


@goods.route('/')
def index():
    return render_template('index1.html',
                           all_goods=Goods.query.all(),
                           menu=App.getMenu())


@goods.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = GoodsForm()
    form.category.choices = [(category.id, category.name)
                             for category in CategoryGoods.query.all()]
    if form.validate_on_submit():
        category = CategoryGoods.query.get(form.category.data)

        new_goods = Goods(code=form.code.data,
                          name=form.name.data,
                          category=category,
                          is_available=form.is_available.data,
                          count=form.count.data,
                          price=form.price.data,
                          description=form.description.data)
        db.session.add(new_goods)
        db.session.commit()
        flash('Goods added!', category='success')
        return redirect(url_for('goods.index'))

    return render_template('create_goods.html', form=form, menu=App.getMenu())


@goods.route('/<id>', methods=['GET', 'POST'])
def view(id):
    view_goods = Goods.query.get(id)
    return render_template('goods.html',
                           view_goods=view_goods,
                           menu=App.getMenu())


@goods.route('/<id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    update_goods = Goods.query.get_or_404(id)
    form = GoodsForm()
    form.category.choices = [(category.id, category.name)
                             for category in CategoryGoods.query.all()]
    if form.validate_on_submit():
        category = CategoryGoods.query.get(form.category.data)

        update_goods.code = form.code.data
        update_goods.name = form.name.data
        update_goods.category = category
        update_goods.count = form.count.data
        update_goods.is_available = form.count.data != 0
        update_goods.price = form.price.data
        update_goods.description = form.description.data

        db.session.commit()
        flash('Goods updated!', category='success')
        return redirect(url_for('goods.index'))

    form.category.data = update_goods.category_id
    form.category.default = update_goods.category_id
    form.process()
    form.code.data = update_goods.code
    form.name.data = update_goods.name
    form.count.data = update_goods.count
    form.is_available.data = update_goods.is_available
    form.price.data = update_goods.price
    form.description.data = update_goods.description

    return render_template('update_goods.html', form=form, menu=App.getMenu())


@goods.route('/<id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    goods_delete = Goods.query.get_or_404(id)
    db.session.delete(goods_delete)
    db.session.commit()
    flash('The goods ' + goods_delete.name + ' is deleted')
    return redirect(url_for('goods.index'))


@goods.route('/categories', methods=['GET', 'POST'])
def categories():
    form = CategoryGoodsForm()
    if form.name.data:
        category = CategoryGoods(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        form.name.data = ''
        flash('Category ' + category.name + ' added!', category='success')
    categories = CategoryGoods.query.all()
    return render_template('categories.html', categories=categories,
                           form=form, menu=App.getMenu())
