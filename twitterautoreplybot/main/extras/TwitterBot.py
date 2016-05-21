from django.conf import settings
from main.models import Campaign, Action, Tweet, TweetAction

import twitter, datetime, time, random, os
import CurlTwitter, GeneratePreviewImage

def randomSleep(min, max):
    waitingTime = random.randint(min, max)
    time.sleep(waitingTime)
    
# Get number of embed images in tweet
def getTweetMedias(client, tweetId):
    try:
        tweet = client.GetStatus(id = tweetId, include_entities = True)
        return tweet.media
    except twitter.TwitterError:
        return False

def twitterBot(campaignPk):
    twitterClient = twitter.Api(
        consumer_key = settings.TWITTER_CONSUMER_KEY,
        consumer_secret = settings.TWITTER_CONSUMER_SECRET,
        access_token_key = settings.TWITTER_ACCESS_TOKEN,
        access_token_secret = settings.TWITTER_ACCESS_SECRET
    )
    campaign = Campaign.objects.get(pk=campaignPk)
    
    # Set campaign as running
    campaign.running = True
    campaign.save()
    
    # Get each type of action
    repliedAction = Action.objects.get(type="replied")
    wrongImageNumberAction = Action.objects.get(type="wrong-image-number")
    
    # Perform each queries
    sinceDate = datetime.date.today() - datetime.timedelta(days = 7) # 7 days old tweets max
    curlTwitter = CurlTwitter.CurlTwitter()
    for query in campaign.queries.all():
        for tweet in twitterClient.GetSearch(query.query + " since:"+sinceDate.isoformat(), count = 100, result_type = "recent"):
            # Check if we already seen this tweet
            tweetId = str(tweet.id)
            if (TweetAction.objects.filter(campaign__pk__exact=campaign.pk, tweet__tweet_id__exact=tweetId).count() == 0):
                # Get medias if needed
                if (query.requiredNumberOfImages != None or query.answerWithImage == True):
                    medias = getTweetMedias(twitterClient, tweetId)
                    # Can't access the medias
                    if (medias == False):
                        continue
                    # Check number of images if needed
                    if (query.requiredNumberOfImages is not None and len(medias) != query.requiredNumberOfImages):
                        tweetDB, created = Tweet.objects.get_or_create(tweet_id=tweetId)
                        tweetDB.save()
                        tweetAction = TweetAction()
                        tweetAction.tweet = tweetDB
                        tweetAction.action = wrongImageNumberAction
                        tweetAction.query = query
                        tweetAction.campaign = campaign
                        tweetAction.save()
                        continue
                    # Generate image if needed
                    if (query.answerWithImage == True):
                        imageGenerator = GeneratePreviewImage.GeneratePreviewImage()
                        imageGenerator.generatePreviewImage(medias[0]["media_url"], medias[1]["media_url"])
                # Answer tweet
                answerSentence, shortenedUrls = campaign.generateAnswerSentence(tweet.user.screen_name, tweetId, query.correspondingSentence)
                if (curlTwitter.twitterTweet(answerSentence, tweetId, (settings.BASE_DIR + "/preview.jpg") if query.answerWithImage else None) == True):
                    # Add it to database
                    tweetDB, created = Tweet.objects.get_or_create(tweet_id=tweetId)
                    tweetDB.save()
                    tweetAction = TweetAction()
                    tweetAction.tweet = tweetDB
                    tweetAction.action = repliedAction
                    tweetAction.query = query
                    tweetAction.campaign = campaign
                    if (len(shortenedUrls) > 0):
                        tweetAction.setShortenedUrls(shortenedUrls)
                    tweetAction.save()
                randomSleep(10, 30)
    
    # Set campaign as idle + last run date
    campaign.lastRun = datetime.datetime.now()
    campaign.running = False
    campaign.save()
        