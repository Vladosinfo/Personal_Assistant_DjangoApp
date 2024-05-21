import json
import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field

class NewItem(Item):
    cur_date = Field()
    min_temperature =   Field()
    max_temperature = Field()

# class NewItemSport(Item):
#     news_headline = Field()
#     news_date = Field()
#
#
# class NewItemNews(Item):
#     date_news = Field()
#     news_time = Field()
#     headline = Field()


class DataPipline:
    weather = []
    # news_sport = []
    # news = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'cur_date' in adapter.keys():
            self.weather.append(dict(adapter))
        # if 'news_headline' in adapter.keys():
        #     self.news_sport.append(dict(adapter))
        # if "date_news" in adapter.keys():
        #     self.news.append(dict(adapter))

    def close_spider(self, spider):
        with open('weather.json', 'w', encoding='utf-8') as fd:
            json.dump(self.weather, fd, ensure_ascii=False, indent=2)

        # with open('news_sport.json', 'w', encoding='utf-8') as fd:
        #     json.dump(self.news_sport, fd, ensure_ascii=False, indent=2)
        #
        # with open("news.json", "w", ) as fd:
        #     json.dump(self.news, fd, ensure_ascii=False, indent=2)


class QuotesSpider(scrapy.Spider):
    # dni = ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень', 'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень']
    # day_week = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    name = "get_weather"
    allowed_domains = ["ua.sinoptik.ua"]
    start_urls = ["https://ua.sinoptik.ua/"]
    custom_settings = {"ITEM_PIPELINES": {DataPipline: 300}}
    def parse(self, response, **kwargs):
        for q in response.xpath("/html//div[@class='main loaded']"):
            cur_date0 = q.xpath("p[@class='day-link']/text()").get().strip()
            cur_date1 = q.xpath("p[@class='date ']/text()").get().strip()
            cur_date2 = q.xpath("p[@class='month']/text()").get().strip()
            cur_date = cur_date0 + " " + cur_date1 + " " + cur_date2
            min_temperature = q.xpath("div[@class='temperature']/div[@class='min']/span/text()").get().strip()
            max_temperature = q.xpath("div[@class='temperature']/div[@class='max']/span/text()").get().strip()

            yield NewItem(cur_date=cur_date, min_temperature=min_temperature, max_temperature=max_temperature)

# class QuotesSpiderSport(scrapy.Spider):
#     name = "get_news_sport"
#     allowed_domains = ["www.volleyball.ua"]
#     start_urls = ["https://www.volleyball.ua/"]
#     custom_settings = {"ITEM_PIPELINES": {DataPipline: 300}}
#     def parse(self, response, **kwargs):
#         for q in response.xpath("/html//div[@class='row']/div[@class='col col-lg-6 col-md-6 col-sm-12 col-xs-12']"):
#             news_headline = q.xpath("div[@class='news-item col-lg-12 col-md-12 col-sm-12 col-xs-12']/a/h3/text()").get().strip()
#             news_date = q.xpath("div[@class='news-item col-lg-12 col-md-12 col-sm-12 col-xs-12']/div[@class='news-info row']/div[@class='col col-lg-7 col-md-7 col-sm-7 col-xs-7']/span[@class='news-date']/text()").get().strip()
#             yield NewItemSport(news_headline = news_headline, news_date=news_date)


# class QuotesSpiderNews(scrapy.Spider):
#     name = "get_news"
#     allowed_domains = ["www.meta.ua"]
#     start_urls = ["https://meta.ua/uk/"]
#     custom_settings = {"ITEM_PIPELINES": {DataPipline: 300}}
#
#     def parse(self, response, **kwargs):
#         date_news = date.today()
#         for q in response.xpath("/html//div{@class = 'main_news__wrapper category-1 active']"):
#             title = (
#                 q.xpath(
#                     "div[@class='content']/a[@class='main_news__link']/text()"
#                 )
#                 .get()
#                 .strip()
#             )
#             date_news = q.xpath("div[@class='news-item col-lg-12 col-md-12 col-sm-12 col-xs-12']/div[@class='news-info row']/div[@class='col col-lg-7 col-md-7 col-sm-7 col-xs-7']/span[@class='news-date']/text()").get().strip()
#             yield NewItemNews(date_news=date_news, title=title)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    # process.crawl(QuotesSpiderNews)
    # process.crawl(QuotesSpiderSport)
    process.start()
