from flask_restx import reqparse

category_parser = reqparse.RequestParser()
category_parser.add_argument('product_category', required=True, type=str, help='product_category should be a string')
# category_parser.add_argument('product_name', required=True, type=str, help='product_name should be a string')

update_category_parser = reqparse.RequestParser()
update_category_parser.add_argument('product_category', required=True, type=str, help='product_category should be a string')
# update_category_parser.add_argument('product_name', required=True, type=str, help='product_name should be a string')
