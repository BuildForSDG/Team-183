# local imports
from ..utils.sdto import update_sale_parser, sale_parser_resp
# from ..models.sale_model import sale_ns, sales, post_sales
# from ..models.sale_model import sale_ns, post_sales
# from ..models.sale_model import salesr, sale_ns, post_sales, sales_resp
from ..models.sale_model import salesr, sale_ns, post_sales
from ..models.cart_model import cart_ns

# from ..utils.decorators import token_required
# from ..utils.validators import validate_product_data, validate_update_product
from ..utils.validators import validate_update_product

from ..utils.decorators import token_required, admin_token_required


# third-party imports
# from flask_restx import Resource, fields
from flask_restx import Resource
from datetime import datetime
from flask import jsonify
# from werkzeug.exceptions import NotFound, BadRequest
# import json

# @sale_ns.route("/sales")


class SaleList(Resource):

    """Displays a list of all sales and lets you POST to add new sales."""

    # @sale_ns.expect(post_sales)
    # @sale_ns.expect(sales_resp)
    # @sale_ns.expect(salesr)
    @sale_ns.doc('adds a sale')
    @sale_ns.response(201, "Created")
    @token_required
    @sale_ns.doc(security='apikey')
    @sale_ns.header(
        'token',
        type=str,
        description='access token')
    def post(user_id, self):
        """Creates a new Sale."""
        # args = sale_parser.parse_args()

        # print(args["product_names"])

        # validate the sale payload
        # invalid_data = validate_product_data(args)
        # if invalid_data:
        #     return invalid_data

        # local import
        from src import mongo
        sales = mongo.db.sales
        carts = mongo.db.carts

        cartsx = carts.find({'user_id': user_id})

        if not cartsx:
            cart_ns.abort(404, "No carts for user {}".format(user_id))

        product_names = []
        products_count = 0
        cart_total = 0

        for cart in cartsx:
            product_names.append(cart['product_name'])
            products_count += cart['quantity']
            cart_total += cart['price']

        if not cart_total:
            cart_ns.abort(404, "No carts for user {}".format(user_id))

        sale_id = sales.insert({
            # 'product_category': args["product_category"],
            # 'product_name': args["product_name"],
            # 'product_names': args["product_names"],
            # 'products_count': args["products_count"],
            'product_names': product_names,
            'products_count': products_count,
            'cart_total': cart_total,

            # 'cart_total': args["cart_total"],
            # 'email': args["email"],
            'user_id': user_id,
            'created': datetime.utcnow(),
            # 'sale_completed': False
        })

        carts.delete_many({'user_id': user_id})
        # carts.delete_one(cart)

        new_sale = sales.find_one({'_id': sale_id})

        message = 'Sale order with id ' + \
            str(new_sale['_id']) + ' created successfully'
        return {'message': message}, 201
        # return {"message": "Sale added successfully"}, 201

        # response = dict(
        #         status="success",
        #         Message='Sale Order created.'
        #     )
        # return response

    @sale_ns.doc("list_sales")
    @sale_ns.response(404, "Sales Not Found")
    # @sale_ns.marshal_list_with(sales, envelope="sales")
    # @admin_token_required
    @token_required
    @sale_ns.doc(security='apikey')
    @sale_ns.header(
        'token',
        type=str,
        description='access token')
    def get(user_id, self):
        """List all Sales by user"""
        # local import
        from src import mongo
        sales = mongo.db.sales
        salesx = sales.find({'user_id': user_id})

        if not salesx:
            sale_ns.abort(404, "No sales for user {}".format(user_id))

        results = []
        for product in salesx:
            # pcount = '' if not product["products_count"] else product["products_count"],

            obj = {
                "sale_id": str(product["_id"]),
                "product_names": product["product_names"],
                # "product_name": product["product_name"],
                "cart_total": product["cart_total"],
                "products_count": product["products_count"],
                # "product_name": pname,

                # "product_category": product["product_category"],
                # "price": product["price"],
                # "quantity": product["quantity"],

                # "status": product["status"],
                "user_id": product["user_id"],
                "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
            }
            results.append(obj)

        # return results
        return {'sales': results}, 200
        # return sales

# @sale_ns.route("/sales/<int:saleId>")
@sale_ns.param("saleId", "sale identifier")
@sale_ns.response(404, 'Sale not found')
class SaleClass(Resource):

    """Displays a single sale item by sale id for user."""

    # @sale_ns.marshal_with(sales)
    @sale_ns.doc('get one sale')
    @token_required
    @sale_ns.doc(security='apikey')
    @sale_ns.header(
        'token',
        type=str,
        description='access token')
    def get(user_id, self, saleId):
        # def get(self, saleId):
        """Displays a single Sale."""
        # local import
        from src import mongo
        sales = mongo.db.sales
        sale = sales.find_one({'_id': saleId})

        if not sale:
            sale_ns.abort(404, "No sale for user {}".format(user_id))

        if sale["user_id"] != str(user_id):
            sale_ns.abort(401, "Unauthorized to view this sale")

        # return sale
        return jsonify(sale)

    @sale_ns.doc('updates a sale')
    @sale_ns.expect(post_sales)
    @token_required
    @sale_ns.doc(security='apikey')
    @sale_ns.header(
        'token',
        type=str,
        description='access token')
    def put(user_id, self, saleId):
        """Updates a single Sale."""
        args = update_sale_parser.parse_args()

        # local	 import
        from src import mongo
        sales = mongo.db.sales
        sale = sales.find_one({'_id': saleId})

        if not sale:
            return {'warning': 'No sale exists with that id'}, 200

        if sale["user_id"] != str(user_id):
            sale_ns.abort(
                401, "Unauthorized to delete this product")

        invalid_data = validate_update_product(sale, args)
        if invalid_data:
            return invalid_data

        sale_obj = {
            "product_name": args["product_name"],
            "product_category": args["product_category"],
            'updated': datetime.utcnow(),
        }

        # product['product_name'] = args["product_name"],
        # product['product_category'] = args["product_category"],
        # sales.save(sale)
        sales.update_one(sale, {"$set": sale_obj})

        return jsonify(
            {"message": "Sale updated successfully", "sale": sale})
        # return {"message": "Sale updated successfully", "sale": sale}
        # return {"message": "Sale updated successfully"}

    @sale_ns.doc('deletes a sale')
    @sale_ns.response(204, 'Sale Deleted')
    @token_required
    @sale_ns.doc(security='apikey')
    @sale_ns.header(
        'token',
        type=str,
        description='access token')
    def delete(user_id, self, saleId):
        """Deletes a single Sale."""
        # local import
        from src import mongo
        sales = mongo.db.sales
        sale = sales.find_one({'_id': saleId})

        if not sale:
            return {'warning': 'No sale exists with that id'}, 200

        if sale["user_id"] != str(user_id):
            sale_ns.abort(401, "Unauthorized to delete this sale")

        sales.delete_one(sale)

        # return {"message": "Sale deleted successfully"}, 204
        return {"message": "Sale deleted successfully"}, 200

# @sale_ns.route('/sale')


class CreateSale(Resource):

    """Lets you POST to add new sales."""
    # @sale_ns.marshal_with(sales_resp, envelope='sales')
    # @sale_ns.response(200, "product_names", fields.List(fields.String))
    # # @sale_ns.expect(sales_resp)
    # @sale_ns.expect(post_sales)
    @sale_ns.expect(salesr)
    # @sale_ns.doc(security='Auth_token')
    @sale_ns.doc('creates a sale')
    @sale_ns.response(201, "Created")
    @token_required
    @sale_ns.doc(security='apikey')
    @sale_ns.header(
        'token',
        type=str,
        description='access token')
    def post(user_id, self):
        # def post(self):
        """Create Sale Order."""
        args = sale_parser_resp.parse_args()

        print(args["product_names"])

        # validate the sale payload
        # invalid_data = validate_product_data(args)
        # if invalid_data:
        #     return invalid_data

        # local import
        from src import mongo
        sales = mongo.db.sales

        sale_id = sales.insert({
            # 'product_category': args["product_category"],
            # 'product_names': ["product1", "product2", "another1"],
            # 'product_name': args["product_name"],
            'product_names': args["product_names"],
            'products_count': args["products_count"],
            'cart_total': args["cart_total"],

            # 'email': args["email"],
            'user_id': user_id,
            'created': datetime.utcnow(),
            # 'sale_completed': False
        })

        new_sale = sales.find_one({'_id': sale_id})

        message = 'Sale with id ' + \
            str(new_sale['_id']) + ' added successfully'
        return {'message': message}, 201
        # return {"message": "Sale added successfully"}, 201


# @sale_ns.route('/sales/<objectid:user_id>')
class GetSingleCart(Resource):
    # @sale_ns.doc(security='Auth_token')
    @sale_ns.doc(security='apikey')
    # @token_required
    # @sale_ns.marshal_with(sales_resp, envelope='sales')
    @sale_ns.header(
        'token',
        type=str,
        description='access token')
    def get(self, user_id):
        # def get(user_id, self):
        """Gets a single Sale given user ID."""
        print(type(user_id))
        user_id = str(user_id)
        print(type(user_id))

        # local import
        from src import mongo
        sales = mongo.db.sales
        salesx = sales.find({'user_id': user_id})
        # print(salesx)
        if not salesx:
            sale_ns.abort(404, "No sales for user {}".format(user_id))

        results = []
        for product in salesx:
            obj = {
                "sale_id": str(product["_id"]),
                # "product_name": product["product_name"],
                # "product_category": product["product_category"],
                "product_names": product["product_names"],
                "products_count": product["products_count"],
                "cart_total": product["cart_total"],

                # "price": product["price"],
                # "status": product["status"],
                "user_id": product["user_id"],
                "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
            }

            # print(product)
            results.append(obj)

        if not results:
            sale_ns.abort(404, "No sales for user {}".format(user_id))

        return {'sales': results}, 200


# @sale_ns.route('/all-sales')
class AllSales(Resource):
    @sale_ns.response(200, 'Success')
    # @sale_ns.marshal_with(sales_resp, envelope='sales')
    # @sale_ns.doc(security='Auth_token')
    @admin_token_required
    @sale_ns.doc(security='apikey')
    @sale_ns.header(
        'token',
        type=str,
        description='access token')
    def get(user_id, self):
        """Gets all sales from db"""
        # local import
        from src import mongo
        sales = mongo.db.sales
        salesx = sales.find()

        if not salesx:
            sale_ns.abort(404, "No sales for found")

        results = []
        for product in salesx:
            obj = {
                "sale_id": str(product["_id"]),
                # "product_name": product["product_name"],
                # "product_names": product["product_names"],
                "products_count": product["products_count"],
                "cart_total": product["cart_total"],

                # "product_category": product["product_category"],
                # "price": product["price"],
                # "status": product["status"],
                "user_id": product["user_id"],
                "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
            }
            results.append(obj)

        return jsonify(
            {"message": "All sales listed successfully", "sales": results})
