from bson import ObjectId
from flask import Blueprint
from flask import request, abort, Response

import APP_Constants as AC
from api.utility import document_filter, response, Message
from modules.dbconnect.models.chronic_kidney import ChronicKidneyModel

chronic_kidney_blp = Blueprint(
    'chronic_kidney_blueprint', __name__, url_prefix=f"{AC.APP_ENDPOINT}/disease"
)


@chronic_kidney_blp.route('/chronic_kidney', methods=["GET"])
@response(ChronicKidneyModel)
def chronic_kidney_list_api():
    """Chronic Kidney disease GET endpoint

        Returns:
            [JSON]: [disease Model result JSON]
    """
    from app import db
    return document_filter(db.kidney)


@chronic_kidney_blp.route('/chronic_kidney/<user_id>', methods=["PATCH", "DELETE"])
@response(ChronicKidneyModel)
def chronic_kidney_api(user_id):
    """Chronic Kidney disease PATCH DELETE endpoint

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

    if not db.kidney.find_one(kwargs):
        return Response(Message.NotFound)

    if request.method == "PATCH":
        if not payload:
            abort(400)
        db.kidney.update_many(kwargs, {"$set": payload})
        return db.kidney.find_many(kwargs)
    if request.method == "DELETE":
        db.kidney.delete_many(kwargs)
        return Response(Message.Success)
