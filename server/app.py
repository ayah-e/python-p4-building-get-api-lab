#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

#GET /bakeries
#query select
#set up dictionary for each bakery in bakeries
#jsonify it to return the array
@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_dict = [ bakery.to_dict() for bakery in bakeries]

    response = make_response(
        jsonify(bakeries_dict),
        200
    )

    return response

#select bakery from Bakery class and jsonify it into array
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict= bakery.to_dict()

    response = make_response(
        jsonify(bakery_dict),
        200
    )

    return response 
                
#select baked goods then order in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    
    ordered_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    ordered_goods_dict = [ordered_good.to_dict() for ordered_good in ordered_goods]

    response = make_response(
        jsonify(ordered_goods_dict),
        200
    )

    return response
        

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    expensive_good_dict = expensive_good.to_dict()

    response = make_response(
        jsonify(expensive_good_dict),
        200
    )

    return response


if __name__ == '__main__':
    app.run(port=555, debug=True)
