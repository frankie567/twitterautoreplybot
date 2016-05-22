from django.test import TestCase

from main.models import Campaign
from main.extras import Bitly

import re

# Bitly service tests
class BitlyTestCase(TestCase):
    def setUp(self):
        self.bitly = Bitly.Bitly()
    
    def test_shorten_urls_with_one_url(self):
        urls = ["https://github.com/frankie567/twitterautoreplybot"]
        shortened_urls = self.bitly.shorten_urls(urls)
        
        # Same size
        self.assertEqual(len(shortened_urls), 1)
        # Check if we truly have Bitly URLs
        bitly_url_pattern = re.compile(ur'http:\/\/bit\.ly\/[a-zA-Z0-9]+')
        for shortened_url in shortened_urls:    
            self.assertTrue(re.match(bitly_url_pattern, shortened_url))
    
    def test_shorten_urls_with_several_urls(self):
        urls = [
            "https://github.com/frankie567/twitterautoreplybot",
            "https://hub.docker.com/r/frankie567/twitterautoreplybot/",
            "https://www.francoisvoron.com"
        ]
        shortened_urls = self.bitly.shorten_urls(urls)
        
        # Same size
        self.assertEqual(len(shortened_urls), 3)
        # Check if we truly have Bitly URLs
        bitly_url_pattern = re.compile(ur'http:\/\/bit\.ly\/[a-zA-Z0-9]+')
        for shortened_url in shortened_urls:    
            self.assertTrue(re.match(bitly_url_pattern, shortened_url))

# Campaign model tests
class CampaignTestCase(TestCase):
    def setUp(self):
        Campaign.objects.create(
            name = "Test campaign",
            answerSentence = "Username : %twitterUsername% / Magic word : %magicWord% / Tweet id : %tweetId% / Random word : [cool|nice|wonderful|lol] / URL : http://www.francoisvoron.com"
        )
            
    def test_generateAnswerSentence(self):
        campaign_test = Campaign.objects.get(name = "Test campaign")
        answer_sentence = campaign_test.generateAnswerSentence("TwitterUser", "1234", "MagicWord")
        
        # Check if sentence result is as expected
        answer_sentence_pattern = re.compile(ur'Username : TwitterUser \/ Magic word : MagicWord \/ Tweet id : 1234 \/ Random word : (cool|nice|wonderful|lol) \/ URL : http:\/\/bit\.ly\/[a-zA-Z0-9]+')
        self.assertTrue(re.match(answer_sentence_pattern, answer_sentence[0]))
        
        # Check if we have a shortened URL
        self.assertEqual(len(answer_sentence[1]), 1)
