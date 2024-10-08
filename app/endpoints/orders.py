from app.utils import *
from flask_restful import Resource, reqparse
from random import randint

#api route for checkout
class Checkout(Resource):
    parser = reqparse.RequestParser()

    
    parser.add_argument('wallet_address', 
                    type=str,required=True,
                    help="Enter wallet address. field cannot be left blank")
    parser.add_argument('product_id', 
                    type=str, required=True,
                    help="Enter product_id. field can be left blank")
    parser.add_argument('total_price', 
                    type=str, required=True,
                    help="Enter total price of products. field can be left blank")
    parser.add_argument('quantity', 
                    type=str, required=True,
                    help="Enter  quantity of product. field can be left blank")
    
    
    #@token_required
    #@jwt_required
    def post(self):
        try:
            data = Checkout.parser.parse_args()
            wallet_address = data.get("wallet_address")
            product_id = data.get("product_id")

            if len(wallet_address)==0:
                 return {"status": False, "responseMessage": " Invalid wallet address", "responseData":"", "responseCode":"01", "statusCode": 400}, 400

            
            product_details = products.find_one({"product_id":product_id}, {"_id":0})

            if product_details:   
                order_id =  str(randint(10000, 99999))
                order = {
                    "order_id": order_id,
                    "wallet_address": wallet_address,
                    "product_details": product_details,
                    "quantity": data.get("quantity"),
                    "total_price": data.get("total_price"),
                    "create_at":stamp()
                    }
                #Post details to database
                orders.insert_one(order)
                #order = orders.find_one({"order_id":order_id}, {"_id":0})
                return {"status": True, "responseMessage": "Checkout successful", "responseData":order, "responseCode":"00", "statusCode": 200}, 200
            else:
                
                return {"status": False, "responseMessage": f"No product found with id {product_id}", "responseData":{}, "responseCode":"01", "statusCode": 404}, 404


        except Exception as e:
            return {"responseMessage":f"An exception occurred: {e}", "status":False, "responseData":"", "responseCode":"01", "statusCode": 422}, 422
api.add_resource(Checkout, '/api/v1/ecommerce/order/checkout')


class GetOrders(Resource):
    #@token_required
    #@jwt_required
    def get(self, wallet_address):
        try:
            
            all_orders = list(orders.find({"wallet_address": wallet_address},{"_id":0}))
            
            if all_orders == []:
                return {"status": False, "responseMessage": "No orders yet", "responseData":{}, "responseCode":"01", "statusCode": 404}, 404
            else:
                return {"status": True, "responseMessage": f"All orders retrieved successfully.", "Count":len(all_orders), "responseData":all_orders, "responseCode":"00", "statusCode": 200}, 200
        except Exception as e:
            return {"responseMessage":f"An exception occurred: {e}", "status":False, "responseData":{}, "responseCode":"01", "statusCode": 422}, 422
api.add_resource(GetOrders, '/api/v1/ecommerce/order/get/<string:wallet_address>')
