from flask_restx import Namespace, fields

sale_ns = Namespace(
    "Sales",
    description="Sales related operations",
    # # path="/sales",
    # path="/api/v1/sales"
    path="/api/v1"
)


products_array = fields.String(description='Products Array')

salesr = sale_ns.model("sales", {
    # "product_names": fields.List(fields.String, description="The product productnames", example=["product1", "product2", "another1"]),
    'products_count': fields.Integer(description='Number of products sold', example=10),
    'cart_total': fields.Integer(description='Total Price of products'),
    # "user_id": fields.String(required=False, description="The product user_id"),
    # "created_at": fields.String(required=False, description="The product creation date"),
    # "product_name": fields.String(required=True, description="The product product_name"),
    # 'products_count': fields.Integer(description='Number of products sold'),
    # 'product_names': product_names,
    # 'product_names': fields.List(fields.String, example=["product1", "product2", "another1"]),
    'product_names': fields.List(products_array, action='append', required=True, description="The product product names", example=["product1", "product2", "another1"]),
    # 'product_names': fields.List(products_array, action='split', example="apple,lemon,cherry"),

})

sales_resp = sale_ns.model('Expected response for finding by id', {
    "product_names": fields.List(fields.String, description="The product product_name", example=["product1", "product2", "another1"]),
    'products_count': fields.Integer(description='Number of products sold', example=10),
    'cart_total': fields.Integer(description='Total Price of products', example=1),
    "user_id": fields.String(description="The product user_id - uniquely Identifies Cart creator"),
    'created_at': fields.DateTime(dt_format='rfc822', description='Date Cart was posted'),
    # "id": fields.String(readonly=False),
    # 'product_names': fields.List(),
    # 'email': fields.String(description='Uniquely Identifies Cart creator'),

})

post_sales = sale_ns.model("post_sales",
                           {"product_name": fields.String(required=True,
                                                          description="sales product_name",
                                                          example='This is my first product.'),
                            "product_category": fields.String(required=True,
                                                              description="sales product_category",
                                                              example='This is my first category.')})
