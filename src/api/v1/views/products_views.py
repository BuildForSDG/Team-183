# local imports
from ..utils.pdto import product_parser, update_product_parser, product_parser_resp, update_product_parser_resp
# from ..utils.pdto import product_parser, update_product_parser
# from ..models.product_model import product_ns, products, post_products
# from ..models.product_model import products, product_ns, post_products, product_mod, product_resp, product_update_resp
from ..models.product_model import products, product_ns, post_products, product_update_resp
# from ..utils.decorators import token_required
from ..utils.decorators import token_required, admin_token_required
from ..utils.validators import validate_product_data, validate_update_product


# third-party imports
from flask_restx import Resource
from datetime import datetime
from flask import jsonify


# @product_ns.route("/products")
class ProductList(Resource):

    """Displays a list of all products and lets you POST to add new products."""

    @product_ns.expect(products)
    # @product_ns.expect(post_products)
    # @product_ns.expect(product_update_resp)
    @product_ns.doc('creates a product')
    @product_ns.response(201, "Created")
    @token_required
    @product_ns.doc(security='apikey')
    @product_ns.header(
        'token',
        type=str,
        description='access token')
    def post(user_id, self):
        """Creates a new Product."""
        args = product_parser.parse_args()

        # validate the product payload
        invalid_data = validate_product_data(args)
        if invalid_data:
            return invalid_data

        # local import
        from src import mongo
        products = mongo.db.products

        product_id = products.insert({
            'product_name': args["product_name"],
            'product_category': args["product_category"],
            'user_id': user_id,
            'created': datetime.utcnow(),
            'sale_completed': False
        })

        new_product = products.find_one({'_id': product_id})

        message = 'Product with id ' + \
            str(new_product['_id']) + ' added successfully'
        return {'message': message}, 201
        # return {"message": "Product added successfully"}, 201

    @product_ns.doc("list_products")
    @product_ns.response(404, "Products Not Found")
    # @product_ns.marshal_list_with(products, envelope="products")
    @token_required
    @product_ns.doc(security='apikey')
    @product_ns.header(
        'token',
        type=str,
        description='access token')
    def get(user_id, self):
        """List all Products by user"""
        # print(type(user_id))

        # local import
        from src import mongo
        products = mongo.db.products
        productx = products.find({'user_id': user_id})
        # print(type(productx))
        # print(productx)

        if not productx:
            product_ns.abort(
                404, "No products for user {}".format(user_id))

        results = []
        for product in productx:
            obj = {
                "product_id": str(
                    product["_id"]),
                "product_name": product["product_name"],
                "min_quantity": product["min_quantity"],
                "price": product["price"],
                "inventory": product["inventory"],
                "user_id": product["user_id"],
                "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
            }
            # print(product)
            results.append(obj)

        # return results
        return {'products': results}, 200


# @product_ns.route("/products/<int:productId>")
# @product_ns.param("productId", "product identifier")
@product_ns.response(404, 'Product not found')
class ProductClass(Resource):

    """Displays a single product item."""

    # @product_ns.marshal_with(products)
    @product_ns.doc('get one product')
    @token_required
    @product_ns.doc(security='apikey')
    @product_ns.header(
        'token',
        type=str,
        description='access token')
    def get(user_id, self, product_id):
        # def get(self, user_id, productId):
        """Displays a single Product."""
        # local import
        from src import mongo
        products = mongo.db.products

        product = products.find_one({'_id': product_id})

        if product["user_id"] != str(user_id):
            product_ns.abort(401, "Unauthorized to view this product")

        # return product
        # return jsonify(product)
        return jsonify({"product": product})

    @product_ns.doc('updates a product')
    @product_ns.expect(post_products)
    @admin_token_required
    @product_ns.doc(security='apikey')
    @product_ns.header(
        'token',
        type=str,
        description='access token')
    def put(user_id, self, product_id):
        # print(user_id)
        """Updates a single Product."""
        args = update_product_parser.parse_args()
        # print(args)

        # local	 import
        from src import mongo
        products = mongo.db.products
        product = products.find_one({'_id': product_id})

        if not product:
            return {'warning': 'No product exists with that id'}, 200

        if product["user_id"] != str(user_id):
            product_ns.abort(
                401, "Unauthorized to delete this product")

        invalid_data = validate_update_product(product, args)
        if invalid_data:
            return invalid_data

        product_obj = {
            "product_name": args["product_name"],
            "product_category": args["product_category"],
            'updated': datetime.utcnow(),
        }

        # product['product_name'] = args["product_name"],
        # product['product_category'] = args["product_category"],
        # products.save(product)

        products.update_one(product, {"$set": product_obj})

        return jsonify(
            {"message": "Product updated successfully", "product": product})
        # return {"message": "Product updated successfully", "product": product}
        # return {"message": "Product updated successfully"}

    @product_ns.doc('deletes a product')
    @product_ns.response(204, 'Product Deleted')
    @token_required
    @product_ns.doc(security='apikey')
    @product_ns.header(
        'token',
        type=str,
        description='access token')
    def delete(user_id, self, product_id):
        """Deletes a single Product."""
        # local import
        from src import mongo
        products = mongo.db.products
        product = products.find_one({'_id': product_id})

        if not product:
            return {'warning': 'No product exists with that id'}, 200

        if product["user_id"] != str(user_id):
            product_ns.abort(
                401, "Unauthorized to delete this product")

        products.delete_one(product)

        # return {"message": "Product deleted successfully"}, 204
        return {"message": "Product deleted successfully"}, 200


# @product_ns.route('/all_products')
class Products(Resource):

    @product_ns.expect(product_update_resp)
    @product_ns.doc('adds a product')
    @product_ns.response(201, 'Product created successfully')
    # @product_ns.doc(security='Auth_token')
    # @product_ns.expect(product_mod, validate=True)
    @admin_token_required
    @product_ns.doc(security='apikey')
    @product_ns.header(
        'token',
        type=str,
        description='access token')
    # def post(self, user_id):
    def post(user_id, self):
        """Creates a new Product  (Admin Only)."""
        # data = json.loads(request.data.decode().replace("'", '"'))
        args = product_parser_resp.parse_args()
        # print(args)
        product_name = args['product_name']
        inventory = args['inventory']
        min_quantity = args['min_quantity']
        category = args['category']
        price = args['price']
        # print(user_id)

        # validate the product payload
        # invalid_data = validate_product_data(args)
        # if invalid_data:
        #     return invalid_data

        # local import
        from src import mongo
        products = mongo.db.products

        product_id = products.insert({
            'product_name': product_name,
            'inventory': inventory,
            'category': category,
            'price': price,
            'min_quantity': min_quantity,

            'user_id': user_id,
            'created': datetime.utcnow(),
            # 'sale_completed': False
        })

        # print(product_id)

        # new_product = products.find_one({'_id': product_id})
        # message = 'Product with id ' + \
        #     str(new_product['_id']) + ' added successfully'
        # return {'message': message}, 201

        new_product = dict(
            product_id=str(product_id),
            product_name=product_name.lower(),
            Stock_count=inventory,
            Category=category.lower(),
            Price_per_unit=price,
            Minimum_quantity=min_quantity
        )

        resp = dict(message="Product successfully added.",
                    new_product=new_product
                    )

        return resp, 201

    @product_ns.response(200, 'Success')
    # @product_ns.doc(security='Auth_token')
    # @token_required
    # @product_ns.marshal_list_with(product_resp, envelope='products')
    @token_required
    @product_ns.doc(security='apikey')
    @product_ns.header(
        'token',
        type=str,
        description='access token')
    def get(self, user_id):
        """"Gets all products from db"""
        # products = Product().get_all()
        # return products

        # local import
        from src import mongo
        products = mongo.db.products
        productsx = products.find()

        if not productsx:
            product_ns.abort(404, "No products for found")

        results = []
        for product in productsx:
            obj = {
                "product_id": str(product["_id"]),
                "product_name": product["product_name"],
                "min_quantity": product["min_quantity"],
                "price": product["price"],
                "inventory": product["inventory"],
                # "product_names": product["product_names"],
                # "products_count": product["products_count"],
                # "cart_total": product["cart_total"],

                # "product_category": product["category"],
                # "price": product["price"],
                # "status": product["status"],
                "user_id": product["user_id"],
                "date_ordered": product["created"].strftime('%d-%b-%Y : %H:%M:%S'),
            }
            results.append(obj)

        return jsonify(
            {"message": "All products listed successfully", "products": results})

# @product_ns.route('/<int:product_id>')'
@product_ns.param("product_id", "product identifier")
@product_ns.response(404, 'Product not found')
class OneProduct(Resource):

    """Displays a single product item by user."""

    # @product_ns.doc(security='Auth_token')
    # @token_required
    # @product_ns.marshal_with(product_resp, envelope='product')
    @product_ns.doc('get single product')
    @token_required
    @product_ns.doc(security='apikey')
    @product_ns.header(
        'token',
        type=str,
        description='access token')
    def get(user_id, self, product_id):
        # def get(self, user_id, product_id):
        """Gets a single  product given a product ID"""
        # local import
        from src import mongo
        products = mongo.db.products

        product = products.find_one({'_id': product_id})

        if not product:
            return {'warning': 'No product exists with that id'}, 200

        # print(product['user_id'])
        # print(user_id)

        if product["user_id"] != str(user_id):
            product_ns.abort(401, "Unauthorized to view this product")

        # return product
        return jsonify(product)

    @product_ns.expect(product_update_resp)
    # @product_ns.expect(product_mod)
    # @product_ns.doc(security='Auth_token')
    @product_ns.doc('admin updates a product')
    # @product_ns.expect(post_products)
    # @product_ns.expect(product_update_resp, validate=False)
    # @product_ns.marshal_with(product_resp)
    # @token_required
    @admin_token_required
    @product_ns.doc(security='apikey')
    @product_ns.header(
        'token',
        type=str,
        description='access token')
    def put(user_id, self, product_id):
        # def put(self, user_id, product_id):
        """Updates product details"""
        # product = Product()
        # existing_prd = Product().get_single_product(product_id)
        # data = json.loads(request.data.decode().replace("'", '"'))

        args = update_product_parser_resp.parse_args()
        # print(args)

        # inventory = existing_prd[0]['inventory']
        # if 'inventory' in args:
        #     inventory = args['inventory']
        # min_quantity = existing_prd[0]['min_quantity']
        # if 'min_quantity' in args:
        #     min_quantity = args['min_quantity']
        # price = existing_prd[0]['price']
        # if 'price' in args:
        #     price = args['price']

        # updated_product = product.update_product(
        #     inventory, min_quantity, price, product_id)

        # return updated_product

        # local	 import
        from src import mongo
        products = mongo.db.products
        product = products.find_one({'_id': product_id})

        if not product:
            return {'warning': 'No product exists with that id'}, 200

        if product["user_id"] != str(user_id):
            product_ns.abort(
                401, "Unauthorized to delete this product")

        # invalid_data = validate_update_product(product, args)
        # if invalid_data:
        #     return invalid_data

        product_obj = {
            "min_quantity": args["min_quantity"],
            "inventory": args["inventory"],
            "price": args["price"],
            'updated': datetime.utcnow(),
        }

        products.update_one(product, {"$set": product_obj})

        return jsonify(
            {"message": "Product updated successfully", "product": product})
