from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'

    #prevents recursively trying things together over and over again
    #comma sets up a tuple
    serialize_rules = ('-baked_goods.bakery',)

    # building our table columns here
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default= db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    #build relationship for the baked good in a bakery, and referencing
    #baked good table and finding the baked goods that match the bakery id
    #does not make a physical column but can be referenced 
    baked_goods = db.relationship("BakedGood", backref = "bakery")
    #relationship goes in the 1 

    def __repr__(self):
        return 'name: {self.name}'

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'

    #also stops recursion between the two so its the reverse of
    #other serialization rule
    serialize_rules = ('-bakery.backed_goods',)

    #Table Columns for Baked Goods
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    #pulling from Bakery Class table "bakeries.id" basically
    #saying that the baked goods are linked to a single bakery
    #many to one relationship
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))
    #foreign key belongs in the many
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at= db.Column(db.DateTime, onupdate=db.func.now())
    
    def __repr__(self):
        return f'name: {self.name}, price: {self.price}'