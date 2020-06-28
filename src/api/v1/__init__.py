"""Application versioning."""
# local imports
from .views.users_views import (
    auth_ns,
    RegisterUser,
    LoginUser,
    UserForgotPassword,
    UserResetPassword,
    LoggedInUserProfile,
    AllUsers
)

from .views.products_views import (
    product_ns,
    ProductList,
    ProductClass,
    Products,
    OneProduct
)

from .views.sales_views import (
    sale_ns,
    SaleList,
    SaleClass,
    AllSales,
    CreateSale,
    GetSingleCart
)


from .views.carts_views import (
    cart_ns,
    AllCarts,
    GetSingleCart1,
    PostCart
)


from .views.categories_views import (
    category_ns,
    CreateCategory
)


# third-party imports
from flask_restx import Api
from flask import Blueprint


api_v1_blueprint = Blueprint(
    'api',
    __name__,
    # url_prefix='/api/v1',
)

authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "token"
    }
}

api = Api(
    api_v1_blueprint,
    version='1.0',
    title='team-183 API',
    authorizations=authorizations,
    description='A team-183 API',
    doc='/'
)


# del auth_api.namespaces[0]
api.add_namespace(auth_ns)
api.add_namespace(product_ns)
api.add_namespace(sale_ns)
api.add_namespace(cart_ns)
api.add_namespace(category_ns)


auth_ns.add_resource(RegisterUser, '/signup', endpoint='signup')
auth_ns.add_resource(LoginUser, '/login', endpoint='login')
auth_ns.add_resource(UserForgotPassword, '/forgot-password', endpoint='forgot-password')
auth_ns.add_resource(UserResetPassword, '/reset-password', endpoint='reset-password')
auth_ns.add_resource(LoggedInUserProfile, '/profile', endpoint='profile')
auth_ns.add_resource(AllUsers, '', endpoint='all_users')


product_ns.add_resource(ProductList, '/products', endpoint='products')
# product_ns.add_resource(ProductClass, '/products/<objectid:productId>', endpoint='product')
product_ns.add_resource(ProductClass, '/products/<objectid:product_id>', endpoint='product')
# product_ns.add_resource(ProductClasproduct_ns.add_resource(ProductList, '/products', endpoint='products')
product_ns.add_resource(Products, '/new_products', endpoint='all_products')
product_ns.add_resource(OneProduct, '/one_product/<objectid:product_id>', endpoint='one_product')


sale_ns.add_resource(SaleList, '/sales', endpoint='sales')
sale_ns.add_resource(SaleClass, '/sales/<objectid:saleId>', endpoint='sale')
# sale_ns.add_resource(SaleClass, '/sales/<int:saleId>', endpoint='sale')
sale_ns.add_resource(AllSales, '/all_sales', endpoint='all_sales')
sale_ns.add_resource(CreateSale, '/create_sale', endpoint='create_sale')
sale_ns.add_resource(GetSingleCart, '/get_sale/<objectid:user_id>', endpoint='get_sale')


cart_ns.add_resource(AllCarts, '/all_carts', endpoint='all_carts')
cart_ns.add_resource(PostCart, '/create_cart/<objectid:product_id>', endpoint='create_cart')
# cart_ns.add_resource(GetSingleCart1, '/get_cart/<objectid:user_id>', endpoint='get_cart')
cart_ns.add_resource(GetSingleCart1, '/get_cart', endpoint='get_cart')


category_ns.add_resource(CreateCategory, '/category', endpoint='create_category')
