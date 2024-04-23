from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)

class DistrictModel(db.Model):
    district_id = db.Column(db.String(15), primary_key=True)
    #store = db.Column(db.String(30), nullable=False)
    #store_id = db.Column(db.String(5))
    name = db.Column(db.String(20))
    #products = db.Column(db.String(100))
    #address = db.Column(db.String(100))
    #price = db.Column(db.Float)

    # Happens only if you choose to print the representation of the above object
    def __repr__(self):
        #return f"District(district={district}, store={store}, name={name}, products={products}, address={address}, store_id={store_id}, district_id={district_id}, price={price})"
        return f"District(district_id={self.district_id},  name={self.name})"

#db.create_all()

# Request parser for the districts
district_put_args = reqparse.RequestParser()
district_put_args.add_argument("district_id", type=str, help="The ID of the district", required=True)
district_put_args.add_argument("name", type=str, help="The name of the district", required=True)

# Update the districts
district_update_args = reqparse.RequestParser()
district_update_args.add_argument("district_id", type=str, help="The ID of the district")
district_update_args.add_argument("name", type=str, help="The name of the district")

# Request parser for the stores
store_args = reqparse.RequestParser()
store_args.add_argument("store_id", type=str, help="The ID of the store", required=True)
store_args.add_argument("name", type=str, help="The name of the store", required=True)
store_args.add_argument("address", type=str, help="The address of the store", required=True)

# Request parser for the products
product_args = reqparse.RequestParser()
product_args.add_argument("name", type=str, help="The name of the product", required=True)
product_args.add_argument("price", type=float, help="The price of the product", required=True)

# Store structure with nested products
store_structure = {
    "store_id": store_args,
    "name": store_args,
    "address": store_args,
    "products": [product_args]
}

# Request parser for districts with nested stores
district_struct = {
    "district_id": district_put_args,
    "name": district_put_args,
    "stores": [store_structure]
}

resource_fields = {
    #'district': fields.String,
    'district_id': fields.String,
    #'store': fields.String,
    #'store_id': fields.String,
    'name': fields.String,
    #'products': fields.String,
    #'address': fields.String,
    #'price': fields.Float
}


# Create a resource
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
            
        district = DistrictModel(district_id=args['district_id'], name=args['name'])
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
        if args['name']:
            result.name = args['name']
        
        db.session.commit()
        return result


    def delete(self, district_id):
        exit_if_district_id_doesnt_exist(district_id)
        del districts[district_id]
        return '', 204

api.add_resource(District, "/district/<string:district_id>")

if __name__ == "__main__":
    app.run(debug=True)