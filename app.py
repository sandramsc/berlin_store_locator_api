from flask import Flask, request, render_template, jsonify, url_for, current_app
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
api = Api(app)

# Set the SQLAlchemy database connection URI
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"

# Set the debug mode to True/False 
app.config["DEBUG"] = True

# Initialize SQLAlchemy extention
db = SQLAlchemy(app)

def load_json():
    try:
        json_path = os.path.join(current_app.root_path, 'berlin_store_locator.json')
        with open(json_path) as json_file:
            data = json.load(json_file)
        return data
    except Exception as error:
        current_app.logger.error(f"Error loading JSON file: {error}")
        return data

# Routes to retrieve all districts, stores, and products
@app.route('/districts/all')
def get_all_districts():
    districts = load_json().get('districts', [])
    return jsonify(districts)

@app.route('/stores/all')
def get_all_stores():
    districts = load_json().get('districts', [])
    stores = [store for district in districts for store in district.get('stores', [])]
    return jsonify(stores)

@app.route('/products/all')
def get_all_products():
    districts = load_json().get('districts', [])
    products = [product for district in districts for store in district.get('stores', []) for product in store.get('products', [])]
    return jsonify(products)
    
@app.route('/showjson', methods=['GET'])
def showjson():
    data = load_json()
    if data:
        return render_template('showjson.jade', data=data)
    else:
        return "Error loading JSON file", 500

# Define the database models
class District(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    district_id = db.Column(db.String(50), nullable=False, unique=True)
    dist_name = db.Column(db.String(100), nullable=False)
    stores = db.relationship('Store', backref='district', lazy=True)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.String(50), nullable=False, unique=True)
    store_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    district_id = db.Column(db.String(50), db.ForeignKey('district.district_id'), nullable=False)
    products = db.relationship('Product', backref='store', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    store_id = db.Column(db.String(50), db.ForeignKey('store.store_id'), nullable=False)

# Create the database tables
db.create_all()

@app.route('/', methods=['GET'])
def home():
    return """ <h1> Berlin Store locator RESTful API </h1>
     <p>description here</p> """


def load_json():
    try:
        json_path = os.path.join(current_app.root_path, 'berlin_store_locator.json')
        with open(json_path) as json_file:
            data = json.load(json_file)
        return data
    except Exception as error:
        current_app.logger.error(f"Error loading JSON file: {error}")
        return {}


# Request parser for PUT and PATCH requests for District
district_put_args = reqparse.RequestParser()
district_put_args.add_argument("district_id", type=str, help="ID of the district", required=True)
district_put_args.add_argument("dist_name", type=str, help="Name of the district", required=True)
district_put_args.add_argument("stores", type=str, help="Stores in the district", required=True)

district_update_args = reqparse.RequestParser()
district_update_args.add_argument("district_id", type=str, help="ID of the district")
district_update_args.add_argument("dist_name", type=str, help="Name of the district")
district_update_args.add_argument("stores", type=str, help="Stores in the district")

# Request parser for PUT and PATCH requests for Store
store_put_args = reqparse.RequestParser()
store_put_args.add_argument("store_id", type=str, help="ID of the store", required=True)
store_put_args.add_argument("store_name", type=str, help="Name of the store", required=True)
store_put_args.add_argument("address", type=str, help="Address of the store", required=True)

store_update_args = reqparse.RequestParser()
store_update_args.add_argument("store_id", type=str, help="ID of the store")
store_update_args.add_argument("store_name", type=str, help="Name of the store")
store_update_args.add_argument("address", type=str, help="Address of the store")

# Request parser for PUT and PATCH requests for Product
product_put_args = reqparse.RequestParser()
product_put_args.add_argument("item", type=str, help="Name of the product", required=True)
product_put_args.add_argument("price", type=float, help="Price of the product", required=True)

product_update_args = reqparse.RequestParser()
product_update_args.add_argument("item", type=str, help="Name of the product")
product_update_args.add_argument("price", type=float, help="Price of the product")

# Resource fields for marshalling
resource_fields = {
    'district_id': fields.String,
    'dist_name': fields.String,
    'stores': fields.List(fields.Nested({
        'store_id': fields.String,
        'store_name': fields.String,
        'address': fields.String,
        'products': fields.List(fields.Nested({
            'item': fields.String,
            'price': fields.Float
        }))
    }))
}


class District(Resource):
    @marshal_with(resource_fields)
    def get(self, district_id):
        data = load_json()
        if district_id not in data.get('districts', {}):
            abort(404, message="District ID not found")
        return data['districts'][district_id], 200

    @marshal_with(resource_fields)
    def put(self, district_id):
        args = district_put_args.parse_args()
        data = load_json()

        # Ensure 'districts' is a dictionary
        if 'districts' not in data or not isinstance(data['districts'], dict):
            data['districts'] = {}

        # Add error handling and print statement here
        try:
            stores_data = args.get("stores", "")
            print("Stores data:", stores_data)  # Print the stores data for inspection
            stores = json.loads(stores_data)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            return {"error": "Invalid JSON data"}, 400  # Return an error response

        # Create district instance
        district = {
            'district_id': args['district_id'],
            'dist_name': args['dist_name'],
            "stores": stores
        }

        data['districts'][district_id] = district
        return district, 201


    @marshal_with(resource_fields)
    def patch(self, district_id):
        args = district_update_args.parse_args()
        data = load_json()
        if district_id not in data.get('districts', {}):
            abort(404, message="District ID not found")

        district = data['districts'][district_id]
        if args['district_id']:
            district['district_id'] = args['district_id']
        if args['dist_name']:
            district['dist_name'] = args['dist_name']
        if args['stores']:
            district['stores'] = json.loads(args['stores'])

        return district

    def delete(self, district_id):
        data = load_json()
        if district_id not in data.get('districts', {}):
            abort(404, message="District ID not found")
        del data['districts'][district_id]
        return '', 204

class Store(Resource):
    @marshal_with(resource_fields)
    def get(self, store_id):
        data = load_json()
        if store_id not in data.get('stores', {}):
            abort(404, message="Store ID not found")
        return data['stores'][store_id], 200

    @marshal_with(resource_fields)
    def put(self, store_id):
        args = store_put_args.parse_args()
        data = load_json()
        if store_id in data.get('stores', {}):
            abort(409, message="Store ID already taken.")

        store = {
            'store_id': args['store_id'],
            'store_name': args['store_name'],
            'address': args['address']
        }
        data['stores'][store_id] = store
        return store, 201

    @marshal_with(resource_fields)
    def patch(self, store_id):
        args = store_update_args.parse_args()
        data = load_json()
        if store_id not in data.get('stores', {}):
            abort(404, message="Store ID not found")

        store = data['stores'][store_id]
        if args['store_id']:
            store['store_id'] = args['store_id']
        if args['store_name']:
            store['store_name'] = args['store_name']
        if args['address']:
            store['address'] = args['address']

        return store

    def delete(self, store_id):
        data = load_json()
        if store_id not in data.get('stores', {}):
            abort(404, message="Store ID not found")
        del data['stores'][store_id]
        return '', 204

class Product(Resource):
    @marshal_with(resource_fields)
    def get(self, item):
        data = load_json()
        if item not in data.get('products', {}):
            abort(404, message="Product not found")
        return data['products'][item], 200

    @marshal_with(resource_fields)
    def put(self, item):
        args = product_put_args.parse_args()
        data = load_json()
        if item in data.get('products', {}):
            abort(409, message="Product already taken.")

        product = {
            'item': args['item'],
            'price': args['price']
        }
        data['products'][item] = product
        return product, 201

    @marshal_with(resource_fields)
    def patch(self, item):
        args = product_update_args.parse_args()
        data = load_json()
        if item not in data.get('products', {}):
            abort(404, message="Product not found")

        product = data['products'][item]
        if args['item']:
            product['item'] = args['item']
        if args['price']:
            product['price'] = args['price']

        return product

    def delete(self, item):
        data = load_json()
        if item not in data.get('products', {}):
            abort(404, message="Product not found")
        del data['products'][item]
        return '', 204

api.add_resource(District, "/district/<string:district_id>")
api.add_resource(Store, "/store/<string:store_id>")
api.add_resource(Product, "/product/<string:item>")


if __name__ == "__main__":
    app.run()