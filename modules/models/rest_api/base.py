import pydantic

from .secondary import *


class IMASResponseAPIModel(pydantic.BaseModel):
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
