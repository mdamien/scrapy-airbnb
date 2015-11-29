import scrapy
from extruct.w3cmicrodata import MicrodataExtractor

from pprint import pprint as pp
import json

def clean(url):
    return url.split('?')[0]

def e0(x):
    e = x.extract()
    if len(e) > 0:
        return e[0]

def extract_bootstrap(response):
    all = {}
    for meta in response.css('meta[id*=_bootstrap-]'):
        id = e0(meta.css('::attr("id")')).replace('_bootstrap-','')
        data = json.loads(e0(meta.css('::attr("content")')))
        all[id] = data
    return all

class AirbnbSpider(scrapy.Spider):
    name = 'airbnb'
    allowed_domains = ['airbnb.com']
    start_urls = ['https://www.airbnb.com/s/San-Francisco--CA?type=apartment']
    custom_settings = {
        'HTTPCACHE_ENABLED': True,
        'HTTPCACHE_DIR': '/tmp/httpcache',
        'HTTPCACHE_GZIP': True,
    }

    def parse(self, response):
        for url in response.css('a::attr("href")').extract():
            url = response.urljoin(clean(url))
            if 'www.airbnb.com' in url and not '.png' in url and not '.jpg' in url and not 'blog.airbnb.com' in url:
                priority = 1 if 'rooms/' in response.url else 0
                yield scrapy.Request(url, self.parse, priority=priority)
        if 'rooms/' in response.url:
            for it in self.parse_listing(response):
                yield it

    def parse_listing(self, response):
        boot = extract_bootstrap(response)
        data = boot['room_options']
        data.update(boot['listing'])
        data.update(boot['neighborhood_card'])
        yield data


