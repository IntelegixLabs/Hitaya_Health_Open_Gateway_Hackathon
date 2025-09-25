from datetime import datetime as dt
from typing import Optional

from bson import ObjectId
from pydantic import Field, model_validator

from modules.dbconnect.models import CustomModel


class ChronicKidneyModel(CustomModel):
    id: Optional[ObjectId] = Field(ObjectId(), alias="_id")
    user_id: ObjectId
    aga: int
    bp: int | float
    sg: int | float
    al: int | float
    su: int | float
    rbc: int | float
    pc: int | float
    pcc: int | float
    ba: int | float
    bgr: int | float
    bu: int | float
    sc: int | float
    sod: int | float
    pot: int | float
    hemo: int | float
    pcv: int | float
    wc: int | float
    rc: int | float
    htn: int | float
    dm: int | float
    cad: int | float
    appet: int | float
    pe: int | float
    ane: int | float
    result: str
    created_at: dt = Field(dt.now())
    updated_at: dt = Field(None)
    is_deleted: bool = Field(False)

    @model_validator(mode="after")
    def datetime_validator(self, values, *args, **kwargs):
        self.updated_at = dt.now() if self.updated_at else self.created_at
        return values
