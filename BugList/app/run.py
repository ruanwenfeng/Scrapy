from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('dmoz')
    process.start()
