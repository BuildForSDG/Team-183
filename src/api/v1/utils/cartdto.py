from flask_restx import reqparse

cart_parser = reqparse.RequestParser()
cart_parser.add_argument('quantity', required=True, type=int, help='quantity should be a number')
cart_parser.add_argument('price', required=False, type=int, help='price should be a number')
cart_parser.add_argument('product_name', required=False, type=str, help='product_name should be a string')
cart_parser.add_argument('product_id', required=False, type=str, help='product_id should be a string')
# cart_parser.add_argument('user_id', required=False, type=str, help='user_id should be a string')
# cart_parser.add_argument('cart_id', required=False, type=str, help='cart_id should be a string')
# cart_parser.add_argument('created', required=False, type=str, help='created should be a string')
# cart_parser.add_argument('products_count', required=True, type=int, help='product_category should be a number')
# cart_parser.add_argument('cart_total', required=True, type=int, help='cart_total should number')

# cart_parser_resp.add_argument('user_id', required=True, type=str, help='product_name should be a string')
# cart_parser_resp.add_argument('created', required=True, type=str, help='product_category should be a string')


# cart_parser_resp = reqparse.RequestParser()
# cart_parser_resp.add_argument('product_name', required=True, type=str, help='product_name products_countshould be a string')
# cart_parser_resp.add_argument('products_count', required=True, type=int, help='product_category should be a number')
# cart_parser_resp.add_argument('cart_total', required=True, type=int, help='cart_total should be a number')
# # cart_parser_resp.add_argument('user_id', required=True, type=str, help='product_name should be a string')
# # cart_parser_resp.add_argument('created', required=True, type=str, help='product_category should be a string')

update_cart_parser = reqparse.RequestParser()
update_cart_parser.add_argument('product_name', required=True, type=str, help='product_name should be a string')
update_cart_parser.add_argument('product_category', required=True, type=str, help='product_category should be a string')
