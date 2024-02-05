import pydantic


class CategorySocialMediaModel(pydantic.BaseModel):
    # CategoryName
    COUNTER: str
    name: str
    type: int

    @property
    def counter(self):
        return self.COUNTER


class CategoryMassMediaModel(pydantic.BaseModel):
    # CategoryName2
    COUNTER: str
    name_cat: str

    @property
    def counter(self):
        return self.COUNTER


class ItemsCountMassMediaModel(pydantic.BaseModel):
    # ItemsCount
    COUNTER: str
    res_id: int
    RESOURCE_NAME: str

    @property
    def counter(self):
        return self.COUNTER


class ItemsCountSocialMediaModel(pydantic.BaseModel):
    # ItemsCount2
    COUNTER: str
    res_id: int
    resource_name: str

    @property
    def counter(self):
        return self.COUNTER


class ItemsMassMediaModel(pydantic.BaseModel):
    # f_news
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


__all__ = [
    'CategorySocialMediaModel',
    'CategoryMassMediaModel',
    'ItemsCountMassMediaModel',
    'ItemsCountSocialMediaModel',
    'ItemsMassMediaModel',
    'ItemsSocialMediaModel',
]