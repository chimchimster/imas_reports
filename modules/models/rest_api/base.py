import pydantic


class BaseMetaModel(pydantic.BaseModel, extra=pydantic.Extra.allow):
    lang: str = 'rus'