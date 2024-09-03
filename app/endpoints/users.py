#######################################################################
##################  IMPORTING LIBRARIES   ##############################
from app.utils import *
from flask_restful import Resource, reqparse


#----------------------USER ENDPOINTS (SIGNIN, LOGIN & LOGOUT) ------
#-----------------------------------------------------------
#api to sign in a user
class SigninUser(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('email', 
                    type=str, required=True,
                    help="Enter Seller email. field can be left blank")
    parser.add_argument('wallet_address', 
                    type=str,required=True,
                    help="Enter wallet address. field cannot be left blank")
    
    
    def post(self):
        try:
            data = SigninUser.parser.parse_args()
            email = data.get("email")
            wallet_address = data.get("wallet_address")
            if not is_valid_email(email):
                return {"status": False, "responseMessage": "Invalid email", "responseData":"", "responseCode":"01", "statusCode": 400}, 400

            if len(wallet_address)==0:
                 return {"status": False, "responseMessage": " Invalid wallet address", "responseData":"", "responseCode":"01", "statusCode": 400}, 400

            get_user = users.find_one({"email":email, "wallet_address": wallet_address}, {"_id":0})
            if not get_user:
                
                user = {
                    "email": email,
                    "wallet_address": wallet_address,
                    "create_at":stamp()
                    }
                #Post details to database
                users.insert_one(user)
                user = users.find_one({"wallet_address":wallet_address}, {"_id":0})

                #creating jwt
                access_token = create_access_token(identity=user.get("wallet_address"), fresh=True)
                refresh_token = create_refresh_token(identity=user.get("wallet_address"))
                return {"status": True, "responseMessage": "Sign in successful!",  "accessToken":access_token, "refreshToken":refresh_token, "responseData":{}, "responseCode":"00", "statusCode": 200}, 200
            else:
                access_token = create_access_token(identity=get_user.get("wallet_address"), fresh=True)
                refresh_token = create_refresh_token(identity=get_user.get("wallet_address"))
                return {"status": True, "responseMessage": "Sign in successful!",  "accessToken":access_token, "refreshToken":refresh_token, "responseData":{}, "responseCode":"00", "statusCode": 200}, 200


        except Exception as e:
            return {"responseMessage":f"An exception occurred: {e}", "status":False, "responseData":"", "responseCode":"01", "statusCode": 422}, 422
api.add_resource(SigninUser, '/api/v1/ecommerce/user/signin')

#api to login a Seller
# class LoginUser(Resource):
#     parser = reqparse.RequestParser()

#     parser.add_argument('email', 
#                     type=str, required=True,
#                     help="Enter Seller email. field can be left blank")
#     parser.add_argument('wallet_address', 
#                     type=str,required=True,
#                     help="Enter wallet address. field cannot be left blank")
    
#     def post(self):
#         try:
#             data = LoginUser.parser.parse_args()
#             email = data.get("email")
#             wallet_address = data.get("wallet_address")
#             if not is_valid_email(email):
#                 return {"status": False, "responseMessage": "Invalid email", "responseData":"", "responseCode":"01", "statusCode": 400}, 400
    

#             get_user = users.find_one({"email":email}, {"_id":0})
#             if not get_user:
#                 return {"status": False, "responseMessage": "Phone number or password incorrect", "responseData":"", "responseCode":"01", "statusCode": 401}, 401
            
#             if wallet_address ==  get_user.get("wallet_address"):
#                 user_details= {
#                     "email": get_user.get("email"),
#                     "wallet_address": get_user.get("wallet_address") 
#                     }
#                 #creating jwt
#                 access_token = create_access_token(identity=get_user.get("email"), fresh=True)
#                 refresh_token = create_refresh_token(identity=get_user.get("email"))
#                 return {"status": True, "responseMessage": "Login successful!", "responseData": user_details, "accessToken":access_token, "refreshToken":refresh_token, "responseCode":"00", "statusCode": 200}, 200
#             else:
#                 return {"status": False, "responseMessage": "Invalid Credentials", "responseData":"", "responseCode":"01","statusCode": 401}, 401
#         except Exception as e:
#             return {"responseMessage":f"An exception occurred: {e}", "status":False, "responseData":"", "responseCode":"01", "statusCode": 422}, 422
# api.add_resource(LoginUser, '/api/v1/ecommerce/user/login')

class LogoutUser(Resource):

    @jwt_required()
    def post(self):
        try:
            auth = request.headers.get('Authorization').split()[1]
            jti = get_jti(auth)
            jwt_blacklist.insert_one({"jti": jti})
            return {"status": True, "responseMessage": "Logout successful!", "responseData":{}, "responseCode":"00", "statusCode": 200}, 200
        except Exception as e:
            return {"responseMessage":f"An exception occurred: {e}", "status":False, "responseData":"", "responseCode":"01", "statusCode": 422}, 422
api.add_resource(LogoutUser, '/api/v1/ecommerce/user/logout')
