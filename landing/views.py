from django.shortcuts import render, redirect
from news.models import News
from landing.models import CourseDirection, Review, CallbackRequest, Expert, MinstroyProgram
from landing.forms import NOCRequestForm
from django.http import JsonResponse, HttpResponse

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



def callback_request(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()

        if name and phone:
            CallbackRequest.objects.create(name=name, phone=phone)

            # AJAX-ответ
            if request.headers.get("x-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": True})

            # fallback для обычной формы
            return HttpResponse("Заявка отправлена успешно")

        # Ошибка валидации
        if request.headers.get("x-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": False, "error": "Некорректные данные"}, status=400)

    # Если не POST — ошибка
    return JsonResponse({"error": "Invalid method"}, status=405)



def nok_page(request):
    experts = Expert.objects.all()

    if request.method == "POST":
        form = NOCRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True})
            return redirect("nok")
        else:
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": False, "errors": form.errors})
    else:
        form = NOCRequestForm()

    return render(request, "landing/nok.html", {"experts": experts, "form": form})


def minstroy_page(request):
    programs = MinstroyProgram.objects.filter(is_active=True).order_by("order", "id")[:4]
    form = NOCRequestForm()
    context = {
        "programs": programs,
        "form": form,
    }
    return render(request, "landing/minstroy.html", context)