"""
Define the resources for the product
"""
from flask import jsonify, abort
from flasgger import swag_from
from flask_restful import Resource
from flask_restful.reqparse import Argument
from repositories import ProductRepository
from utils import parse_params
from utils.errors import DataNotFound


class ProductResource(Resource):
    """ methods relative to the product """

    @staticmethod
    # @swag_from("../swagger/product/get_one.yml")
    def get_one(product_id):
        """ Return a product key information based on product_id """

        try:
            product = ProductRepository.get(product_id=product_id)
            return jsonify({"data": product.json})
        except DataNotFound as e:
            abort(404, e.message)
        except Exception:
            abort(500)

    @staticmethod
    # @swag_from("../swagger/product/get_all.yml")
    def get_all():
        """ Return all products key information based on the query parameter """
        products = ProductRepository.getAll()
        return jsonify({"data": products})

    @staticmethod
    @parse_params(
        Argument("title", location="json", required=True,
                 help="The title of the product."),
        Argument("price", location="json", required=True,
                 help="The price of the product."),
        Argument("quantity", location="json", required=True,
                 help="The quantity of the products."),
        Argument("short_desc", location="json", required=True,
                 help="Short description of the product."),
        Argument("thumbnail", location="json", required=True,
                 help="Thumbnail of the product."),
        Argument("rating", location="json", required=True,
                 help="Rating of the product."),
        Argument("long_desc", location="json", required=True,
                 help="Long description of the product."),
        Argument("image", location="json", required=True,
                 help="Image of the product.")
    )
    @swag_from("../swagger/product/POST.yml")
    def post(title, price, quantity, short_desc, long_desc, image, rating, thumbnail):
        """ Create a product based on the provided information """
        # Check duplicates
        new_product = ProductRepository.create(
            title=title, price=price, quantity=quantity, short_desc=short_desc,
            long_desc=long_desc, image=image, rating=rating, thumbnail=thumbnail
        )
        return jsonify({"data": new_product.json})


    
   
   
