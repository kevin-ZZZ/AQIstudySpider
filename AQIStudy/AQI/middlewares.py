# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html


from selenium import webdriver
import scrapy
import time

class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        driver = webdriver.Chrome()

        driver.get(request.url)
        time.sleep(2)
        html = driver.page_source

        driver.quit()

        return scrapy.http.HtmlResponse(url=request.url, body=html, encoding="utf-8", request = request)

