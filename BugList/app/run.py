from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import multiprocessing


def worker(index):
    process = CrawlerProcess(get_project_settings())
    process.crawl('dmoz', ['item{0}.json'.format(str(index)), 15000*index, 15000])
    process.start()


if __name__ == '__main__':
    prp = [multiprocessing.Process(target=worker, args=(i+1,)) for i in range(4)]
    [p.start() for p in prp]