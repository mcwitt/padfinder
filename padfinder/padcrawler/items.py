from scrapy import Item, Field


class ApartmentPost(Item):

    id = Field()
    repost_of = Field()
    posted_ts = Field()
    snapshot_ts = Field()
    region = Field()
    subregion = Field()
    url = Field()
    title = Field()
    price = Field()
    bedrooms = Field()
    sqfeet = Field()
    neighborhood = Field()
    address = Field()
    latitude = Field()
    longitude = Field()
    available_date = Field()
    tag_list = Field()
