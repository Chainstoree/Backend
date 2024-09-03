from app.utils import *
from flask_restful import Resource, reqparse

#api route for searching products
class SearchAProduct(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('search_term', 
                    type=str,
                    required=True, 
                    help="Enter Search term. field cannot be left blank")
    
    #@token_required
    def post(self):
        try:

            data = SearchAProduct.parser.parse_args()
            search_term = data.get("search_term").lower().strip()
            
        
            # Perform the search
            results = list(products.find({"$text": {"$search": f"{search_term}"}},{"_id":0}))

            if len(results)==0:
                return {"status": False, "responseMessage": "No record found for the search", "responseData":"", "responseCode":"01", "statusCode": 404}, 404

            else:
                return {"status": True, "responseMessage": "Search result retrieved successfully.", "Count":len(results), "responseData":results, "responseCode":"00", "statusCode": 200}, 200
        except Exception as e:
            return {"responseMessage":f"An exception occurred: {e}", "status":False, "responseData":{}, "responseCode":"01", "statusCode": 422}, 422
api.add_resource(SearchAProduct, '/api/v1/ecommerce/product/search')

#api route for retrieving Popular Products
class GetAllProducts(Resource):
    #@token_required
    def get(self):
        try:
            
            all_product = list(products.find({},{"_id":0}))
            
            if all_product == []:
                return {"status": False, "responseMessage": "No records yet", "responseData":{}, "responseCode":"01", "statusCode": 404}, 404
            else:
                return {"status": True, "responseMessage": f"All products retrieved successfully.", "Count":len(all_product), "responseData":all_product, "responseCode":"00", "statusCode": 200}, 200
        except Exception as e:
            return {"responseMessage":f"An exception occurred: {e}", "status":False, "responseData":{}, "responseCode":"01", "statusCode": 422}, 422
api.add_resource(GetAllProducts, '/api/v1/ecommerce/product/popular')

#api route for retrieving a Product details using product_name
class GetAProductsDetails(Resource):
    #@token_required
    def get(self, product_name):
        try:
            
            product = products.find_one({"product_name":product_name},{"_id":0})
            if not product:
                return {"status": False, "responseMessage": f"No record for product {product_name}", "responseData":{}, "responseCode":"01", "statusCode": 404}, 404
            else:
                return {"status": True, "responseMessage": f"Details for product with Id {product_name} retrieved successfully.", "responseData":product, "responseCode":"00", "statusCode": 200}, 200
        except Exception as e:
            return {"message":f"An exception occurred: {e}", "status":False}, 422
api.add_resource(GetAProductsDetails, '/api/v1/ecommerce/product/detail/<string:product_name>')