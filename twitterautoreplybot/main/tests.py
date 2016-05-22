from django.test import TestCase
from main.models import Campaign

# Campaign model tests
class CampaignTestCase(TestCase):
    def setUp(self):
        Campaign.objects.create(
            name = "Test campaign",
            answerSentence = "Username : %twitterUsername% / Magic word : %magicWord% / Tweet id : %tweetId%"
        )
            
    def test_generateAnswerSentence(self):
        campaign_test = Campaign.objects.get(name = "Test campaign")
        self.assertEqual(
            campaign_test.generateAnswerSentence("TwitterUser", "1234", "MagicWord"),
            ("Username : TwitterUser / Magic word : MagicWord / Tweet id : 1234", [])
        )
