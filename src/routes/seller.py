
SELLER_BLUEPRINT.route(
    "/sellers", methods=['GET'])(SellerResource.get_all)
SELLER_BLUEPRINT.route("/sellers", methods=['POST'])(SellerResource.post)
SELLER_BLUEPRINT.route("/sellers/<int:seller_id>",
                        methods=['GET'])(SellerResource.get_one)
SELLER_BLUEPRINT.route("sellers/<int:seller_id>",
                        methods=["DELETE"])(SellerResource.delete)