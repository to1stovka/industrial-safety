from django.shortcuts import render, redirect
from news.models import News
from landing.models import CourseDirection, Review, CallbackRequest, Expert

def index(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()

        if name and phone:
            CallbackRequest.objects.create(name=name, phone=phone)
        return redirect(request.path)
    reviews = Review.objects.all()[:6]

    popular_courses = CourseDirection.objects.filter(featured=True)[:3]

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

from .models import CallbackRequest

def callback_request(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()

        if name and phone:
            CallbackRequest.objects.create(name=name, phone=phone)

from django.shortcuts import render, redirect
from .models import Expert

def nok_page(request):
    experts = Expert.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        # добавить сохранение в модель CallbackRequest
        print("Заявка:", name, phone, message)
        return redirect("nok")

    return render(request, "landing/nok.html", {"experts": experts})
