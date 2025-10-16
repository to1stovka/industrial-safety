from django.shortcuts import render
from news.models import News
from landing.models import CourseDirection, Review

def index(request):
    reviews = Review.objects.all()[:6]

    popular_courses = CourseDirection.objects.filter(featured=True)[:3]

    # Если нет отмеченных как featured — берём просто первые три
    if not popular_courses:
        popular_courses = CourseDirection.objects.all()[:3]
    latest_news = News.objects.all().order_by('-created_at')[:3]

    context = {
        'latest_news': latest_news,
        'popular_courses': popular_courses,
        'reviews': reviews
    }
    return render(request, 'landing/index.html', context)

def contact(request):
    return render(request, 'landing/contact.html')