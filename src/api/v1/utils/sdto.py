from flask_restx import reqparse

sale_parser = reqparse.RequestParser()
sale_parser.add_argument('product_names', required=True, type=list, help='product_names should be a list of strings')
sale_parser.add_argument('products_count', required=True, type=int, help='product_count should be a number')
sale_parser.add_argument('cart_total', required=True, type=int, help='cart_total should number')


sale_parser_resp = reqparse.RequestParser()
sale_parser_resp.add_argument('product_names', '--nargs', required=True, type=list, help='product_name products_count should be a list of strings')
sale_parser_resp.add_argument('products_count', required=True, type=int, help='product_count should be a number')
sale_parser_resp.add_argument('cart_total', required=True, type=int, help='cart_total should be a number')


update_sale_parser = reqparse.RequestParser()
update_sale_parser.add_argument('product_name', required=True, type=str, help='product_name should be a string')
update_sale_parser.add_argument('product_category', required=True, type=str, help='product_category should be a string')
