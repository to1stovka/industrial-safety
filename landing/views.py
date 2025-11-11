from django.shortcuts import render, redirect
from news.models import News
from landing.models import CourseDirection, Review, CallbackRequest, Expert, MinstroyProgram, Qualification
from landing.forms import NOCRequestForm
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator

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
    qualifications = Qualification.objects.order_by("created_at")[:3]

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

    return render(request, "landing/nok.html", {"experts": experts, "form": form, "qualifications": qualifications})


def minstroy_page(request):
    programs = MinstroyProgram.objects.filter(is_active=True).order_by("order", "id")[:4]
    form = NOCRequestForm()
    context = {
        "programs": programs,
        "form": form,
    }
    return render(request, "landing/minstroy.html", context)

def minstroy_list(request):
    programs = MinstroyProgram.objects.all().order_by("order")
    paginator = Paginator(programs, 14)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "landing/minstroy_list.html", {"page_obj": page_obj})

def exam(request):
    programs = MinstroyProgram.objects.filter(is_active=True).order_by("order", "id")[:4]
    qualifications = Qualification.objects.order_by("created_at")[:3]
    return render(request, "landing/exam.html", {"programs": programs, "qualifications": qualifications})


def qualifications_list(request):
    qualifications = Qualification.objects.order_by("code")
    paginator = Paginator(qualifications, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "landing/qualifications_list.html", {"page_obj": page_obj})


def attestation(request):
    return render(request, 'landing/attestation.html')

def TD(request):
    form = NOCRequestForm()
    context = {
        "form": form,
        "page": "TD",
    }
    return render(request, 'landing/TD.html', context)

def IO(request):
    form = NOCRequestForm()
    context = {
        "form": form,
        "page": "IO",
    }
    return render(request, 'landing/TD.html', context)

def NK(request):
    form = NOCRequestForm()
    context = {
        "form": form,
        "page": "NK",
    }
    return render(request, 'landing/TD.html', context)

def docs(request):
    return render(request, 'landing/docs.html')

def preparation(request):
    return render(request, 'landing/preparation.html')

def safety(request):
    return render(request, 'landing/safety.html')