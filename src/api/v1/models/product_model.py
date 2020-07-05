from flask_restx import Namespace, fields

product_ns = Namespace(
    "Products",
    description="Products related operations",
    # # path="/products",
    # path="/api/v1/products"
    path="/api/v1"
)


products = product_ns.model("products", {
    "id": fields.Integer(readonly=True),
    "product_name": fields.String(required=True, description="The product product_name", example='Layer H3n'),
    "product_category": fields.String(required=True, description="The product product_category", example='Raw Chicken'),
    "user_id": fields.String(required=True, description="The product user_id"),
    "created_at": fields.String(required=True, description="The product creation date")
})

post_products = product_ns.model(
    "post_products",
    {
        "product_name": fields.String(
            required=True,
            description="products product_name",
            example='This is my first product.'),
        "product_category": fields.String(
            required=True,
            description="products product_category",
            example='This is my first category.')})


product_mod = product_ns.model('product model', {
    # 'product_name': fields.String(required=True, description='products Name', example='Layer H3n'),
    'inventory': fields.Integer(required=True, description='Products inventory', example=4),
    'min_quantity': fields.Integer(required=True, description='Minimum Inventory Quantity Allowed', example=0),
    'category': fields.String(required=True, description='Category of product', example='Raw Chicken'),
    'price': fields.Integer(required=True, description='Price of each product', example=1000),
})

product_update_resp = product_ns.model('product model', {
    'product_name': fields.String(required=True, description='products Name', example='Layer H3n'),
    'inventory': fields.Integer(required=True, description='Products inventory', example=4),
    'min_quantity': fields.Integer(required=True, description='Minimum Inventory Quantity Allowed', example=0),
    'category': fields.String(required=True, description='Category of product', example='Raw Chicken'),
    'price': fields.Integer(required=True, description='Price of each product', example=1000),
})

product_resp = product_ns.model('Expected response for finding by id', {
    'product_name': fields.String(required=True, description='products Name', example='Layer H3n'),
    'inventory': fields.Integer(required=True, description='Products inventory', example=4),
    'min_quantity': fields.Integer(required=True, description='Minimum Inventory Quantity Allowed', example=0),
    'category': fields.String(required=True, description='Category of product', example='Raw Chicken'),
    'price': fields.Integer(required=True, description='Price of each product', example=1000),
    # 'product_id': fields.Integer(description='Unique Identification for products'),
    # 'date_created': fields.DateTime(dt_format='rfc822', description='Date product was created'),
    # 'date_modified': fields.DateTime(dt_format='rfc822', description='Date product was modified'),

})

# product_update_resp = product_ns.model('Expected response for finding by id', {
#     'inventory': fields.Integer(required=True, description='Products inventory', example=4),
#     'min_quantity': fields.Integer(required=True, description='Minimum Inventory Quantity Allowed', example=0),
#     'category': fields.String(required=True, description='Category of product', example='Raw Chicken'),
#     'price': fields.Integer(required=True, description='Price of each product', example=1000),
#     # 'date_modified': fields.DateTime(dt_format='rfc822', description='Date product was modified'),

# })
