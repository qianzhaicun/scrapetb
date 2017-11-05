import re
from urllib import robotparser
from urllib.parse import urljoin

import requests
from throttle import Throttle

import csv
import re
from lxml.html import fromstring
from lxml import etree
#导入parse模块
from urllib import parse

class CsvCallback:
    def __init__(self):
        self.writer = csv.writer(open('../data/countries.csv', 'w'))
        self.fields = ('area', 'population', 'iso', 'country',
        'capital', 'continent', 'tld', 'currency_code',
        'currency_name',
        'phone', 'postal_code_format', 'postal_code_regex',
        'languages', 'neighbours')
        self.writer.writerow(self.fields)
    def __call__(self, url, html):
        if re.search('/view/', url):
            tree = fromstring(html)
            all_rows = [tree.xpath(
                    '//tr[@id="places_%s__row"]/td[@class="w2p_fw"]' %
                    field)[0].text_content()
                for field in self.fields]
            self.writer.writerow(all_rows)

def download(url, user_agent='wswp', num_retries=2, proxies=None):
    """ Download a given URL and return the page content
        args:
            url (str): URL
        kwargs:
            user_agent (str): user agent (default: wswp)
            proxies (dict): proxy dict w/ keys 'http' and 'https', values
                            are strs (i.e. 'http(s)://IP') (default: None)
            num_retries (int): # of retries if a 5xx error is seen (default: 2)
    """
    print('Downloading:', url)
    headers = {'User-Agent': user_agent}
    try:
        resp = requests.get(url, headers=headers, proxies=proxies)
        html = resp.text
        if resp.status_code >= 400:
            print('Download error:', resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                # recursively retry 5xx HTTP errors
                return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print('Download error:', e)
        html = None
    return html


def get_robots_parser(robots_url):
    " Return the robots parser object using the robots_url "
    rp = robotparser.RobotFileParser()
    rp.set_url(robots_url)
    rp.read()
    return rp


def get_links(html):
    """ Return a list of links (using simple regex matching)
        from the html content """
    # a regular expression to extract all links from the webpage
    webpage_regex = re.compile("""<a[^>]+href=["'](.*?)["']""", re.IGNORECASE)
    # list of all links from the webpage
    return webpage_regex.findall(html)


def link_crawler(start_url, link_regex, robots_url=None, user_agent='wswp',
                 proxies=None, delay=3, max_depth=4):
    """ Crawl from the given start URL following links matched by link_regex.
    In the current implementation, we do not actually scrape any information.
        args:
            start_url (str): web site to start crawl
            link_regex (str): regex to match for links
        kwargs:
            robots_url (str): url of the site's robots.txt
                              (default: start_url + /robots.txt)
            user_agent (str): user agent (default: wswp)
            proxies (dict): proxy dict w/ keys 'http' and 'https', values
                            are strs (i.e. 'http(s)://IP') (default: None)
            delay (int): seconds to throttle between requests
                         to one domain (default: 3)
            max_depth (int): maximum crawl depth (to avoid traps) (default: 4)
    """
    crawl_queue = [start_url]
    # keep track which URL's have seen before
    seen = {}
    if not robots_url:
        robots_url = '{}/robots.txt'.format(start_url)
    rp = get_robots_parser(robots_url)
    throttle = Throttle(delay)
    while crawl_queue:
        url = crawl_queue.pop()
        # check url passes robots.txt restrictions
        if rp.can_fetch(user_agent, url):
            depth = seen.get(url, 0)
            if depth == max_depth:
                print('Skipping %s due to depth' % url)
                continue
            throttle.wait(url)
            html = download(url, user_agent=user_agent, proxies=proxies)
            if not html:
                continue
            # TODO: add actual data scraping here
            # filter for links matching our regular expression
            for link in get_links(html):
                if re.match(link_regex, link):
                    abs_link = urljoin(start_url, link)
                    if abs_link not in seen:
                        seen[abs_link] = depth + 1
                        crawl_queue.append(abs_link)
        else:
            print('Blocked by robots.txt:', url)
    print(len(seen))


if __name__ == "__main__":
    #print(link_crawler("http://date.jobbole.com/",r'^(http://date.jobbole.com/)(\d+)/$'))
    user_agent = 'wswp'
    url = input('请复制url:')
    #url = 'https://item.taobao.com/item.htm?id=547627656391&ali_refid=a3_430673_1006:1150119134:N:%E5%AE%A2%E5%8E%85%E7%81%AF:61dc40e224ec86e921314c179963a3a8&ali_trackid=1_61dc40e224ec86e921314c179963a3a8&spm=a2e15.8261149.07626516002.2'
    proxies = None
    html = download(url, user_agent=user_agent, proxies=proxies)
    print(html)
    tree = fromstring(html)
    #atitle = tree.xpath('//title[@id="places_area__row"]/td[@class="w2p_fw"]/text()')[0]
    productName = tree.xpath('//title/text()')[0]
    atitle = productName.split('-')
    print(atitle[0])

    #urp = parse.urlparse(url)

    #print(urp)
    #itemId = tree.xpath('//input[@name="item_id"]/@value')[0]
    #print('aitemid: ' + itemId)
    query = parse.splitquery(url)
    #print(parse.splitquery(url)[1])

    itemId = (re.findall(r'id=(.*?)&', url)[0])
    print('aitemid: ' + itemId)

    rangePrice = tree.xpath('//*[@id="J_StrPriceModBox"]')
    print(rangePrice)
    #rangePrice = tree.xpath('//em[@class="tb-rmb-num"]/text()')[0]
    #print('rangePrice: ' + rangePrice)
    
    