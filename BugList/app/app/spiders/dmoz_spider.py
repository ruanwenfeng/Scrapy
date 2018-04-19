from bs4 import BeautifulSoup
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from ..items import BugItem


class DmozSpider(CrawlSpider):
    name = "dmoz"
    allowed_domains = ["bugzilla.mozilla.org"]
    rules = (
            Rule(
                LinkExtractor(allow=('show_bug\.cgi\?id=\d+$', )),
                callback='parse_item', follow=True),
            # Rule(
            #     LinkExtractor(allow=('attachment\.cgi\?id=\d+&action=diff$',)),
            #     callback='parse_diff'),
        )

    def __init__(self, *a, **kw):
        super(DmozSpider, self).__init__(*a, **kw)
        self.start_urls = self.urls()

    @staticmethod
    def urls():
        limit = 100
        index = 1
        # yield 'https://bugzilla.mozilla.org/show_bug.cgi?id=15809'
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
            if (index-1)*limit > 10000:
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
        _depends = []
        _duplicates = []
        # blocked 是否存在
        if soup.select_one('#field-blocked'):
            _blocked = [self.get_id_by_href(a['href']) for a in soup.select('#field-value-blocked a')]

        # Depends 是否存在
        if soup.select_one('#field-dependson'):
            _depends = [self.get_id_by_href(a['href']) for a in soup.select('#field-value-dependson a')]

        # Duplicates 是否存在
        if soup.select_one("a[href='https://wiki.mozilla.org/BMO/UserGuide/BugFields#duplicates']"):
            _duplicates = [self.get_id_by_href(a['href']) for a in
                           soup.find("a", attrs={"href": 'https://wiki.mozilla.org/BMO/UserGuide/BugFields#duplicates'})
                               .parent.parent.select('div.value > a')]
        _reporter = soup.select_one('#ch-0 span.fna')
        self.log(type(_assigned))
        item = BugItem()
        item['id'] = self.get_id_by_href(_id['href'])
        item['desc'] = _desc.text
        item['blocked'] = _blocked
        item['dependson'] = _depends
        item['assigned'] = _assigned.text if _assigned else 'Unassigned'
        item['reporter'] = _reporter.text
        item['duplicates'] = _duplicates
        yield item


    def parse_diff(self, response):
        soup = BeautifulSoup(response.body, "html.parser")


    @staticmethod
    def get_id_by_href(href):
        try:
            return int(href[href.find('=')+1:])
        except Exception as error:
            print(href)
            raise error
