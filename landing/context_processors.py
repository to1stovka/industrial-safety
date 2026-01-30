from django.conf import settings

def landing_features(request):
    return {"landing_features": getattr(settings, "LANDING_FEATURES", {})}
