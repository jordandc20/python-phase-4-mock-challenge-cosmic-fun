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
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable = False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable = False)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    @validates('name')
    def validates_name(self, key, value):
        if not value:
            raise ValueError('Name is required.')
        return value
    @validates('scientist_id')
    def validates_scientist_id(self, key, value):
        scientists = Scientist.query.all()
        scientist_id = [scientist.id for scientist in scientists]
        if not value:
            raise ValueError('Scientist is required.')
        elif not value in scientist_id:
            raise ValueError('Scientist does not exist.')
        return value
    @validates('planet_id')
    def validates_planet_id(self, key, value):
        planets = Planet.query.all()
        planet_id = [planet.id for planet in planets]
        if not value:
            raise ValueError('Planet is required.')
        elif not value in planet_id:
            raise ValueError('Planet does not exist.')
        return value
    def __repr__(self):
        return f'Name: {self.name}, Scientist_id: {self.scientist_id}, Planet_id: {self.planet_id}'
class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'
    serialize_rules = ('-missions', '-created_at', '-updated_at')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False, unique = True)
    field_of_study = db.Column(db.String, nullable = False)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    missions = db.relationship('Mission', backref = 'scientist', cascade = 'all, delete, delete-orphan')
    planets = association_proxy('missions', 'planet')
    @validates('name')
    def validates_name(self, key, value):
        if not value:
            raise ValueError('Name is required.')
        return value
    @validates('field_of_study')
    def validates_field_of_study(self, key, value):
        if not value:
            raise ValueError('Field of study is required.')
        return value
    def __repr__(self):
        return f'Name: {self.name}, Field_of_study: {self.field_of_study}, avatar: {self.avatar}'
class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'
    serialize_rules = ('-missions', '-created_at', '-updated_at')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable = False)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())
    missions = db.relationship('Mission', backref = 'planet', cascade = 'all, delete, delete-orphan')
    scientists = association_proxy('missions', 'scientist')
    def __repr__(self):
        return f'Planet name: {self.name}, distance_from_earth: {self.distance_from_earth}, nearest_star: {self.nearest_star}, image: {self.image}'






