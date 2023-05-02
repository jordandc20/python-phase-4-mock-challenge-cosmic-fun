from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Scientist, Planet, Mission
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
CORS(app)
migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
class Scientists(Resource):
    def get(self):
        scientists = Scientist.query.all()
        scientist = [scientist.to_dict() for scientist in scientists]
        return make_response(scientist, 200)
    def post(self):
        json = request.get_json()
        try:
            new_scientist = Scientist(
                name = json['name'],
                field_of_study = json['field_of_study'],
                avatar = json['avatar']
            )
            db.session.add(new_scientist)
            db.session.commit()
        except Exception as ex:
            return make_response({
                'error': [ex.__str__()]
            }, 404)
        return make_response(new_scientist.to_dict(), 201)
class ScientistById(Resource):
    def get(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({
                'error': 'Scientist not found.'
            }, 404)
        return make_response(scientist.to_dict(rules = ('planets',)), 200)
    def patch(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        json = request.get_json()
        if not scientist:
            return make_response({
                'error': 'Scientist not found.'
            }, 404)
        try:
            for attr in json:
                setattr(scientist, attr, json[attr])
            db.session.add(scientist)
            db.session.commit()
        except Exception as ex:
            return make_response({
                'error': [ex.__str__()]
            }, 404)
        return make_response(scientist.to_dict(), 202)
    def delete(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({
                'error': 'Scientist not found.'
            }, 404)
        db.session.delete(scientist)
        db.session.commit()
        return make_response({}, 200)
class Planets(Resource):
    def get(self):
        planet_to_dict = [planet.to_dict() for planet in Planet.query.all()]
        return make_response(planet_to_dict, 200)
class Missions(Resource):
    def post(self):
        json = request.get_json()
        try:
            new_mission = Mission(
                name = json['name'],
                scientist_id = json['scientist_id'],
                planet_id = json['planet_id']
            )
            db.session.add(new_mission)
            db.session.commit()
        except Exception as ex:
            return make_response({
                'error': [ex.__str__()]
            }, 404)
        return make_response(new_mission.planet.to_dict(), 201)
api.add_resource(Scientists, '/scientists')
api.add_resource(ScientistById, '/scientists/<int:id>')
api.add_resource(Planets, '/planets')
api.add_resource(Missions, '/missions')
if __name__ == '__main__':
    app.run(port=5555, debug = True)