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
    except Exeption as error:
        current_app.logger.error(f"Error loading JSON file: {error}")
        return "Error loading JSON file", 500

@app.route('/api/v1/resources/districts/all', methods=['GET'])
def get_districts():
    data = load_json()
    if data:
        return jsonify(data.get('districts'))
    else:
        return "Erorr loading JSON file", 500

@app.route('/api/v1/resources/stores/all', methods=['GET'])
def get_stores():
    data = load_json()
    if data:
        return jsonify(data.get('stores'))
    else:
        return "Erorr loading JSON file", 500

@app.route('/showjson', methods=['GET'])
def showjson():
    data = load_json()
    if data:
        return render_template('showjson.jade', data=data)
    else:
        return "Error loading JSON file", 500
      
class DistrictModel(db.Model):
    district_id = db.Column(db.String(15), primary_key=True)
    store_id = db.Column(db.String(5), nullable=False)
    store_name = db.Column(db.String(30))
    dist_name = db.Column(db.String(20))
    #products = db.Column(db.String(100))
    address = db.Column(db.String(100))
    #price = db.Column(db.Float)

    # Happens only if you choose to print the representation of the above object
    def __repr__(self):
        #return f"Store(store_id={self.store_id}, store_name={self.name}, address={self.address})"
        return f"District(district_id={self.district_id},  dist_name={self.dist_name})"

db.create_all()

# Request parser for the districts
district_put_args = reqparse.RequestParser()
district_put_args.add_argument("district_id", type=str, help="The ID of the district", required=True)
district_put_args.add_argument("dist_name", type=str, help="The name of the district", required=True)

# Update the districts
district_update_args = reqparse.RequestParser()
district_update_args.add_argument("district_id", type=str, help="The ID of the district")
district_update_args.add_argument("dist_name", type=str, help="The name of the district")

# Request parser for the stores
store_put_args = reqparse.RequestParser()
store_put_args.add_argument("store_id", type=str, help="The ID of the store", required=True)
store_put_args.add_argument("store_name", type=str, help="The name of the store", required=True)
store_put_args.add_argument("address", type=str, help="The address of the store", required=True)

# Update the stores
store_update_args = reqparse.RequestParser()
store_update_args.add_argument("store_id", type=str, help="The ID of the store", required=True)
store_update_args.add_argument("store_name", type=str, help="The name of the store", required=True)
store_update_args.add_argument("address", type=str, help="The address of the store", required=True)

# Request parser for the store address
address_put_args = reqparse.RequestParser()
address_put_args.add_argument("address", type=str, help="The address of the store", required=True)

# Update the store address
address_update_args = reqparse.RequestParser()
address_update_args.add_argument("address", type=str, help="The address of the store", required=True)

# Request parser for the products
product_put_args = reqparse.RequestParser()
product_put_args.add_argument("item", type=str, help="The name of the product", required=True)
product_put_args.add_argument("price", type=float, help="The price of the product", required=True)

# Update the products
product_update_args = reqparse.RequestParser()
product_update_args.add_argument("item", type=str, help="The name of the product", required=True)
product_update_args.add_argument("price", type=float, help="The price of the product", required=True)

# Request parser for districts with nested stores
district_struct = {
    "district_id": district_put_args,
    "dist_name": district_put_args,
    "stores": [store_struct]
}

# Request parser for Stores with nested products
store_struct = {
    "store_id": store_args,
    "store_name": store_args,
    "address": store_args,
    "products": [product_args]
}

resource_fields = {
    #'district': fields.String,
    'district_id': fields.String,
    'store_name': fields.String,
    'store_id': fields.String,
    'dist_name': fields.String,
    #'products': fields.String,
    'address': fields.String,
    #'price': fields.Float
}


# Create a resource for District
class District(Resource):
    @marshal_with(resource_fields)
    def get(self, district_id):
        result = DistrictModel.query.filter_by(district_id=district_id).first()
        if not result:
            abort(404, message="District ID not found")
        return result

    @marshal_with(resource_fields)
    def put(self, district_id):
        args = district_put_args.parse_args()
        print("Received arguments:", args)
        result = DistrictModel.query.filter_by(district_id=district_id).first()
        if result:
            abort(409, message="District ID already taken.")
            
        district = DistrictModel(district_id=args['district_id'], dist_name=args['dist_name'])
        print("New district to be inserted", district)
        db.session.add(district)
        db.session.commit()
        print("District inserted successfully!")
        return district, 201

    @marshal_with(resource_fields)
    def patch(self, district_id):
        args = district_update_args.parse_args()
        result = DistrictModel.query.filter_by(district_id=district_id).first()
        if not result:
            abort(404, message="District doesn't exist, therefore cannot update.") 

        # Check if values are not None - that they exist
        if args['district_id']:
            result.district_id = args['district_id']
        if args['dist_name']:
            result.dist_name = args['dist_name']
        
        db.session.commit()
        return result


    def delete(self, district_id):
        exit_if_district_id_doesnt_exist(district_id)
        del districts[district_id]
        return '', 204


# Create a resource for Store
class Store(Resource):
    @marshal_with(resource_fields)
    def get(self, store_id):
        result = StoreModel.query.filter_by(store_id=store_id).first()
        if not result:
            abort(404, message="Store ID not found")
        return result

    @marshal_with(resource_fields)
    def put(self, store_id):
        args = store_put_args.parse_args()
        print("Received arguments:", args)
        result = StoreModel.query.filter_by(store_id=store_id).first()
        if result:
            abort(409, message="Store ID already taken.")
            
        store = StoreModel(store_id=args['store_id'], store_name=args['store_name'], address=args['address'])
        print("New store to be inserted", store)
        db.session.add(store)
        db.session.commit()
        print("Store inserted successfully!")
        return store, 201

    @marshal_with(resource_fields)
    def patch(self, store_id):
        args = store_update_args.parse_args()
        result = StoreModel.query.filter_by(store_id=store_id).first()
        if not result:
            abort(404, message="Store doesn't exist, therefore cannot update.") 

        # Check if values are not None - that they exist
        if args['store_id']:
            result.store_id = args['store_id']
        if args['store_name']:
            result.store_name = args['store_name']
        if args['address']:
            result.address = args['address']
        
        db.session.commit()
        return result


    def delete(self, store_id):
        exit_if_store_id_doesnt_exist(store_id)
        del stores[store_id]
        return '', 204

api.add_resource(District, "/district/<string:district_id>")
api.add_resource(Store, "/store/<string:store_id>")

if __name__ == "__main__":
    app.run()