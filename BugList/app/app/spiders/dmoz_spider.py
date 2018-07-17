from bs4 import BeautifulSoup
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import time
from scrapy.http import Request
import re
from ..items import BugItem


class DmozSpider(CrawlSpider):

    name = "dmoz"
    allowed_domains = ["www.qu.la"]
    rules = (
        # Rule(
        #     LinkExtractor(allow=('book/\d+/$',)),
        #     callback='parse_item', follow=True),
        # Rule(
        #     LinkExtractor(allow=('attachment\.cgi\?id=\d+&action=diff$',)),
        #     callback='parse_diff'),
    )

    def __init__(self, *a, **kw):
        super(DmozSpider, self).__init__(*a, **kw)
        self.file_name = a[0][0]
        print(self.file_name)
        self.book_id = a[0][1]
        self.id = a[0][1] - a[0][2]
        self.counter = 0
        self.start_urls = self.urls()

    def urls(self):
        while self.id < self.book_id:
            if self.counter > 10:
                break
            yield "https://www.qu.la/book/{0}/".format(self.id)
            self.id += 1

    def parse(self, response):
        try:
            if response.status != 200:
                self.counter += 1
                return
            self.counter = 0
            soup = BeautifulSoup(response.body, 'html.parser')
            # if
            g = re.match(r"window.location.href='(https://www.qu.la/book/.*)';", str.strip(soup.text))
            if g:
                yield Request(g.group(1), callback=self.parse)
                # print(g.group(1))
            else:
                title = soup.find('title').get_text()
                item = BugItem()
                item['id'] = re.match(r"https://www.qu.la/book/(\d+).*", response.url).group(1)
                item['title'] = title
                item['name'] = self.file_name
                yield item
        except Exception as error:
            print(28*'*', error, response.body)

