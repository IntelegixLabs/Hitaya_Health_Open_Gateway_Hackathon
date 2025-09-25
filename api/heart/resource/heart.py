from bson import ObjectId
from flask import Blueprint
from flask import request, abort, Response

import APP_Constants as AC
from api.utility import document_filter, response, Message
from modules.dbconnect.models.heart import HeartModel

heart_blp = Blueprint(
    'heart_blueprint', __name__, url_prefix=f"{AC.APP_ENDPOINT}/disease"
)


@heart_blp.route('/heart', methods=["GET"])
@response(HeartModel)
def heart_list_api():
    """Heart disease GET endpoint

        Returns:
            [JSON]: [disease Model result JSON]
    """
    from app import db
    return document_filter(db.heart)


@heart_blp.route('/heart/<user_id>', methods=["PATCH", "DELETE"])
@response(HeartModel)
def heart_api(user_id):
    """Heart disease PATCH DELETE endpoint

        Returns:
            [JSON]: [disease Model result JSON]
    """
    from app import db
    kwargs = {"user_id": ObjectId(user_id)}

    payload = request.get_json()
    _id = payload.get("id")
    if payload and _id:
        kwargs["_id"] = ObjectId(_id)
        del payload["id"]

    if not db.heart.find_one(kwargs):
        return Response(Message.NotFound)

    if request.method == "PATCH":
        if not payload:
            abort(400)
        db.heart.update_many(kwargs, {"$set": payload})
        return db.heart.find_many(kwargs)
    if request.method == "DELETE":
        db.heart.delete_many(kwargs)
        return Response(Message.Success)
