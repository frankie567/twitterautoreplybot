from django.test import TestCase
from django.conf import settings

from main.models import Campaign
from main.extras import Bitly, CurlTwitter

import re, time

# Bitly service tests
class BitlyTestCase(TestCase):
    def setUp(self):
        self.bitly = Bitly.Bitly()
    
    def test_shorten_urls_with_one_url(self):
        urls = ['https://github.com/frankie567/twitterautoreplybot']
        shortened_urls = self.bitly.shorten_urls(urls)
        
        # Same size
        self.assertEqual(len(shortened_urls), 1)
        # Check if we truly have Bitly URLs
        bitly_url_pattern = re.compile(ur'http:\/\/bit\.ly\/[a-zA-Z0-9]+')
        for shortened_url in shortened_urls:    
            self.assertTrue(re.match(bitly_url_pattern, shortened_url))
    
    def test_shorten_urls_with_several_urls(self):
        urls = [
            'https://github.com/frankie567/twitterautoreplybot',
            'https://hub.docker.com/r/frankie567/twitterautoreplybot/',
            'https://www.francoisvoron.com'
        ]
        shortened_urls = self.bitly.shorten_urls(urls)
        
        # Same size
        self.assertEqual(len(shortened_urls), 3)
        # Check if we truly have Bitly URLs
        bitly_url_pattern = re.compile(ur'http:\/\/bit\.ly\/[a-zA-Z0-9]+')
        for shortened_url in shortened_urls:    
            self.assertTrue(re.match(bitly_url_pattern, shortened_url))
            
# CurlTwitter service tests
class CurlTwitterTestCase(TestCase):
    def setUp(self):
        self.curl_twitter = CurlTwitter.CurlTwitter()
        
    def test_twitterLogin(self):
        # Check if cookie contains session
        self.assertTrue('_twitter_sess' in self.curl_twitter.cookie.read())
        
    def test_twitterTweetWithoutImage(self):
        tweet = 'test_twitterTweetWithoutImage unit test on ' + str(time.time())
        reply_status_id = '733989999952154624'
        self.assertTrue(self.curl_twitter.twitterTweet(tweet, reply_status_id))
        
    def test_twitterTweetWithImage(self):
        tweet = 'test_twitterTweetWithImage unit test on ' + str(time.time())
        reply_status_id = '733989999952154624'
        image_path = settings.BASE_DIR + '/main/tests/test-image.jpg'
        self.assertTrue(self.curl_twitter.twitterTweet(tweet, reply_status_id, image_path))

# Campaign model tests
class CampaignTestCase(TestCase):
    def setUp(self):
        Campaign.objects.create(
            name = 'Test campaign',
            answerSentence = 'Username : %twitterUsername% / Magic word : %magicWord% / Tweet id : %tweetId% / Random word : [cool|nice|wonderful|lol] / URL : http://www.francoisvoron.com'
        )
            
    def test_generateAnswerSentence(self):
        campaign_test = Campaign.objects.get(name = 'Test campaign')
        answer_sentence = campaign_test.generateAnswerSentence('TwitterUser', '1234', 'MagicWord')
        
        # Check if sentence result is as expected
        answer_sentence_pattern = re.compile(ur'Username : TwitterUser \/ Magic word : MagicWord \/ Tweet id : 1234 \/ Random word : (cool|nice|wonderful|lol) \/ URL : http:\/\/bit\.ly\/[a-zA-Z0-9]+')
        self.assertTrue(re.match(answer_sentence_pattern, answer_sentence[0]))
        
        # Check if we have a shortened URL
        self.assertEqual(len(answer_sentence[1]), 1)
