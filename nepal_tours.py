import scrapy
from numpy import unicode


class Tours(scrapy.Spider):
    name = 'HimalayanGlacier'
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    start_urls = ['https://www.himalayanglacier.com/trips/nepal/',
                  'https://www.himalayanglacier.com/trips/tibet/',
                  'https://www.himalayanglacier.com/trips/bhutan/',
                  'https://www.himalayanglacier.com/trips/india/',
                  'https://www.himalayanglacier.com/trips/tanzania/',
                  'https://www.himalayanglacier.com/trips/vietnam/',
                  'https://www.himalayanglacier.com/trips/thailand/',
                  'https://www.himalayanglacier.com/trips/cambodia/',
                  'https://www.himalayanglacier.com/trips/myanmar/',
                  'https://www.himalayanglacier.com/trips/china/'
                  ]

    def parse(self, response, **kwargs):
        page = response.url.split('/')[-2]
        filename = f'HimalayanGlacier-{page}.html'
        with open(filename, 'w') as f:
            f.write(str(response.text))

        for a in response.xpath("//div[@class='col-sm-12 col-md-12 col-lg-12 col-xl-12 trip-wrap']/div[@class='col-sm-12 col-md-6 col-lg-4 col-xl-4 t-block']/a/@href"):
            yield scrapy.Request(url=a.get(), callback=self.parse_inner)
        next_page = response.xpath("//div[@id = 'gdlr-core-column-20993']/div/div[2]/div/div/div/div[2]/div[4]/a").extract_first()
        # next_page = response.xpath("//a[contains(text(),'Show more')]/load-more/@href").extract()
        next_page = response.urljoin(str(next_page))
        if next_page is not None:
            # yield scrapy.Request(url=next_page, callback=self.parse)
            yield response.follow(next_page, self.parse)

    def parse_inner(self, response):
        # i = 1
        for b in response.xpath("//div[@class='tourmaster-single-header-title-wrap tourmaster-item-pdlr']/div[@class='container-fluid']/div[@class='row']"):
            yield {
                'url': b.xpath("//link[@rel='canonical']/@href").get(),
                'trip_country': b.xpath("//div[@class='col-sm-12 col-md-8 col-lg-8 col-xl-8 trip-topic triphead-block p-0']/div[@class='trip-destinations']/ul/li/text()").get(),
                'trip heading/title': b.xpath("//title/text()").get(),
                'description': response.xpath("//div[@id='tourmaster-page-wrapper']/div[2]/div/div/div/div[2]/div/div[2]/div/div/div/div/div/h6/text()").get(),
                'package_name': b.xpath("//div[@class='col-sm-12 col-md-8 col-lg-8 col-xl-8 trip-topic triphead-block p-0']/h1[@class='tourmaster-single-header-title']/text()").get(),
                'duration': b.xpath("//div[@class='col-sm-12 col-md-8 col-lg-8 col-xl-8 trip-topic triphead-block p-0']/h1[@class='tourmaster-single-header-title']/p/text()").get(),
                'ratings': b.xpath("//div[@class='col-sm-12 col-md-8 col-lg-8 col-xl-8 trip-topic triphead-block p-0']/div[@class='rating']/div[@class='circle-rating']/text()").get(),
                'reviews': b.xpath("//div[@class='col-sm-12 col-md-8 col-lg-8 col-xl-8 trip-topic triphead-block p-0']/div[@class='rating']/div[@class='tourmaster-tour-rating']/span[@class='tourmaster-tour-rating-text']/text()").get(),
                'total_price': b.xpath("//div[@class='col-sm-12 col-md-4 col-lg-4 col-xl-4 trip-price triphead-block p-0']/div[@class='price-tag']/h3/text()").get(),
                'price_per_day': b.xpath("//div[@class='col-sm-12 col-md-4 col-lg-4 col-xl-4 trip-price triphead-block p-0']/div[@class='price-tag']/span/text()").get(),
                'arrival_city': response.xpath("//div[@id='overview']/div/div/div/div/div[2]/div/div/div[2]/span/text()").get(),
                'departure_city': response.xpath("//div[@id='overview']/div/div/div/div/div[2]/div[2]/div/div[2]/span/text()").get(),
                'lodging_level': response.xpath("//div[@id='overview']/div/div/div/div/div[2]/div[3]/div/div[2]/span[3]/text()").get(),
                'meals': response.xpath("//div[@id='overview']/div/div/div/div/div[2]/div[4]/div/div[2]/span/text()").get(),
                'trip_grade': response.xpath("//div[@id='overview']/div/div/div/div/div[2]/div[5]/div/div[2]/span/text()").get(),
                'max_altitude': response.xpath("//div[@id='overview']/div/div/div/div/div[2]/div[6]/div/div[2]/span/text()").get(),
                'attraction': response.xpath("//div[@id='overview']/div/div/div/div/div[2]/div[7]/div/div[2]/span/text()").get(),
                'activity': response.xpath("//div[6]/div/div/div/div/div/div[2]/div[8]/div/div[2]/span/text()").get(),
                'styles': response.xpath("//div[@id='overview']/div/div/div/div/div[2]/div[9]/div/div[2]/span/text()").get(),
                'Itinerary': response.xpath("//a[contains(text(),'Show DetailItinerary')]").getall(),
                'day': response.xpath("//div[@id='itinerary']/section/div/div/div/div/div[3]/table/span/text()").getall(),
                'itinerary': response.xpath("//div[@id='itinerary']/section/div/div/div/div/div[3]/table/tbody/tr/td/span[2]/text()").get(),
                'Max_altitude': response.xpath("//div[@id='itinerary']/section/div/div/div/div/div[3]/table/tbody/tr/td[2]/span/text()").get(),
                'walking_hiking': response.xpath("//div[@id='itinerary']/section/div/div/div/div/div[3]/table/tbody/tr[2]/td[3]/span/text()").get()

            }
