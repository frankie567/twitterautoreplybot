from django.forms import ModelForm
from extra_views import InlineFormSet

from .models import Campaign, Query

class CampaignForm(ModelForm):
    class Meta:
        model = Campaign
        fields = ["name", "answerSentence"]
        exclude = ["creator"]
    
class QueryFormSet(InlineFormSet):
    model = Query
    extra = 1
    
class QueryFormSetUpdate(InlineFormSet):
    model = Query
    extra = 0