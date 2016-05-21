from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.forms.formsets import all_valid
from extra_views import CreateWithInlinesView, UpdateWithInlinesView

import django, django_rq, datetime, sys, bitly_api

from .models import Tweet, Campaign, TweetAction
from .forms import CampaignForm, QueryFormSet, QueryFormSetUpdate
from .extras import TwitterBot
import main

# Custom mixin to check ownership
def campaign_owner(func):
    def check_and_call(request, *args, **kwargs):
        pk = kwargs["pk"]
        campaign = Campaign.objects.get(pk=pk)
        if (campaign.creator.id != request.user.id): 
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return check_and_call
        
class CampaignOwnerMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CampaignOwnerMixin, cls).as_view(**initkwargs)
        return campaign_owner(view)

# Create your views here.
@login_required
def IndexView(request):
    nbTweets = Tweet.objects.all().count()
    nbRepliedTweets = TweetAction.objects.filter(action__type__exact="replied").count()
    
    return render(request, 'main/index.html', {'nbTweets': nbTweets, 'nbRepliedTweets': nbRepliedTweets})

class CampaignCreate(CreateWithInlinesView):
    model = Campaign
    inlines = [QueryFormSet]
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateWithInlinesView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = None
        
        if django.VERSION >= (1, 6) and self.fields is None and self.form_class is None:
            self.fields = '__all__'  # backward compatible with older versions

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.creator = self.request.user
            form_validated = True
        else:
            form_validated = False

        inlines = self.construct_inlines()

        if all_valid(inlines) and form_validated:
            return self.forms_valid(form, inlines)
        return self.forms_invalid(form, inlines)
    
class CampaignUpdate(CampaignOwnerMixin, UpdateWithInlinesView):
    model = Campaign
    inlines = [QueryFormSetUpdate]
    template_name = 'main/campaign_form_update.html'
    
class CampaignView(CampaignOwnerMixin, DetailView):
    model = Campaign
  
@campaign_owner  
def CampaignSchedule(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    
    scheduler = django_rq.get_scheduler('default')
    job = scheduler.schedule(
        scheduled_time=datetime.datetime.now(),
        func=main.extras.TwitterBot.twitterBot,
        args=[campaign.pk],
        interval=3600,
        timeout=3600,
        repeat=None
    )

    campaign.jobId = job.id
    campaign.save()
    
    return redirect(campaign)

@campaign_owner
def CampaignUnschedule(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    
    scheduler = django_rq.get_scheduler('default')
    scheduler.cancel(campaign.jobId)
    
    campaign.jobId = None
    campaign.save()
    
    return redirect(campaign)
    
def TweetActionReturn(request, tweet_id, action):
    tweet = get_object_or_404(Tweet, tweet_id=tweet_id)
    
    tweetAction = tweet.tweet_actions.all()[0]
    if (action == "clicked" and tweetAction.shortened_urls != None):
        bitly = bitly_api.Connection(access_token = settings.BITLY_TOKEN)
        if (bitly.link_clicks(tweetAction.getShortenedUrls()[0]) > 1):
            tweetAction.clicked = True
    elif (action == "created"):
        tweetAction.prefrCreated = True
    tweetAction.save()
        
    return JsonResponse({'status': 'ok'})
    