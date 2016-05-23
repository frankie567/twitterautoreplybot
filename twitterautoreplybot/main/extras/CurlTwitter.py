# -*- coding: utf-8 -*-

from django.conf import settings

import os, urllib, sys, tempfile
from bs4 import BeautifulSoup

class CurlTwitter:

    def __init__(self):
        self.username = settings.TWITTER_USERNAME
        self.password = settings.TWITTER_PASSWORD
        self.cookie = tempfile.NamedTemporaryFile()
        self.temporaryHTML = tempfile.NamedTemporaryFile()
        self.authenticityToken = ""
        self.twitterLogin()
        
    # Find the authencity token in HTML
    def getAuthenticityToken(self, html):
        parsed_html = BeautifulSoup(html, 'html.parser')
        authenticity_token = parsed_html.find('input', {'name': 'authenticity_token'})
        return authenticity_token['value']

    # Login to Twitter 
    def twitterLogin(self):
        os.system("curl 'https://mobile.twitter.com/session/new' -H 'accept-encoding: gzip, deflate, sdch' -H 'accept-language: fr-FR,fr;q=0.8,en;q=0.6' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'authority: mobile.twitter.com' --compressed -c '"+self.cookie.name+"' -o "+self.temporaryHTML.name+" > /dev/null 2>&1")
        loginPageString = self.temporaryHTML.read()
        self.authenticityToken = self.getAuthenticityToken(loginPageString)
        
        os.system("curl https://mobile.twitter.com/sessions -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36' -H 'content-type: application/x-www-form-urlencoded' --data 'authenticity_token="+ self.authenticityToken +"&remember_me=1&wfa=1&redirect_after_login=%2F&session%5Busername_or_email%5D="+self.username+"&session%5Bpassword%5D="+self.password+"' --compressed -v -b '"+self.cookie.name+"' -c '"+self.cookie.name+"' -o "+self.temporaryHTML.name+" -L > /dev/null 2>&1")
    
    # Upload image
    def twitterUploadImage(self, imagePath):        
        # Upload
        uploadOutput = tempfile.NamedTemporaryFile()
        os.system("curl 'https://upload.twitter.com/i/media/upload.json' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36' -b '"+self.cookie.name+"' -c '"+self.cookie.name+"' -F 'media=@"+imagePath+"' -F 'm5_csrf_tkn="+self.authenticityToken+"' --compressed -v -L -o "+uploadOutput.name+" > /dev/null 2>&1")
        
        # Get media id
        uploadImageReturn = uploadOutput.read()
        mediaId = re.findall(ur'\"media_id\":(\d+)', uploadImageReturn)[0]
        
        return mediaId
    
    # Tweet
    def twitterTweet(self, tweet, replyStatusId, imagePath = None):
        # Authenticity token
        tokenPage = tempfile.NamedTemporaryFile()
        os.system("curl 'https://twitter.com/' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36' -H 'content-type: application/x-www-form-urlencoded' --compressed -b '"+self.cookie.name+"' -c '"+self.cookie.name+"' -v -L -o "+tokenPage.name+" > /dev/null 2>&1")
        composeTweetPageString = tokenPage.read()
        self.authenticityToken = self.getAuthenticityToken(composeTweetPageString)

        # Prepare data
        data = "authenticity_token="+self.authenticityToken+"&is_permalink_page=false&place_id=&status="+urllib.quote(tweet.encode('utf-8'))+"&tagged_users=&in_reply_to_status_id="+replyStatusId
        # If image, upload
        if (imagePath is not None):
            mediaId = self.twitterUploadImage(imagePath)
            data += ("&media_ids="+mediaId)
            
        # Tweet
        tweetResult = tempfile.NamedTemporaryFile()
        os.system("curl 'https://twitter.com/i/tweet/create' -H 'origin: https://twitter.com' -H 'accept-encoding: gzip, deflate' -H 'x-requested-with: XMLHttpRequest' -H 'accept-language: fr,en;q=0.8' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36' -H 'content-type: application/x-www-form-urlencoded; charset=UTF-8' -H 'accept: application/json, text/javascript, */*; q=0.01' -H 'referer: https://twitter.com/' -H 'authority: twitter.com' -b '"+self.cookie.name+"' -c '"+self.cookie.name+"' --data '"+data+"' --compressed -o "+tweetResult.name+" > /dev/null 2>&1")
        sendTweetPageString = tweetResult.read()
        if (sendTweetPageString.startswith('Forbidden')):
            print(u"We crossed the Twitter limit. We'll retry later 😢")
            sys.exit(-1)
        elif (not sendTweetPageString.startswith('{"tweet_id"')):
            return False
        else:
            return True