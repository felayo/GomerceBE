""" Defines the Product repository """
import sys
from flask import jsonify, abort
from sqlalchemy import or_
from models import Product, ProductCategory, Seller
from utils.auth_decorators import requires_role
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError


class ProductRepository:
    """ The repository for the product model """

    @staticmethod
    def get(product_id=None):
        """ Query a product by product_id """

        # make sure one of the parameters was passed
        if not product_id:
            raise DataNotFound(f"Product not found, no detail provided")

        try:
            query = Product.query
            if product_id:
                query = query.filter(Product.id == product_id)

            product = query.first()
            return product
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Product with {product_id} not found")

    @staticmethod
    def getAll():
        """ Query all products"""
        products = Product.query.all()
        return  [product.json for product in products]

    @staticmethod
    @requires_role('seller')
    def create(title, price, quantity, short_desc, long_desc=None, image=None,
        thumbnail=None, rating=None
    ):
        """Create new product"""
        try:
            product = Product(title=title, price=price, quantity=quantity,
                                  short_desc=short_desc, long_desc=long_desc,
                                  image=image, thumbnail=thumbnail, rating=rating
            )
            product.save()
        except IntegrityError as e:
            Product.rollback()
            message = e.orig.diag.message_detail
            print(message)
            raise DuplicateData(message)
        except Exception as e:
            Product.rollback()
            raise DataNotFound(e)

        return jsonify({
            "Product" : product.title,
            "Quantity" : product.quantity,
            "Description" : product.short_desc
        })
