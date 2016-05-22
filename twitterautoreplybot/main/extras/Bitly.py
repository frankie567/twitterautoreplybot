# -*- coding: utf-8 -*-

from django.conf import settings

import bitly_api

class Bitly:

    def __init__(self):
        self.bitly = bitly_api.Connection(settings.BITLY_LOGIN, settings.BITLY_API_KEY)
        
    def shorten_urls(self, urls):
        shortenedUrls = []
        for url in urls:
            shortenedUrl = self.bitly.shorten(url)
            shortenedUrls.append(shortenedUrl["url"])
        return shortenedUrls
