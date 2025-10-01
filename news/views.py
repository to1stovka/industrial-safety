from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import News

def news_list(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'news/list.html', {
        'page_obj': page_obj,
        'news_list': page_obj.object_list,
    })

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/detail.html', {'news': news})