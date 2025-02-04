

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant  

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'  # Database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False  

migrate = Migrate(app, db)
db.init_app(app)


api = Api(app)

class Plants(Resource):

    def get(self):
        """Get all plants."""
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        """Create a new plant."""
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)


# Add the resource to the API at the `/plants` endpoint
api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        """Get a plant by its ID."""
        plant = Plant.query.filter_by(id=id).first()
        if plant:
            return make_response(jsonify(plant.to_dict()), 200)
        return make_response(jsonify({'message': 'Plant not found'}), 404)

    def patch(self, id):
        """Update a plant's "is_in_stock" value by ID."""
        plant = Plant.query.filter_by(id=id).first()

        if plant:
            data = request.get_json()
            if 'is_in_stock' in data:
                plant.is_in_stock = data['is_in_stock']
                db.session.commit()

            return make_response(jsonify(plant.to_dict()), 200)

        return make_response(jsonify({'message': 'Plant not found'}), 404)
   
    def delete(self, id):
        """Delete a plant by ID."""
        plant = Plant.query.filter_by(id=id).first()

        if plant:
            db.session.delete(plant)
            db.session.commit()
            return '', 204  

        return make_response(jsonify({'message': 'Plant not found'}), 404)

api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
