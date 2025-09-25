from bson import ObjectId
from flask import Blueprint
from flask import request, abort, Response

import APP_Constants as AC
from api.utility import document_filter, response, Message
from modules.dbconnect.models.breast_cancer import BreastCancerModel

breast_cancer_blp = Blueprint(
    'breast_cancer_blueprint', __name__, url_prefix=f"{AC.APP_ENDPOINT}/disease"
)


@breast_cancer_blp.route('/breast_cancer', methods=["GET"])
@response(BreastCancerModel)
def breast_cancer_list_api():
    """Breast Cancer disease GET endpoint

        Returns:
            [JSON]: [disease Model result JSON]
    """
    from app import db
    return document_filter(db.breast_cancer)


@breast_cancer_blp.route('/breast_cancer/<user_id>', methods=["PATCH", "DELETE"])
@response(BreastCancerModel)
def breast_cancer_api(user_id):
    """Breast Cancer disease PATCH DELETE endpoint

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

    if not db.breast_cancer.find_one(kwargs):
        return Response(Message.NotFound)

    if request.method == "PATCH":
        if not payload:
            abort(400)
        db.breast_cancer.update_many(kwargs, {"$set": payload})
        return db.breast_cancer.find_many(kwargs)
    if request.method == "DELETE":
        db.breast_cancer.delete_many(kwargs)
        return Response(Message.Success)
