from app.utils import *

@app.route("/api/v1/ecommerce/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return {"status": True, "responseMessage": "Token refreshed successfully!", "responseData":{}, "accessToken":access_token,"statusCode": 200}, 200