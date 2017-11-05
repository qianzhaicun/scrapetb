# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 16:22:53 2017
@author: caicai
"""
import requests
import urllib.request
import urllib.parse
import http.cookiejar

LOGIN_URL = 'http://www.jobbole.com/wp-admin/admin-ajax.php'
LOGIN_EMAIL = 'caicai'
LOGIN_PASSWORD = 'asdjkl!@#'

url = LOGIN_URL
postdata = urllib.parse.urlencode({'user_login': LOGIN_EMAIL, 'user_pass': LOGIN_PASSWORD,'action':'user_login'
    ,'remember_me':'1','redirect_url':'http://www.jobbole.com/'}).encode('utf-8')
req = urllib.request.Request(url,postdata)
req.add_header('User-Agent','Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:55.0) Gecko/20100101 Firefox/55.0')
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

#url2 = 'http://date.jobbole.com/4510/'
#data2=urllib.request.urlopen(url2).read()
#fhandle=open('4.html','wb')
#fhandle.write(data2)
#fhandle.close()

print(cjar)


second_response = requests.post('http://www.jobbole.com/login', postdata, cookies=cjar)
print(second_response.url)