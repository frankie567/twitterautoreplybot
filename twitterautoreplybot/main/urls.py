from django.conf.urls import url

from main.views import IndexView, CampaignCreate, CampaignUpdate, CampaignView, CampaignSchedule, CampaignUnschedule

urlpatterns = [
    url(r'^$', IndexView, name='IndexView'),
    url(r'^campaign/new/$', CampaignCreate.as_view(), name='CampaignCreate'),
    url(r'^campaign/(?P<pk>[0-9]+)/edit$', CampaignUpdate.as_view(), name='CampaignUpdate'),
    url(r'^campaign/(?P<pk>[0-9]+)/$', CampaignView.as_view(), name='CampaignView'),
    url(r'^campaign/(?P<pk>[0-9]+)/schedule/$', CampaignSchedule, name='CampaignSchedule'),
    url(r'^campaign/(?P<pk>[0-9]+)/unschedule/$', CampaignUnschedule, name='CampaignUnschedule')
]