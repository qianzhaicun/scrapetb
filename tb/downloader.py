# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 13:58:14 2017

@author: admin
"""

from random import choice
import requests

from throttle import Throttle

import urllib.request
import urllib.parse
import http.cookiejar


class Downloader:
    """ Downloader class to use cache and requests for downloading pages.
        For contructor, pass:
            delay (int): # of secs delay between requests (default: 5)
            user_agent (str): user agent string (default: 'wswp')
            proxies (list[dict]): list of possible proxies, each
                must be a dict with http / https keys and proxy values
            cache (dict or dict-like obj): keys: urls, values: dicts with keys (html, code)
            timeout (float/int): number of seconds to wait until timeout
    """
    def __init__(self, delay=5, user_agent='wswp', proxies=None, cache={},
                 timeout=60):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.cache = cache
        self.num_retries = None  # we will set this per request
        self.timeout = timeout
        
        
        LOGIN_URL = 'http://www.jobbole.com/wp-admin/admin-ajax.php'
        LOGIN_EMAIL = 'caicai'
        LOGIN_PASSWORD = 'asdjkl!@#'
            
            
        postdata = urllib.parse.urlencode({'user_login': LOGIN_EMAIL, 'user_pass': LOGIN_PASSWORD,'action':'user_login'
                ,'remember_me':'1','redirect_url':'http://www.jobbole.com/'}).encode('utf-8')
        req = urllib.request.Request(LOGIN_URL,postdata)
        req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:55.0) Gecko/20100101 Firefox/55.0')
        urllib.request.ProxyHandler(proxies=proxies)
        #create CookieJar
        cjar = http.cookiejar.CookieJar()
        #create opener
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
        #open 安装为全局
        urllib.request.install_opener(opener)
            
        file = opener.open(req)
        data=file.read()
        file=open('3.html','wb')
        file.write(data)
        file.close() 
            

    def __call__(self, url, num_retries=2):
        """ Call the downloader class, which will return HTML from cache
            or download it
            args:
                url (str): url to download
            kwargs:
                num_retries (int): # times to retry if 5xx code (default: 2)
        """
        self.num_retries = num_retries
        try:
            result = self.cache[url]
            print('Loaded from cache:', url)
        except KeyError:
            result = None
        if result and self.num_retries and 500 <= result['code'] < 600:
            # server error so ignore result from cache
            # and re-download
            result = None
        if result is None:
            # result was not loaded from cache, need to download
            self.throttle.wait(url)
            proxies = choice(self.proxies) if self.proxies else None
            headers = {'User-Agent': self.user_agent}
            result = self.download(url, headers, proxies)
            self.cache[url] = result
        return result['html']

    def download(self, url, headers, proxies):
        """ Download a and return the page content
            args:
                url (str): URL
                headers (dict): dict of headers (like user_agent)
                proxies (dict): proxy dict w/ keys 'http'/'https', values
                    are strs (i.e. 'http(s)://IP') (default: None)
        """
        print('Downloading:', url)
        try:
            resp = requests.get(url, headers=headers, proxies=proxies,
                                timeout=self.timeout)
            html = resp.text
            
            
            html=urllib.request.urlopen(url).read().decode('utf-8')
            
            if resp.status_code >= 400:
                print('Download error:', resp.text)
                html = None
                if self.num_retries and 500 <= resp.status_code < 600:
                    # recursively retry 5xx HTTP errors
                    self.num_retries -= 1
                    return self.download(url, headers, proxies)
        except requests.exceptions.RequestException as e:
            print('Download error:', e)
            return {'html': None, 'code': 500}
        return {'html': html, 'code': resp.status_code}