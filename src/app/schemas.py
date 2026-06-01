# Data Validation
from pydantic import BaseModel


class SuccessResponse(BaseModel):
    message: str
