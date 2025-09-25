from bson import ObjectId
from pydantic import BaseModel


class CustomModel(BaseModel):
    """
    Override the default pydantic base model to handle bson type object id
    """

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True  # required for the _id
        json_encoders = {ObjectId: str}
