# -*- coding:utf-8 -*-
"""
@author: shenbing
@file: ZentaoParser.py
@time: 2018/6/8 14:30
"""

from bs4 import BeautifulSoup
import urllib
import http.cookiejar


class ZentaoParser(object):

    def __init__(self, loginUrl, username, password):
        super()
        self.loginUrl = loginUrl
        self.baseUrl = loginUrl[0:len(loginUrl) - loginUrl[::-1].index("/")]
        self.username = username
        self.password = password
        self.productUrl = self.baseUrl + "product-ajaxGetDropMenu-1-product-all-.html"
        self.bugBrowseTemp = self.baseUrl + "bug-browse-%d.html"
        self.bugReportTemp = self.baseUrl + "bug-report-%d-unclosed-0-0.html"
        self.cookie = http.cookiejar.CookieJar()
        self.handle = urllib.request.HTTPCookieProcessor(self.cookie)
        self.opener = urllib.request.build_opener(self.handle)

    def login(self):
        loginparams = {"account": self.username, "password": self.password, "keepLogin[]": "on"}
        response = self.opener.open(self.loginUrl, urllib.parse.urlencode(loginparams).encode('utf-8'))
        return response.read()

    def getProductInfo(self):
        product_ids = []
        product_names = []
        if "parent.location='/zentao/index.html'" in str(self.login()):
            response = self.opener.open(self.productUrl)
            soup = BeautifulSoup(response.read(), "html.parser", from_encoding="utf8")
            productIds = soup.select("div#defaultMenu > ul > li")
            for item in productIds:
                product_ids.append(int(item['data-id']))
            productNames = soup.select("div#defaultMenu > ul > li > a")
            for item in productNames:
                product_names.append(item.text.strip())
        return dict(zip(product_ids, product_names))

    def getNewlyBug(self) -> dict:
        result = {}
        productInfos = self.getProductInfo()
        param = {"charts[]": "openedBugsPerDay"}
        for id, name in productInfos.items():
            date_list = []
            value_list = []
            self.opener.open(self.bugBrowseTemp % id)
            response = self.opener.open(self.bugReportTemp % id, urllib.parse.urlencode(param).encode('utf-8'))
            soup = BeautifulSoup(response.read(), "html.parser", from_encoding="utf8")
            date_data = soup.find_all(name="td", attrs={'class': 'chart-label'})
            for item in date_data:
                if len(item.contents) == 1:
                    date = str(item.contents[0])
                    date_list.append(date)
            value_data = soup.find_all(name="td", attrs={'class': 'chart-value'})
            for item in value_data:
                if len(item.contents) == 1:
                    value_list.append(int(item.contents[0]))
            # date_list = date_list[-60:]
            # value_list = value_list[-60:]
            bugs_dict = dict(zip(date_list, value_list))
            result[name] = bugs_dict
            soup.clear()
        return result

    def getBugStatus(self):
        result = {}
        productInfos = self.getProductInfo()
        param = {"charts[]": "bugsPerStatus"}
        for id, name in productInfos.items():
            category_list = []
            value_list = []
            self.opener.open(self.bugBrowseTemp % id)
            response = self.opener.open(self.bugReportTemp % id, urllib.parse.urlencode(param).encode('utf-8'))
            soup = BeautifulSoup(response.read(), "html.parser", from_encoding="utf8")
            date_data = soup.find_all(name="td", attrs={'class': 'chart-label'})
            for item in date_data:
                if len(item.contents) == 1:
                    category = str(item.contents[0])
                    category_list.append(category)
            value_data = soup.find_all(name="td", attrs={'class': 'chart-value'})
            for item in value_data:
                if len(item.contents) == 1:
                    value_list.append(int(item.contents[0]))
            result[name] = dict(zip(category_list, value_list))
        return result


if __name__ == '__main__':
    loginUrl = 'http://10.1.210.51:80/zentao/user-login.html'
    username = 'shenbing'
    password = 'aA!111111'
    zentaoParser = ZentaoParser(loginUrl, username, password)
    print(zentaoParser.getBugStatus())
    print(zentaoParser.getNewlyBug())