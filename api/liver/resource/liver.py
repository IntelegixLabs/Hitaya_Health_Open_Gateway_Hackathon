from bson import ObjectId
from flask import request, abort, Response

from api.utility import document_filter, response, Message
from modules.dbconnect.models.liver import LiverModel
from flask import Blueprint
import APP_Constants as AC

liver_blp = Blueprint(
    'liver_blueprint', __name__, url_prefix=f"{AC.APP_ENDPOINT}/disease"
)

@liver_blp.route('/liver', methods=["GET"])
@response(LiverModel)
def liver_list_api():
    """Liver disease GET endpoint

        Returns:
            [JSON]: [disease Model result JSON]
    """
    from app import db
    return document_filter(db.liver)


@liver_blp.route('/liver/<user_id>', methods=["PATCH", "DELETE"])
@response(LiverModel)
def liver_api(user_id):
    """Liver disease PATCH DELETE endpoint

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

    if not db.liver.find_one(kwargs):
        return Response(Message.NotFound)

    if request.method == "PATCH":
        if not payload:
            abort(400)
        db.liver.update_many(kwargs, {"$set": payload})
        return db.liver.find_many(kwargs)
    if request.method == "DELETE":
        db.liver.delete_many(kwargs)
        return Response(Message.Success)
