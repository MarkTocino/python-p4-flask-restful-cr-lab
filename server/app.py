#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        plant_dict = [p.to_dict() for p in plants]
        response = make_response(jsonify(plant_dict), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    def post(self):
        data = request.get_json()
        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
            # name=request.form['name'],
            # image=request.form['image'],
            # price=request.form['price']
        )
        db.session.add(new_plant)
        db.session.commit()
        response_dict = new_plant.to_dict()
        response = make_response(
        jsonify(response_dict),
        201)
        response.headers['Content-Type'] = 'application/json'
        return response
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plants = Plant.query.filter(Plant.id == id).first()
        plant_dict = plants.to_dict()
        response = make_response(jsonify(plant_dict), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
api.add_resource(PlantByID,'/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
