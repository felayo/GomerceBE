""" Defines the Customer repository """
import sys
from sqlalchemy import or_
from models import Seller
from utils import Notification
from repositories.verification_token import VerificationTokenRepository
from utils.errors import DataNotFound, DuplicateData, InternalServerError
from sqlalchemy.exc import IntegrityError


class SellerRepository:
    """ The repository for the seller model """

    @staticmethod
    def get(seller_id=None, username=None, email=None):
        """ Query a seller by seller_id """

        # make sure one of the parameters was passed
        if not seller_id and not username and not email:
            raise DataNotFound(f"Seller not found, no detail provided")

        try:
            query = Seller.query
            if seller_id:
                query = query.filter(Seller.id == seller_id)
            if username:
                query = query.filter(
                    or_(
                        Seller.username == username,
                        Seller.email == username
                    ))
            if email:
                query = query.filter(
                    or_(Seller.email == email, Seller.username == email))

            seller = query.first()
            return seller
        except DataNotFound as e:
            print(sys.exc_info())
            raise DataNotFound(f"Seller with {seller_id} not found")

    @staticmethod
    def getAll():
        """ Query all sellers"""
        sellers = Seller.query.all()
        all_sellers = [seller.json for seller in sellers]

        return all_sellers

    def update(self, seller_id, **args):
        """ Update a seller's details """
        seller = Seller.query.get(seller_id)

        if 'phone' in args and args['phone'] is not None:
            seller.phone = args['phone']

        if 'email' in args and args['email'] is not None:
            seller.email = args['email']

        if 'last_name' in args and args['last_name'] is not None:
            seller.last_name = args['last_name']

        if 'first_name' in args and args['first_name'] is not None:
            seller.first_name = args['first_name']

        if 'rating' in args and args['rating'] is not None:
            seller.rating = args['rating']

        return seller.save()

    @staticmethod
    def create(username, last_name, first_name, password, email,
                phone, rating=0, email_verified=False, 
                phone_verified=False):
        """ Create a new seller """
        error=False
        try:
            new_seller = Seller(username=username, first_name=first_name,
                                last_name=last_name, email=email, phone=phone,
                                rating=rating, email_verified=email_verified, 
                                phone_verified=phone_verified)
            new_seller.set_password(password)

            # # create verification tokens for the email and phone
            # email_token = VerificationTokenRepository.create(user_id=new_seller.id,
            #                                                     user_type="seller", email=True,
            #                                                     phone=False)
            # if not email_token:
            #     error = True

            # if not error:
            #     # create email template for verification token
            #     email_confirm_url = f"http://localhost:2000/confirm_email/{email_token}"
            #     email_notification = Notification(email=True)
            #     email_message = email_notification.create_email_template("user_verification_email.html",
            #                                                                 confirm_url=email_confirm_url,
            #                                                                 new_seller=new_seller)

            #     # send email verification notification
            #     recipient = {
            #         "name": f"{new_seller.first_name} {new_seller.last_name}",
            #         "email": new_seller.email
            #     }
            #     subject = "Customer Email Verification"
            #     Notification.send_email(
            #         message=email_message, to=recipient, subject=subject)

            return new_seller.save()
        except IntegrityError as e:
            error = True 
            message = e.orig.diag.message_detail
            raise DuplicateData(message)
        except Exception:
            error=True
            raise InternalServerError
