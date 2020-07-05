# local imports
from ..utils.cartdto import cart_parser
# from ..utils.cartdto import cart_parser, update_cart_parser
# from ..models.cart_model import cart_ns, cart_model, carts_resp
from ..models.cart_model import cart_ns, cart_model

# cart_ns = cart_ns
# cart_model = cart_model
# carts_resp = carts_resp
# from ..models.products import Product
# from ..models.carts import Cart
# from ..models.user import User
# from ..utils.validators import validate_product_data
# from ..utils.validators import validate_product_data, validate_update_product
from ..utils.decorators import token_required


# third party imports
from flask_restx import Resource
from datetime import datetime
from flask import jsonify
# from werkzeug.exceptions import NotFound, BadRequest
# import json


# @cart_ns.route('carts/<int:product_id>')
class PostCart(Resource):

    @cart_ns.expect(cart_model, validate=True)
    @token_required
    @cart_ns.doc(security='apikey')
    @cart_ns.header(
        'token',
        type=str,
        description='access token')
    def post(user_id, self, product_id):
        """
        Add a product to Cart
        """

        # data = json.loads(request.data.decode().replace("'", '"'))
        # quantity = data['quantity']
        # new_cart = Cart()
        # return new_cart.post_cart(product_id, quantity,
        # current_user_email)

        args = cart_parser.parse_args()

        quantity = args["quantity"]

        # validate the sale payload
        # invalid_data = validate_product_data(args)
        # if invalid_data:
        #     return invalid_data

        # local import
        from src import mongo
        carts = mongo.db.carts
        products = mongo.db.products

        product = products.find_one({'_id': product_id})
        # print(product)

        product_name = product['product_name']
        # product_name = product['product_name'].lower()
        # print(product_name)

        stock = int(product['inventory'])
        if stock < int(quantity):
            response = dict(
                status='Failed',
                message="Not enough {} in stock.Only {} remaining".format(
                    product_name,
                    product['inventory']))
            return response

        unit_price = int(product['price'])

        price = int(quantity) * unit_price

        cart_id = carts.insert({
            # 'product_id': args["product_id"],
            'product_id': product_id,
            # 'product_name': args["product_name"],
            'product_name': product_name,

            # 'products_count': args["products_count"],
            # 'cart_total': args["cart_total"],
            # 'quantity': args["quantity"],
            'quantity': quantity,


            'price': price,
            'user_id': user_id,
            'created': datetime.utcnow(),
            # 'sale_completed': False
        })

        remaining_stock = stock - quantity

        product_obj = {
            "inventory": remaining_stock,
            # "product_category": args["product_category"],
            # 'updated': datetime.utcnow(),
        }

        # product['product_name'] = args["product_name"],
        # product['product_category'] = args["product_category"],
        # products.save(product)

        products.update_one(product, {"$set": product_obj})

        new_cart = carts.find_one({'_id': cart_id})

        # message = 'Cart with id ' + \
        #     str(new_cart['_id']) + ' created successfully'
        # return {'message': message}, 201

        cart_item = dict(
            product_name=product_name,
            product_id=str(product_id),
            quantity=quantity,
            unit_price=unit_price,
            Total_price=price
        )
        response_obj = dict(
            message='cart posted successfully.',
            cart_item=cart_item,
            remaining_stock=remaining_stock

        )
        return response_obj, 201


# @cart_ns.route('/carts/<string:user_id>')
class GetSingleCart1(Resource):
    # @cart_ns.doc(security='Auth_token')
    # @token_required
    # @cart_ns.marshal_with(carts_resp, envelope='Cart_record')
    @token_required
    @cart_ns.doc(security='apikey')
    @cart_ns.header(
        'token',
        type=str,
        description='access token')
    # def get(self, user_id):
    def get(user_id, self):
        """Gets a single Cart given a user's ID"""
        # cart = Cart()
        # data = cart.get_single_cart(user_id)
        # return data
        # print(user_id)
        # local import
        from src import mongo
        carts = mongo.db.carts
        cartsx = carts.find({'user_id': user_id})
        print(type(carts.count()))

        if not cartsx:
            cart_ns.abort(404, "No carts for user {}".format(user_id))

        results = []
        for product in cartsx:
            obj = {
                "cart_id": str(product["_id"]),
                "product_name": product["product_name"],
                "product_id": str(product["product_id"]),
                # "product_names": product["product_names"],
                # "products_count": product["products_count"],
                # "cart_total": product["cart_total"],
                "quantity": product["quantity"],

                "price": product["price"],
                # "status": product["status"],
                "user_id": product["user_id"],
                "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
            }
            results.append(obj)

        return {'cart_record': results}, 200

        # return jsonify( {"cart_record": str(cartsx)})
        # return {"cart_record": str(cartsx)}, 200


# @cart_ns.route('/carts')
class AllCarts(Resource):
    @cart_ns.response(200, 'Success')
    # @cart_ns.marshal_with(carts_resp, envelope='Carts')
    # @cart_ns.doc(security='Auth_token')
    @token_required
    # @admin_token_required
    @cart_ns.doc(security='apikey')
    @cart_ns.header(
        'token',
        type=str,
        description='access token')
    # def get(self):
    def get(user_id, self):
        # def get(self, user_id):
        """"Gets all products from db"""
        # Carts = Cart().get_all()
        # return Carts, 200
        # print(user_id)
        # local import
        from src import mongo
        carts = mongo.db.carts
        cartsx = carts.find()

        if not cartsx:
            cart_ns.abort(404, "No carts for found")

        results = []
        for product in cartsx:
            obj = {
                "cart_id": str(product["_id"]),
                "quantity": product["quantity"],
                # "cart_name": product["product_name"],
                # "product_names": product["product_names"],
                # "products_count": product["products_count"],
                # "cart_total": product["cart_total"],
                # "product_category": product["product_category"],
                # "price": product["price"],
                # "status": product["status"],
                # "user_id": product["user_id"],
                "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
            }
            results.append(obj)

        return jsonify(
            {"message": "All carts listed successfully",
             "carts_count": carts.count(),
             "carts": results
             })
