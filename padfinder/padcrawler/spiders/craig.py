import datetime as dt
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.loader.processors import MapCompose
from padcrawler.items import ApartmentPost
from padcrawler.loaders import ApartmentPostLoader
from padcrawler.settings import MAX_POST_AGE_DAYS


class CraigSpider(scrapy.Spider):

    name = "craig"
    allowed_domains = ["craigslist.org"]

    def __init__(self, region='sfbay', subregion='eby'):
        self.region = region
        self.subregion = subregion
        self.start_urls = [
            'http://{}.craigslist.org/search/{}/apa'.format(region, subregion)]

    def parse(self, response):
        posts = response.xpath('//li[@class="result-row"]')
        for post in posts:
            l = ApartmentPostLoader(ApartmentPost(), post)

            l.add_value('region', self.region)
            l.add_value('subregion', self.subregion)
            l.add_value('snapshot_ts', dt.datetime.now().isoformat())

            l.add_xpath('id', './@data-pid')
            l.add_xpath('repost_of', './@data-repost-of')
            l.add_xpath('posted_ts', './/time/@datetime')
            l.add_xpath('url', './/a[@class="result-title hdrlnk"]/@href', MapCompose(response.urljoin))
            l.add_xpath('title', './/a[@class="result-title hdrlnk"]/text()')
            l.add_xpath('price', './/span[@class="result-price"]', re='\$(\d+)')
            l.add_xpath('bedrooms', './/span[@class="housing"]', re='(\d+)br')
            l.add_xpath('sqfeet', './/span[@class="housing"]', re='(\d+)ft')
            l.add_xpath('neighborhood', './/span[@class="result-hood"]', re='\((.*)\)')

            post = l.load_item()

            posted_ts = dt.datetime.strptime(post['posted_ts'], '%Y-%m-%d %H:%M')

            # stop if we've reached posts older than the cutoff
            if (dt.datetime.now() - posted_ts).days > MAX_POST_AGE_DAYS:
                raise CloseSpider('reached post age cutoff ({} days)'
                                  .format(MAX_POST_AGE_DAYS))

            # fill in remaining fields from the post detail page
            detail_url = response.urljoin(post['url'])
            yield scrapy.Request(detail_url,
                                 callback=self.parse_details,
                                 meta={'post': post})

        # request next page of search results
        next_href = response.xpath('//a[@class="button next"]/@href').extract_first()
        next_url = response.urljoin(next_href)
        yield scrapy.Request(next_url, callback=self.parse)

    def parse_details(self, response):
        post = response.meta['post']
        l = ApartmentPostLoader(post, response)

        l.add_xpath('id', '//p[@class="postinginfo"]', re='post id: (\d+)')
        l.add_xpath('address', '//div[@class="mapaddress"]/text()')
        l.add_xpath('latitude', '//@data-latitude')
        l.add_xpath('longitude', '//@data-longitude')
        l.add_xpath('available_date', '//span[@class="housing_movein_now property_date"]/@data-date')

        for tag in [
            'cats are OK - purrr',
            'dogs are OK - wooof',
            'street parking',
            'off-street parking'
            'carport',
            'attached garage',
            'detached garage',
            'no smoking',
            'laundry on site',
            'laundry in bldg',
            'w/d in unit',
            'apartment',
            'condo',
            'cottage/cabin',
            'duplex',
            'flat',
            'house',
            'in-law',
            'loft'
            'townhouse'
        ]:
            l.add_xpath('tag_list', '//text()[.="{}"]'.format(tag))

        return l.load_item()
