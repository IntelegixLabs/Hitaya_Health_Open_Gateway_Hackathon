from datetime import datetime as dt
from typing import Optional

from bson import ObjectId
from pydantic import Field, model_validator

from modules.dbconnect.models import CustomModel


class LiverModel(CustomModel):
    id: Optional[ObjectId] = Field(ObjectId(), alias="_id")
    user_id: ObjectId
    Age: int
    Gender_Female: int
    Gender_Male: int
    Total_Bilirubin: int | float
    Direct_Bilirubin: int | float
    Alkaline_Phosphotase: int | float
    Alamine_Aminotransferase: int | float
    Aspartate_Aminotransferase: int | float
    Total_Protiens: int | float
    Albumin: int | float
    Albumin_and_Globulin_Ratio: int | float
    created_at: dt = Field(dt.now())
    updated_at: dt = Field(None)
    is_deleted: bool = Field(False)
    result: str

    @model_validator(mode="after")
    def datetime_validator(self, values, *args, **kwargs):
        self.updated_at = dt.now() if self.updated_at else self.created_at
        return values
