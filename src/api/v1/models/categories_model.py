from flask_restx import Namespace, fields

category_ns = Namespace(
    'Categories',
    description='Category related Operations',
    path="/api/v1"
    )

category_model = category_ns.model('Details required to create a category', {
    'product_category': fields.String(required=True, description='Name of the Category', example='Raw Chicken')
})
