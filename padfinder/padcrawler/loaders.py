from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, TakeFirst


class ApartmentPostLoader(ItemLoader):
    tag_sep = '|'

    # input/output processors

    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()

    tag_list_out = Join(tag_sep)
