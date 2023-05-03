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


@app.route('/')
def index():
    response = make_response(
        {"message": "Hello Scientists!"}
    )
    return response


class Scientists(Resource):
    def get(self):
        scientists = Scientist.query.all()
        scientists_dict = [scientist.to_dict() for scientist in scientists]
        return make_response(scientists_dict, 200)

    def post(self):
        data = request.get_json()
        try:
            scientist = Scientist(
                name=data['name'],
                field_of_study=data['field_of_study'],
                avatar=data['avatar']
            )
            db.session.add(scientist)
            db.session.commit()
        except Exception as ex:
            return make_response({'error': [ex.__str__()]}, 422)

        return make_response(scientist.to_dict(), 201)


api.add_resource(Scientists, '/scientists')


class ScientistById(Resource):
    def get(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({'error': 'Scientist not found'}, 404)
        return make_response(scientist.to_dict(rules=('planets',)), 200)

    def patch(self, id):
        data = request.get_json()
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({'error': 'Scientist not found'}, 404)
        try:
            for attr in data:
                setattr(scientist,attr,data[attr])
            db.session.add(scientist)
            db.session.commit()
        except Exception as ex:
            return make_response({'error': [ex.__str__()]}, 422)
        return make_response(scientist.to_dict(),202)

    def delete(self, id):
        scientist = Scientist.query.filter_by(id=id).first()
        if not scientist:
            return make_response({'error': 'Scientist not found'}, 404)
        db.session.delete(scientist)
        db.session.commit()
        return make_response("", 200)

api.add_resource(ScientistById, '/scientists/<int:id>')


class Planets(Resource):
    def get(self):
        planets  = Planet.query.all()
        planet_dict = [planet.to_dict() for planet in planets]
        return make_response(planet_dict, 200 )

api.add_resource(Planets, '/planets')

class Missions(Resource):
    def post(self):
        data = request.get_json()
        try:
            mission = Mission(
                name= data['name'],
                scientist_id= data['scientist_id'],
                planet_id= data['planet_id']
            )
            db.session.add(mission)
            db.session.commit()
        except Exception as ex:
            return make_response({'errors':[ex.__str__()]},422)
        print(mission.planet.to_dict())
        return make_response (mission.planet.to_dict(),201)
api.add_resource(Missions, '/missions')

if __name__ == '__main__':
    app.run(port=5555)
