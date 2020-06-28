# # local imports
# from ..utils.pdto import product_parser, update_product_parser, product_parser_resp, update_product_parser_resp
# from ..models.product_model import product_ns, product_mod, product_resp, product_update_resp

# # from ..models.products import Product
# from ..utils.decorators import token_required, admin_token_required
# from ..utils.validators import validate_product_data, validate_update_product

# # third party imports
# from flask_restx import Resource
# from datetime import datetime
# from flask import request, jsonify
# from werkzeug.exceptions import NotFound, BadRequest
# import json


# @product_ns.route('/')
# class Products(Resource):

#     @product_ns.response(201, 'Product created successfully')
#     @product_ns.doc(security='Auth_token')
#     @admin_token_required
#     @product_ns.expect(product_mod, validate=True)
#     def post(user_id, self):
#         """Creates a new Product  (Admin Only)."""
#         # data = json.loads(request.data.decode().replace("'", '"'))
#         args = product_parser_resp.parse_args()

#         product_name = args['product_name']
#         inventory = args['inventory']
#         min_quantity = args['min_quantity']
#         category = args['category']
#         price = args['price']
#         if product_name == '':
#             resp = dict(
#                 status='Failed.',
#                 message='Product Name cannot be empty.'
#             )
#             return resp, 400

#         # product = Product(product_name, inventory,
#         #                   min_quantity, category, price)

#         # product.save_product()

#         # validate the product payload
#         invalid_data = validate_product_data(args)
#         if invalid_data:
#             return invalid_data

#         # local import
#         from src import mongo
#         products = mongo.db.products

#         product_id = products.insert({
#             'product_name': product_name,
#             'inventory': inventory,
#             'category': category,
#             'price': price,
#             'user_id': user_id,
#             'created': datetime.utcnow(),
#             # 'sale_completed': False
#         })

#         # new_product = products.find_one({'_id': product_id})
#         # message = 'Product with id ' + \
#         #     str(new_product['_id']) + ' added successfully'
#         # return {'message': message}, 201

#         new_product = dict(
#             product_name=product_name.lower(),
#             Stock_count=inventory,
#             Category=category.lower(),
#             Price_per_unit=price,
#             Minimum_quantity=min_quantity
#         )

#         resp = dict(message="successfully created.",
#                     new_product=new_product
#                     )

#         return resp, 201

#     @product_ns.response(200, 'Success')
#     # @product_ns.doc(security='Auth_token')
#     # @token_required
#     @product_ns.marshal_list_with(product_resp, envelope='products')
#     @token_required
#     @product_ns.doc(security='apikey')
#     @product_ns.header(
#         'x-access-token',
#         type=str,
#         description='access token')
#     def get(self):
#         """"Gets all products from db"""
#         # products = Product().get_all()
#         # return products

#         # local import
#         from src import mongo
#         products = mongo.db.products
#         productsx = products.find()

#         if not productsx:
#             product_ns.abort(404, "No products for found")

#         results = []
#         for product in productsx:
#             obj = {
#                 # "product_id": str(product["_id"]),
#                 "product_name": product["product_name"],
#                 # "product_names": product["product_names"],
#                 # "products_count": product["products_count"],
#                 # "cart_total": product["cart_total"],

#                 "product_category": product["product_category"],
#                 # "price": product["price"],
#                 # "status": product["status"],
#                 "user_id": product["user_id"],
#                 "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
#             }
#             results.append(obj)

#         return jsonify(
#             {"message": "All products listed successfully", "products": results})


# @product_ns.route('/<int:product_id>')
# class OneProduct(Resource):
#     # @product_ns.doc(security='Auth_token')
#     # @token_required
#     @product_ns.marshal_with(product_resp, envelope='product')
#     @token_required
#     @product_ns.doc(security='apikey')
#     @product_ns.header(
#         'x-access-token',
#         type=str,
#         description='access token')
#     def get(user_id, self, product_id):
#         """Gets a single  product given a product ID"""

#         # product = Product()
#         # data = product.get_single_product(product_id)
#         # return data

#         # local import
#         from src import mongo
#         products = mongo.db.products

#         product = products.find_one({'_id': product_id})

#         if product["user_id"] != str(user_id):
#             product_ns.abort(401, "Unauthorized to view this product")

#         # return product
#         return jsonify(product)

#     @product_ns.doc(security='Auth_token')
#     # @admin_token_required
#     @product_ns.expect(product_update_resp, validate=False)
#     @product_ns.marshal_with(product_resp)
#     @token_required
#     @product_ns.doc(security='apikey')
#     @product_ns.header(
#         'x-access-token',
#         type=str,
#         description='access token')
#     def put(user_id, self, product_id):
#         """Updates product details"""
#         # product = Product()
#         # existing_prd = Product().get_single_product(product_id)
#         # data = json.loads(request.data.decode().replace("'", '"'))

#         args = update_product_parser_resp.parse_args()

#         # inventory = existing_prd[0]['inventory']
#         # if 'inventory' in data:
#         #     inventory = data['inventory']
#         # min_quantity = existing_prd[0]['min_quantity']
#         # if 'min_quantity' in data:
#         #     min_quantity = data['min_quantity']
#         # price = existing_prd[0]['price']
#         # if 'price' in data:
#         #     price = data['price']

#         # updated_product = product.update_product(
#         #     inventory, min_quantity, price, product_id)

#         # return updated_product

#         # local	 import
#         from src import mongo
#         products = mongo.db.products
#         product = products.find_one({'_id': product_id})

#         if not product:
# return {'warning': 'No product exists with that id'}, 200

#         if product["user_id"] != str(user_id):
#             product_ns.abort(
#                 401, "Unauthorized to delete this product")

#         invalid_data = validate_update_product(product, args)
#         if invalid_data:
#             return invalid_data

#         product_obj = {
#             "min_quantity": args["min_quantity"],
#             "inventory": args["inventory"],
#             "price": args["price"],
#             'updated': datetime.utcnow(),
#         }

#         # product['product_name'] = args["product_name"],
#         # product['product_category'] = args["product_category"],
#         # products.save(product)

#         products.update_one(product, {"$set": product_obj})

#         return jsonify(
#             {"message": "Product updated successfully", "product": product})
