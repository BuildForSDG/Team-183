from flask_restx import reqparse

product_parser = reqparse.RequestParser()
product_parser.add_argument('product_name', required=True, type=str, help='product_name should be a string')
product_parser.add_argument('product_category', required=True, type=str, help='product_category should be a string')

update_product_parser = reqparse.RequestParser()
update_product_parser.add_argument('product_name', required=True, type=str, help='product_name should be a string')
update_product_parser.add_argument('product_category', required=True, type=str, help='product_category should be a string')

product_parser_resp = reqparse.RequestParser()
product_parser_resp.add_argument('product_name', required=True, type=str, help='product_name should be a string')
product_parser_resp.add_argument('inventory', required=True, type=str, help='product_category should be a string')
product_parser_resp.add_argument('min_quantity', required=True, type=str, help='product_name should be a string')
product_parser_resp.add_argument('category', required=True, type=str, help='product_category should be a string')
product_parser_resp.add_argument('price', required=True, type=str, help='product_name should be a string')
# product_parser_resp.add_argument('product_category', required=True, type=str, help='product_category should be a string')

update_product_parser_resp = reqparse.RequestParser()
# update_product_parser_resp.add_argument('product_name', required=True, type=str, help='product_name should be a string')
update_product_parser_resp.add_argument('inventory', required=True, type=int, help='product_category should be a number')
update_product_parser_resp.add_argument('min_quantity', required=True, type=int, help='product_name should be a number')
# update_product_parser_resp.add_argument('category', required=True, type=str, help='product_category should be a string')
update_product_parser_resp.add_argument('price', required=True, type=int, help='product_name should be a number')
