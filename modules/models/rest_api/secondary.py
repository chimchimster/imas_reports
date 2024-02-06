import pydantic
from pydantic import Field, ConfigDict

from typing_extensions import Annotated

from .base import BaseMetaModel
from modules.apps.localization import ReportLanguagePicker


class CategorySocialMediaModel(pydantic.BaseModel):
    # CategoryName

    model_config = ConfigDict(extra='allow')

    COUNTER: str
    name: str
    type: int

    @property
    def counter(self):
        return self.COUNTER


class CategoryMassMediaModel(BaseMetaModel):
    # CategoryName2

    model_config = ConfigDict(extra='allow')

    COUNTER: str
    name_cat: Annotated[str, Field(validate_default=True)]

    @property
    def counter(self):
        return self.COUNTER

    # @classmethod
    # @pydantic.field_validator('name_cat', mode='before')
    # def translate_category(cls):
    #
    #     return ReportLanguagePicker(cls.language)().get('titles').get('smi')


class ItemsCountMassMediaModel(pydantic.BaseModel):
    # ItemsCount

    model_config = ConfigDict(extra='allow')

    COUNTER: str
    res_id: int
    RESOURCE_NAME: str

    @property
    def counter(self):
        return self.COUNTER


class ItemsCountSocialMediaModel(pydantic.BaseModel):
    # ItemsCount2

    model_config = ConfigDict(extra='allow')

    COUNTER: str
    res_id: int
    resource_name: str

    @property
    def counter(self):
        return self.COUNTER


class ItemsMassMediaModel(pydantic.BaseModel):
    # f_news

    model_config = ConfigDict(extra='allow')

    id: str
    title: str
    nd_date: int
    not_date: str
    content: str
    link: str
    news_link: str
    res_id: str
    RESOURCE_NAME: str
    RESOURCE_PAGE_URL: str
    sentiment: int
    full_text: str

    @property
    def resource_name(self):
        return self.RESOURCE_NAME

    @property
    def resource_page_url(self):
        return self.RESOURCE_PAGE_URL


class ItemsSocialMediaModel(pydantic.BaseModel):
    # f_news2

    model_config = ConfigDict(extra='allow')

    id: str
    title: str
    date: int
    text: str
    link: str
    res_id: str
    type: int
    news_link: str
    resource_name: str
    res_link: str
    members: int
    sentiment: int
    full_text: str


class IMASResponseAPIModel(BaseMetaModel):
    analyzer_tags_changed: str
    categoryNames: list[CategoryMassMediaModel]
    categoryNames2: list[CategorySocialMediaModel]
    itemsCount: list[ItemsCountMassMediaModel]
    itemsCount2: list[ItemsCountSocialMediaModel]
    f_news: list[ItemsMassMediaModel]
    f_news2: list[ItemsSocialMediaModel]

    @property
    def tags(self):
        return self.analyzer_tags_changed

    @property
    def category_mass_media(self):
        return self.categoryNames

    @property
    def category_social_media(self):
        return self.categoryNames2

    @property
    def items_count_mass_media(self):
        return self.itemsCount

    @property
    def items_count_social_media(self):
        return self.itemsCount2

    @property
    def items_mass_media(self):
        return self.f_news

    @property
    def items_social_media(self):
        return self.f_news2


__all__ = [
    'IMASResponseAPIModel',
]