import pydantic


class BaseMetaModel(pydantic.BaseModel):
    lang: str = pydantic.Field(default='rus', strict=False)
