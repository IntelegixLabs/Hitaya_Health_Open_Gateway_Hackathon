from bson import ObjectId
from flask import Blueprint
from flask import request, abort, Response

import APP_Constants as AC
from api.utility import document_filter, response, Message
from modules.dbconnect.models.diabetics import DiabeticModel

diabetic_blp = Blueprint(
    'diabetic_blueprint', __name__, url_prefix=f"{AC.APP_ENDPOINT}/disease"
)


@diabetic_blp.route('/diabetic', methods=["GET"])
@response(DiabeticModel)
def diabetics_list_api():
    """Diabetics disease GET endpoint

        Returns:
            [JSON]: [disease Model result JSON]
    """
    from app import db
    return document_filter(db.diabetes)


@diabetic_blp.route('/diabetic/<user_id>', methods=["PATCH", "DELETE"])
@response(DiabeticModel)
def diabetic_api(user_id):
    """Diabetic disease PATCH DELETE endpoint

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

    if not db.diabetes.find_one(kwargs):
        return Response(Message.NotFound)

    if request.method == "PATCH":
        if not payload:
            abort(400)
        db.diabetes.update_many(kwargs, {"$set": payload})
        return db.diabetes.find_many(kwargs)
    if request.method == "DELETE":
        db.diabetes.delete_many(kwargs)
        return Response(Message.Success)
