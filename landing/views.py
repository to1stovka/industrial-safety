from django.shortcuts import render
from news.models import News

def index(request):
    latest_news = News.objects.all().order_by('-created_at')[:3]
    
    context = {
        'latest_news': latest_news,
    }
    return render(request, 'landing/index.html', context)