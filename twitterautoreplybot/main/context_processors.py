from .models import Campaign

def campaigns_processor(request):
    campaigns = Campaign.objects.all()            
    return {'campaigns': campaigns}
    