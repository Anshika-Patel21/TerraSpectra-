from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):

    farm_id: str = Field(
        ...,
        min_length=1,
        description="Unique farm identifier"
    )

    file_name: str = Field(
        ...,
        min_length=1,
        description="Hyperspectral image filename"
    )