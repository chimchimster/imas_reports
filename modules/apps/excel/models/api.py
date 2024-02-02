import pydantic


class Tags(pydantic.BaseModel):
    analyzer_tags_changed: str


class CategoryMassMedia(pydantic.BaseModel):
    COUNTER: str
    name_cat: str


class CategorySocialMedia(pydantic.BaseModel):
    COUNTER: str
    name: str
    type: int


class CategoryNames1:
    categories = list[CategoryMassMedia]


class CategoryNames2:
    categories = list[CategorySocialMedia]
