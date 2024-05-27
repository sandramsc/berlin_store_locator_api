from flask import Flask, request, render_template, jsonify, current_app
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

# Initialize SQLAlchemy extension
db = SQLAlchemy(app)

# Load JSON data
def load_json():
    try:
        json_path = os.path.join(current_app.root_path, 'berlin_store_locator.json')
        with open(json_path) as json_file:
            data = json.load(json_file)
        return data
    except Exception as error:
        current_app.logger.error(f"Error loading JSON file: {error}")
        return {}

# Save JSON data
def save_json(data):
    try:
        json_path = os.path.join(current_app.root_path, 'berlin_store_locator.json')
        with open(json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except Exception as error:
        current_app.logger.error(f"Error saving JSON file: {error}")

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
    return """ <h1> Berlin Store locator RESTful API </h1> """

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
district_fields = {
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

store_fields = {
    'store_id': fields.String,
    'store_name': fields.String,
    'address': fields.String,
    'products': fields.List(fields.Nested({
        'item': fields.String,
        'price': fields.Float
    }))
}

product_fields = {
    'item': fields.String,
    'price': fields.Float
}

class DistrictResource(Resource):
    @marshal_with(district_fields)
    def get(self, district_id):
        data = load_json()
        districts = data.get('districts', [])
        for district in districts:
            if district['district_id'] == district_id:
                return district, 200
        abort(404, message="District ID not found")

    @marshal_with(district_fields)
    def put(self, district_id):
        args = district_put_args.parse_args()
        data = load_json()

        districts = data.get('districts', [])
        for district in districts:
            if district['district_id'] == district_id:
                abort(409, message="District ID already exists.")

        try:
            stores = json.loads(args['stores'])
        except json.JSONDecodeError as e:
            return {"error": "Invalid JSON data for stores"}, 400

        new_district = {
            'district_id': args['district_id'],
            'dist_name': args['dist_name'],
            'stores': stores
        }

        districts.append(new_district)
        data['districts'] = districts
        save_json(data)
        return new_district, 201

    @marshal_with(district_fields)
    def patch(self, district_id):
        args = district_update_args.parse_args()
        data = load_json()
        districts = data.get('districts', [])
        for district in districts:
            if district['district_id'] == district_id:
                if args['district_id']:
                    district['district_id'] = args['district_id']
                if args['dist_name']:
                    district['dist_name'] = args['dist_name']
                if args['stores']:
                    try:
                        district['stores'] = json.loads(args['stores'])
                    except json.JSONDecodeError:
                        return {"error": "Invalid JSON data for stores"}, 400
                save_json(data)
                return district, 200
        abort(404, message="District ID not found")

    def delete(self, district_id):
        data = load_json()
        districts = data.get('districts', [])
        new_districts = [district for district in districts if district['district_id'] != district_id]
        if len(new_districts) == len(districts):
            abort(404, message="District ID not found")
        data['districts'] = new_districts
        save_json(data)
        return '', 204

class StoreResource(Resource):
    @marshal_with(store_fields)
    def get(self, store_id):
        data = load_json()
        stores = []
        for district in data.get('districts', []):
            stores.extend(district.get('stores', []))
        for store in stores:
            if store['store_id'] == store_id:
                return store, 200
        abort(404, message="Store ID not found")

    @marshal_with(store_fields)
    def put(self, store_id):
        args = store_put_args.parse_args()
        data = load_json()
        stores = []
        for district in data.get('districts', []):
            stores.extend(district.get('stores', []))
        for store in stores:
            if store['store_id'] == store_id:
                abort(409, message="Store ID already taken.")

        new_store = {
            'store_id': args['store_id'],
            'store_name': args['store_name'],
            'address': args['address'],
            'products': []
        }

        for district in data.get('districts', []):
            if district['district_id'] == args['district_id']:
                district['stores'].append(new_store)
                save_json(data)
                return new_store, 201
        return {"error": "District ID not found"}, 400

    @marshal_with(store_fields)
    def patch(self, store_id):
        args = store_update_args.parse_args()
        data = load_json()
        stores = []
        for district in data.get('districts', []):
            stores.extend(district.get('stores', []))
        for store in stores:
            if store['store_id'] == store_id:
                if args['store_id']:
                    store['store_id'] = args['store_id']
                if args['store_name']:
                    store['store_name'] = args['store_name']
                if args['address']:
                    store['address'] = args['address']
                save_json(data)
                return store, 200
        abort(404, message="Store ID not found")

    def delete(self, store_id):
        data = load_json()
        for district in data.get('districts', []):
            new_stores = [store for store in district.get('stores', []) if store['store_id'] != store_id]
            if len(new_stores) != len(district.get('stores', [])):
                district['stores'] = new_stores
                save_json(data)
                return '', 204
        abort(404, message="Store ID not found")

class ProductResource(Resource):
    @marshal_with(product_fields)
    def get(self, item):
        data = load_json()
        products = []
        for district in data.get('districts', []):
            for store in district.get('stores', []):
                products.extend(store.get('products', []))
        for product in products:
            if product['item'] == item:
                return product, 200
        abort(404, message="Product not found")

    @marshal_with(product_fields)
    def put(self, item):
        args = product_put_args.parse_args()
        data = load_json()
        products = []
        for district in data.get('districts', []):
            for store in district.get('stores', []):
                products.extend(store.get('products', []))
        for product in products:
            if product['item'] == item:
                abort(409, message="Product already exists.")

        new_product = {
            'item': args['item'],
            'price': args['price']
        }

        for district in data.get('districts', []):
            for store in district.get('stores', []):
                if store['store_id'] == args['store_id']:
                    store['products'].append(new_product)
                    save_json(data)
                    return new_product, 201
        return {"error": "Store ID not found"}, 400

    @marshal_with(product_fields)
    def patch(self, item):
        args = product_update_args.parse_args()
        data = load_json()
        products = []
        for district in data.get('districts', []):
            for store in district.get('stores', []):
                products.extend(store.get('products', []))
        for product in products:
            if product['item'] == item:
                if args['item']:
                    product['item'] = args['item']
                if args['price']:
                    product['price'] = args['price']
                save_json(data)
                return product, 200
        abort(404, message="Product not found")

    def delete(self, item):
        data = load_json()
        for district in data.get('districts', []):
            for store in district.get('stores', []):
                new_products = [product for product in store.get('products', []) if product['item'] != item]
                if len(new_products) != len(store.get('products', [])):
                    store['products'] = new_products
                    save_json(data)
                    return '', 204
        abort(404, message="Product not found")

api.add_resource(DistrictResource, "/district/<district_id>")
api.add_resource(StoreResource, "/store/<store_id>")
api.add_resource(ProductResource, "/product/<item>")

if __name__ == "__main__":
    app.run()
