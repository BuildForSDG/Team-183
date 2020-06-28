from flask_restx import Namespace, fields


cart_ns = Namespace(
    'Carts',
    description='Cart related Operations',
    path="/api/v1"
    )

cart_model = cart_ns.model('Details required to create Cart order', {
    'quantity': fields.Integer(description='Number of products sold', example=10),
    'price': fields.Integer(description='Total Price of products', example=1000),
    'product_name': fields.String(description='products Name', example='Layer H3N'),
    # 'product_id': fields.String(description='products ID'),
    # 'created_at': fields.DateTime(dt_format='rfc822', description='Date Cart was posted'),
})

carts_resp = cart_ns.model('Expected response for finding by id', {
    'product_name': fields.String(description='products Name'),
    'quantity': fields.Integer(description='Number of products sold'),
    'price': fields.Integer(description='Total Price of products'),
    'created_at': fields.DateTime(dt_format='rfc822', description='Date Cart was posted'),
    'email': fields.String(description='Uniquely Identifies Cart')
})
