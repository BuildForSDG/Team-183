# local imports
from ..utils.cdto import category_parser
# from ..utils.cdto import category_parser, update_category_parser
from ..models.categories_model import category_model, category_ns
# category_ns = category_ns
# category_model = category_model
# from ..models.category import Category
# from ..utils.validators import validate_product_data, validate_update_product
# from ..utils.decorators import token_required, admin_token_required
# from ..utils.validators import validate_product_data
from ..utils.decorators import admin_token_required

# third-party imports
from flask_restx import Resource
from datetime import datetime
from flask import jsonify
# from werkzeug.exceptions import NotFound, BadRequest
# import json


# @category_ns.route('/category')
class CreateCategory(Resource):
    @category_ns.expect(category_model)
    # @category_ns.doc(security='Auth_token')
    # @category_ns.expect(category_model, validate=True)
    @admin_token_required
    @category_ns.doc(security='apikey')
    @category_ns.header(
        'token',
        type=str,
        description='access token')
    def post(user_id, self):
        """Creates a new category."""
        # data = json.loads(request.data.decode().replace("'", '"'))
        # category_name = data['category_name']
        # new_category = Category()
        # return new_category.add_category(category_name)
        args = category_parser.parse_args()

        # # validate the category payload
        # invalid_data = validate_product_data(args)
        # if invalid_data:
        #     return invalid_data

        # local import
        from src import mongo
        categories = mongo.db.categories

        category_id = categories.insert({
            'product_category': args["product_category"],
            # 'product_name': args["product_name"],
            # 'products_count': args["products_count"],
            # 'cart_total': args["cart_total"],

            # 'email': args["email"],
            'user_id': user_id,
            'created': datetime.utcnow(),
            # 'category_completed': False
        })

        new_category = categories.find_one({'_id': category_id})

        message = 'category with id ' + \
            str(new_category['_id']) + ' added successfully'
        return {'message': message}, 201

    @category_ns.response(200, 'Success')
    # @category_ns.doc(security='Auth_token')
    @category_ns.expect(category_model)
    # @category_ns.marshal_list_with(category_model, envelope='categories')
    @admin_token_required
    @category_ns.doc(security='apikey')
    @category_ns.header(
        'token',
        type=str,
        description='access token')
    def get(user_id, self):
    # def get(self):
        """"Gets all categories from db."""
        # categories = Category().get_all()

        # return categories

        # local import
        from src import mongo
        categories = mongo.db.categories
        categoriesx = categories.find()

        if not categoriesx:
            category_ns.abort(404, "No categories for found")

        results = []
        for product in categoriesx:
            obj = {
                "category_id": str(product["_id"]),
                "product_category": product["product_category"],
                # "product_name": product["product_name"],
                # "product_names": product["product_names"],
                # "products_count": product["products_count"],
                # "cart_total": product["cart_total"],

                # "product_category": product["product_category"],
                # "price": product["price"],
                # "status": product["status"],
                "user_id": product["user_id"],
                "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
            }
            results.append(obj)

        return jsonify(
            {"message": "All categories listed successfully", "categories": results})
