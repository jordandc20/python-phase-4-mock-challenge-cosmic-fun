from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'
    serialize_rules = ('-planet.missions', '-scientist.missions')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    
    @validates('name')
    def validate_scientist_name(self,key,value):
        if not value:
            raise ValueError('mission name must be provided')
        return value

    @validates('scientist_id')
    def validate_scientist_id(self,key,value):
        scientists = [scientist.id for scientist in Scientist.query.all()]
        if not value:
            raise ValueError('scientist_id must be provided')
        elif value not in scientists:
            raise ValueError('scientist_id must exist')
        return value
    
    @validates('planet_id')
    def validate_scientist_planet_id(self,key,value):
        planets = [planet.id for planet in Planet.query.all()]
        if not value:
            raise ValueError(' planet_id must be provided')
        elif value not in planets:
            raise ValueError('planet_id must exist')
        return value
    
    
class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    serialize_rules = ('-updated_at','-created_at','-missions', '-planets.scientist', '-planets.missions')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique = True)
    field_of_study = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    
    missions = db.relationship('Mission', backref = 'scientist', cascade = 'all,delete,delete-orphan')
    planets = association_proxy('missions', 'planet')
    
    @validates('name')
    def validate_scientist_name(self,key,value):
        scientists = [scientist.name for scientist in Scientist.query.all()]
        if not value:
            raise ValueError('scientist name must be provided')
        elif value in scientists:
            raise ValueError('scientist name must be unique')
        return value
    
    @validates('field_of_study')
    def validate_scientist_field_of_study(self,key,value):
        if not value:
            raise ValueError('scientist field_of_study must be provided')
        return value
    

class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'
    serialize_rules = ('-updated_at','-created_at','-missions', '-scientists.planet')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    
    missions = db.relationship('Mission', backref = 'planet', cascade = 'all,delete,delete-orphan')
    scientists = association_proxy('missions', 'scientist')