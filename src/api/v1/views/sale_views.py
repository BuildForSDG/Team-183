# #local imports
# from ..utils.sdto import sale_parser, update_sale_parser
# from ..models.sale_model import sale_ns, sales_resp

# # from ..models.carts import Cart
# # from ..models.sales import Sale
# # from ..models.user import User
# from ..utils.decorators import token_required, admin_token_required


# # third party imports
# from flask_restx import Resource
# from flask import request
# from werkzeug.exceptions import NotFound, BadRequest
# import json


# @sale_ns.route('/')
# class CreateSale(Resource):
#     @sale_ns.doc(security='Auth_token')
#     def post(self):
#         """Create Sale Order."""
#         # auth_token = None
#         # current_user_email = None
#         # if 'Authorization' in request.headers:
#         #         auth_token = request.headers['Authorization']
#         # if not auth_token:
#         #     response_object = dict(
#         #         message='Token is missing.Please log in to continue.',
#         #         status='Failed.'
#         #     )
#         #     return response_object, 401
#         # try:
#         #     current_user = User()
#         #     data = current_user.decode_jwt_token(auth_token)
#         #     if data:
#         #         current_user_email = data['sub']
#         # except:
#         #     response_object = dict(
#         #         message='Token is invalid.',
#         #         status='Failed.'
#         #     )
#         # new_sale = Sale()
#         # return new_sale.checkout(current_user_email)
#         args = sale_parser.parse_args()

#         # validate the sale payload
#         invalid_data = validate_product_data(args)
#         if invalid_data:
#             return invalid_data

#         # sale_name = args["sale_name"]
#         # sale_category = args["sale_category"]

#         # local import
#         from src import mongo
#         sales = mongo.db.sales

#         sale_id = sales.insert({
#             # 'product_category': args["product_category"],
#             'product_name': args["product_name"],
#             'products_count': args["products_count"],
#             'cart_total': args["cart_total"],

#             # 'email': args["email"],
#             'user_id': user_id,
#             'created': datetime.utcnow(),
#             # 'sale_completed': False
#         })

#         new_sale = sales.find_one({'_id': sale_id})

#         message = 'Sale with id ' + \
#             str(new_sale['_id']) + ' added successfully'
#         return {'message': message}, 201
#         # return {"message": "Sale added successfully"}, 201


# @sale_ns.route('/<string:email>')
# class GetSingleCart(Resource):
#     @sale_ns.doc(security='Auth_token')
#     @token_required
#     @sale_ns.marshal_with(sales_resp, envelope='sales')
#     def get(self, email):
#         """Gets a single Sale given user Email"""
#         # sale = Sale()
#         # data = sale.get_single_sale(email)
#         # return data

#         # local import
#         from src import mongo
#         sales = mongo.db.sales
#         salesx = sales.find({'user_id': user_id})

#         if not salesx:
#             sale_ns.abort(404, "No sales for user {}".format(user_id))

#         results = []
#         for product in salesx:
#             obj = {
#                 "product_id": str(product["_id"]),
#                 "product_name": product["product_name"],
#                 "product_category": product["product_category"],
#                 # "price": product["price"],
#                 # "status": product["status"],
#                 "user_id": product["user_id"],
#                 "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
#             }
#             results.append(obj)

#         # return results
#         return {'sales': results}, 200
#         # return sales


# @sale_ns.route('/')
# class AllSales(Resource):
#     @sale_ns.response(200, 'Success')
#     @admin_token_required
#     @sale_ns.marshal_with(sales_resp, envelope='sales')
#     @sale_ns.doc(security='Auth_token')
#     def get(self):
#         """"Gets all sales from db"""
#         # sales = Sale().get_all()
#         # return sales, 200

#         # local import
#         from src import mongo
#         salesx = mongo.db.sales
#         # salesx = sales.find({'user_id': user_id})

#         if not salesx:
#             # sale_ns.abort(404, "No sales for user {}".format(user_id))
#             sale_ns.abort(404, "No sales for found")


#         results = []
#         for product in salesx:
#             obj = {
#                 "product_id": str(product["_id"]),
#                 "product_name": product["product_name"],
#                 "product_category": product["product_category"],
#                 # "price": product["price"],
#                 # "status": product["status"],
#                 "user_id": product["user_id"],
#                 "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
#             }
#             results.append(obj)

#         # return results
#         return {'sales': results}, 200
#         # return sales
