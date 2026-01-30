from django.shortcuts import render, redirect
from news.models import News
from landing.models import CourseDirection, Review, Expert, MinstroyProgram, Qualification, UnifiedRequest, ThreedGalleryImage
from landing.forms import CallbackForm, NOCRequestForm
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.http import Http404

def index(request):
    if request.method == "POST":
        form = CallbackForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)

    reviews = Review.objects.all()[:6]
    popular_courses = CourseDirection.objects.filter(featured=True)[:3] or CourseDirection.objects.all()[:3]
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
        form = CallbackForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.request_type = "callback"
            obj.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True})

            return HttpResponse("OK")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    return JsonResponse({"error": "Invalid method"}, status=405)



def nok_page(request):
    experts = Expert.objects.all()
    qualifications = Qualification.objects.order_by("created_at")[:3]

    if request.method == "POST":
        form = NOCRequestForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.request_type = "noc"
            obj.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"success": True})

            return redirect("nok")

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": False, "errors": form.errors})

    else:
        form = NOCRequestForm()

    return render(
        request,
        "landing/nok.html",
        {"experts": experts, "form": form, "qualifications": qualifications}
    )


def prep_request(request):
    if request.method == "POST":
        req_type = request.POST.get("request_type")

        if req_type not in ("prep_expert", "prep_specialist"):
            return JsonResponse({"success": False, "error": "Invalid type"}, status=400)

        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        if not (name and phone and email):
            return JsonResponse({"success": False, "error": "Missing fields"}, status=400)

        UnifiedRequest.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message,
            request_type=req_type
        )

        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid method"}, status=405)


def minstroy_page(request):
    programs = MinstroyProgram.objects.all().order_by("id")[:4]
    form = NOCRequestForm()
    context = {
        "programs": programs,
        "form": form,
    }
    return render(request, "landing/minstroy.html", context)

def minstroy_list(request):
    programs = MinstroyProgram.objects.all().order_by("id")
    paginator = Paginator(programs, 14)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "landing/minstroy_list.html", {"page_obj": page_obj})

def exam(request):
    qs = MinstroyProgram.objects.all()
    fields = {f.name for f in MinstroyProgram._meta.get_fields()}

    if "is_active" in fields:
        qs = qs.filter(is_active=True)
    if "order" in fields:
        qs = qs.order_by("order", "id")
    else:
        qs = qs.order_by("id")

    programs = qs[:4]
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

def threed(request):
    if not settings.LANDING_FEATURES.get("ENABLE_THREED_PAGE", True):
        raise Http404
    gallery = ThreedGalleryImage.objects.all()
    form = NOCRequestForm()
    context = {
        'gallery': gallery,
        "form": form,
    }
    return render(request, 'landing/threed.html', context)
