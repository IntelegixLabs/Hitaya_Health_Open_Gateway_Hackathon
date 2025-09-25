from datetime import datetime as dt
from typing import Optional

from bson import ObjectId
from pydantic import Field, model_validator

from modules.dbconnect.models import CustomModel


class HeartModel(CustomModel):
    id: Optional[ObjectId] = Field(ObjectId(), alias="_id")
    user_id: ObjectId
    age: int
    sex: int
    cp: int | float
    trestbps: int | float
    chol: int | float
    fbs: int | float
    restecg: int | float
    exang: int | float
    oldpeak: int | float
    slope: int | float
    ca: int | float
    thal: int | float
    created_at: dt = Field(dt.now())
    updated_at: dt = Field(None)
    is_deleted: bool = Field(False)
    result: str

    @model_validator(mode="after")
    def datetime_validator(self, values, *args, **kwargs):
        self.updated_at = dt.now() if self.updated_at else self.created_at
        return values
