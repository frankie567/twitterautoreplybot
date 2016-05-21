from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

import re, random, twitter, bitly_api

# Create your models here.        
class Campaign(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="campaigns", blank=True, null=True, editable=False)
    name = models.CharField(max_length=255)
    answerSentence = models.TextField()
    running = models.BooleanField(default=False)
    lastRun = models.DateTimeField(blank=True, null=True, editable=False)
    jobId = models.CharField(max_length=255, blank=True, null=True, editable=False)
    
    def nbTweetsReplied(self):
        return self.tweet_actions.filter(action__type__exact="replied").count()
    def nbTweetsClicked(self):
        return self.tweet_actions.filter(clicked=True).count()
    def nbTweetsPrefrCreated(self):
        return self.tweet_actions.filter(prefrCreated=True).count()
        
    def getTweetDetails(self, limit=5):
        tweetActions = self.tweet_actions.filter(action__type__exact="replied").order_by('-pk')[:limit]
        tweetDetails = []
        
        twitterClient = twitter.Api(
            consumer_key = settings.TWITTER_CONSUMER_KEY,
            consumer_secret = settings.TWITTER_CONSUMER_SECRET,
            access_token_key = settings.TWITTER_ACCESS_TOKEN,
            access_token_secret = settings.TWITTER_ACCESS_SECRET
        )
        for tweetAction in tweetActions:
            try:
                tweet = twitterClient.GetStatus(id = tweetAction.tweet.tweet_id, include_entities = True)
                tweetDetails.append({"id": tweet.id, "message": tweet.text, "query": tweetAction.query, "clicked": tweetAction.clicked, "prefrCreated": tweetAction.prefrCreated})
            except twitter.TwitterError:
                tweetDetails.append({"id": tweet.id, "message": "-", "query": tweetAction.query, "clicked": tweetAction.clicked, "prefrCreated": tweetAction.prefrCreated})
        
        return tweetDetails
    
    def generateAnswerSentence(self, twitterUsername, tweetId, queryMagicWord):
        toReturn = self.answerSentence
        # Replace Twitter username, tweet id, and magic word
        toReturn = toReturn.replace('%twitterUsername%', twitterUsername)
        toReturn = toReturn.replace('%tweetId%', tweetId)
        toReturn = toReturn.replace('%magicWord%', queryMagicWord)
        
        # Shorten URLs
        urls = re.findall(r'(https?://\S+)', toReturn)
        shortenedUrls = []
        if (len(urls) > 0):
            bitly = bitly_api.Connection(settings.BITLY_LOGIN, settings.BITLY_API_KEY)
            for url in urls:
                shortenedUrl = bitly.shorten(url)
                shortenedUrls.append(shortenedUrl["url"])
                toReturn = toReturn.replace(url, shortenedUrl["url"])
        
        # Process word sets
        p = re.compile(ur'\[([^\]]+)\]')
        wordSets = re.findall(p, toReturn)
        for wordSet in wordSets:
            words = wordSet.split('|')
            randomWord = random.choice(words)
            toReturn = toReturn.replace("[" + wordSet + "]", randomWord, 1)
            
        return toReturn, shortenedUrls
    
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('main:CampaignView', kwargs={'pk': self.pk})
        
class Query(models.Model):
    query = models.CharField(max_length=255)
    correspondingSentence = models.CharField(max_length=255)
    campaign = models.ForeignKey(Campaign, related_name="queries")
    requiredNumberOfImages = models.IntegerField(blank=True, null=True)
    answerWithImage = models.BooleanField(default=False)
    
    def nbTweetsSeen(self):
        return Tweet.objects.filter(tweet_actions__query__pk__exact=self.pk).count()
    def nbTweetsReplied(self):
        return Tweet.objects.filter(tweet_actions__query__pk__exact=self.pk, tweet_actions__action__type__exact="replied").count()
    def nbTweetsClicked(self):
        return Tweet.objects.filter(tweet_actions__query__pk__exact=self.pk, tweet_actions__clicked=True).count()
    def nbTweetsPrefrCreated(self):
        return Tweet.objects.filter(tweet_actions__query__pk__exact=self.pk, tweet_actions__prefrCreated=True).count()
    
    def __unicode__(self):
        return self.query
    
class Action(models.Model):
    type = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.type   
    
class Tweet(models.Model):
    tweet_id = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.tweet_id
        
class TweetAction(models.Model):
    tweet = models.ForeignKey(Tweet, related_name="tweet_actions")
    action = models.ForeignKey(Action)
    query = models.ForeignKey(Query, related_name="tweet_actions")
    campaign = models.ForeignKey(Campaign, related_name="tweet_actions")
    shortened_urls = models.TextField(blank=True, null=True)
    clicked = models.BooleanField(default=False)
    prefrCreated = models.BooleanField(default=False)
    
    def setShortenedUrls(self, shortenedUrls):
        self.shortened_urls = ','.join(shortenedUrls)
        
    def getShortenedUrls(self):
        return self.shortened_urls.split(",")

class Image(models.Model):
    tweet = models.ForeignKey(Tweet, related_name="images")
    url = models.URLField()
    
    def __unicode__(self):
        return self.url