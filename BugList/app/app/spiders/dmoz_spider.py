from bs4 import BeautifulSoup
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from ..items import BugItem


class DmozSpider(CrawlSpider):
    name = "dmoz"
    allowed_domains = ["bugzilla.mozilla.org"]
    rules = (
            Rule(
                LinkExtractor(allow=('show_bug\.cgi\?id=\d+', )),
                callback='parse_item'),
        )

    def __init__(self, *a, **kw):
        super(DmozSpider, self).__init__(*a, **kw)
        self.start_urls = self.urls()

    @staticmethod
    def urls():
        limit = 1000
        index = 1
        while True:
            yield "https://bugzilla.mozilla.org/buglist.cgi?" \
                  "bug_status=RESOLVED&" \
                  "field0-0-0=product&" \
                  "field0-0-1=component&" \
                  "field0-0-2=alias&" \
                  "field0-0-3=short_desc&" \
                  "field0-0-4=status_whiteboard&" \
                  "field0-0-5=cf_crash_signature&" \
                  "query_format=advanced&" \
                  "type0-0-0=substring&" \
                  "type0-0-1=substring&" \
                  "type0-0-2=substring&" \
                  "type0-0-3=substring&" \
                  "type0-0-4=substring&" \
                  "type0-0-5=substring&" \
                  "value0-0-0=bug&" \
                  "value0-0-1=bug&" \
                  "value0-0-2=bug&" \
                  "value0-0-3=bug&" \
                  "value0-0-4=bug&" \
                  "value0-0-5=bug&" \
                  "order=bug_id&" \
                  "offset={0}&" \
                  "limit={1}".format((index-1)*limit, limit)
            index += 1
            if (index-1)*limit > 0:
                break

    # def parse(self, response):
    #     soup = BeautifulSoup(response.body, "html.parser")
    #     for item in soup.select('#main-inner > table.bz_buglist.sortable > tbody > tr'):
    #         # print(item)
    #         break
    #     return super().parse(response)

    def parse_item(self, response):
        soup = BeautifulSoup(response.body, "html.parser")
        _assigned = soup.select_one('#field-value-assigned_to > div > a > span')
        _id = soup.select_one('#this-bug')
        _desc = soup.select_one('#ct-0')
        _blocked = []
        # blocked 是否存在
        if soup.select_one('#field-blocked'):
            _blocked = [self.get_id_by_href(a['href']) for a in soup.select('#field-value-blocked a')]
        self.log(type(_assigned))
        item = BugItem()
        item['id'] = self.get_id_by_href(_id['href'])
        item['desc'] = _desc.text
        item['blocked'] = _blocked
        item['dependson'] = 4
        item['assigned'] = _assigned.text if _assigned else 'Unassigned'
        item['reporter'] = 6
        yield item

    @staticmethod
    def get_id_by_href(href):
        try:
            return int(href[href.find('=')+1:])
        except Exception as error:
            print(href)
            raise error
