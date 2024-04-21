from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# Request parser for the districts
district_put_args = reqparse.RequestParser()
district_put_args.add_argument("district_id", type=str, help="The ID of the district", required=True)
district_put_args.add_argument("name", type=str, help="The name of the district", required=True)

# Request parser for the stores
store_args = reqparse.RequestParser()
store_args.add_argument("id", type=str, help="The ID of the store", required=True)
store_args.add_argument("name", type=str, help="The name of the store", required=True)
store_args.add_argument("address", type=str, help="The address of the store", required=True)

# Request parser for the products
product_args = reqparse.RequestParser()
product_args.add_argument("name", type=str, help="The name of the product", required=True)
product_args.add_argument("price", type=float, help="The price of the product", required=True)

# Store structure with nested products
store_structure = {
    "id": store_args,
    "name": store_args,
    "address": store_args,
    "products": [product_args]
}

# Request parser for districts with nested stores
district_struct = {
    "id": district_put_args,
    "name": district_put_args,
    "stores": [store_structure]
}

districts = {}

# Create a resource
class District(Resource):
    def get(self, district_id):
        return districts[district_id]

    def put(self, district_id):
        args = district_put_args.parse_args()
        districts[district_id] = args
        return districts[district_id], 201

api.add_resource(District, "/district/<string:district_id>")

if __name__ == "__main__":
    app.run(debug=True)