from datetime import datetime as dt
from typing import Optional

from bson import ObjectId
from pydantic import Field, model_validator

from modules.dbconnect.models import CustomModel


class DiabeticModel(CustomModel):
    id: Optional[ObjectId] = Field(ObjectId(), alias="_id")
    user_id: ObjectId
    Pregnancies: int
    Glucose: int
    BloodPressure: int
    SkinThickness: int
    Insulin: int
    BMI: float
    DiabetesPedigreeFunction: float
    Age: float
    result: Optional[str]
    created_at: dt = Field(dt.now())
    updated_at: dt = Field(None)
    is_deleted: bool = Field(False)

    @model_validator(mode="after")
    def datetime_validator(self, values, *args, **kwargs):
        self.updated_at = dt.now() if self.updated_at else self.created_at
        return values
