from flask import jsonify, request
from flask_restful import Resource
from models import db, Restaurant, RestaurantPizza, Pizza

class RestaurantListResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return jsonify([restaurant.to_dict() for restaurant in restaurants])

class RestaurantResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        return jsonify(restaurant.to_dict())

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204

class PizzaListResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return jsonify([pizza.to_dict() for pizza in pizzas])

class RestaurantPizzaResource(Resource):
    def post(self):
        data = request.get_json()
        price = data.get('price')
        pizza_id = data.get('pizza_id')
        restaurant_id = data.get('restaurant_id')

        if not (price and pizza_id and restaurant_id):
            return {"errors": ["price, pizza_id, and restaurant_id are required"]}, 400
        
        pizza = Pizza.query.get(pizza_id)
        if not pizza:
            return {"errors": ["Pizza not found"]}, 404
        
        restaurant = Restaurant.query.get(restaurant_id)
        if not restaurant:
            return {"errors": ["Restaurant not found"]}, 404

        # Create RestaurantPizza
        restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
        db.session.add(restaurant_pizza)
        db.session.commit()

        return jsonify(restaurant_pizza.to_dict()), 201
