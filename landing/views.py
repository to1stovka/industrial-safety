from django.shortcuts import render, redirect
from news.models import News
from landing.models import CourseDirection, Review, Expert, MinstroyProgram, Qualification, UnifiedRequest, ThreedGalleryImage, NocPreparationDirection
from landing.forms import CallbackForm, NOCRequestForm
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.http import Http404
from django.views.decorators.http import require_POST
from django.urls import reverse
from datetime import datetime

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
    directions = NocPreparationDirection.objects.filter(is_active=True).order_by("kind", "id")
    return render(request, "landing/exam.html", {
        "programs": programs,
        "qualifications": qualifications,
        "directions": directions,
    })



def qualifications_list(request):
    q = (request.GET.get("q") or "").strip()
    page_number = request.GET.get("page")

    base_qs = Qualification.objects.all().order_by("code")

    if q:
        q_cf = q.casefold()

        items = [
            obj for obj in base_qs
            if q_cf in (obj.code or "").casefold()
            or q_cf in (obj.title or "").casefold()
        ]

        paginator = Paginator(items, 12)
        page_obj = paginator.get_page(page_number)
        total = len(items)
    else:
        paginator = Paginator(base_qs, 12)
        page_obj = paginator.get_page(page_number)
        total = base_qs.count()

    return render(request, "landing/qualifications_list.html", {
        "page_obj": page_obj,
        "q": q,
        "total": total,
    })

from io import BytesIO
from pathlib import Path
from docxtpl import DocxTemplate
from collections import defaultdict
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

CHECKED = "☑"
UNCHECKED = "☐"


def _p(cell, text, bold=False, center=False, size=10):
    p = cell.paragraphs[0] if cell.paragraphs else cell.add_paragraph()
    run = p.add_run(text or "")
    run.bold = bold
    run.font.size = Pt(size)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return p


def build_auditors_table(subdoc, selected_dirs):
    auditors = [d for d in selected_dirs if d.kind == "auditor"]
    if not auditors:
        subdoc.add_paragraph("Аудиторы: не выбрано.")
        return subdoc

    # Таблица: № | Наименование | отметка | Код проф. квалиф.
    t = subdoc.add_table(rows=1, cols=4)
    t.style = "Table Grid"

    hdr = t.rows[0].cells
    _p(hdr[0], "№", bold=True, center=True)
    _p(hdr[1], "Наименование ОПО", bold=True, center=True)
    _p(hdr[2], "", bold=True, center=True)
    _p(hdr[3], "Код проф. квалиф.", bold=True, center=True)

    for i, d in enumerate(auditors, start=1):
        row = t.add_row().cells
        _p(row[0], str(i), center=True)
        _p(row[1], d.title)
        _p(row[2], CHECKED, center=True, size=14)  # выбран — значит отмечен
        _p(row[3], d.code, center=True)

    return subdoc


def build_experts_table(subdoc, selected_dirs):
    experts = [d for d in selected_dirs if d.kind == "expert"]
    if not experts:
        subdoc.add_paragraph("Эксперты: не выбрано.")
        return subdoc

    # группируем по "Наименование ОПО" (title)
    # внутри — по track (TU/ZS) и category (1/2/3)
    grouped = defaultdict(list)
    for d in experts:
        grouped[d.title].append(d)

    # какие категории вообще выбраны (чтобы колонки были только по ним)
    cats = sorted({d.category for d in experts if d.category is not None})
    # если вдруг category не заполнена, можно fallback:
    if not cats:
        cats = [1, 2, 3]  # или [] — но таблица станет пустой

    # Таблица: № | Наименование ОПО | ТУ/ЗС | (Категории...)
    cols = 3 + len(cats)
    t = subdoc.add_table(rows=1, cols=cols)
    t.style = "Table Grid"

    # Header
    hdr = t.rows[0].cells
    _p(hdr[0], "№", bold=True, center=True)
    _p(hdr[1], "Наименование ОПО", bold=True, center=True)
    _p(hdr[2], "ТУ/ЗС", bold=True, center=True)
    for j, cat in enumerate(cats):
        _p(hdr[3 + j], f"Категория, Код", bold=True, center=True)

    # Rows: по каждому ОПО делаем 2 строки (ТУ и ЗС) только если они есть среди выбранных
    # (если выбран только ТУ — будет 1 строка)
    idx = 1
    for title, items in grouped.items():
        # map: track -> {cat -> dir}
        by_track = defaultdict(dict)
        for d in items:
            by_track[d.track][d.category] = d

        tracks_order = []
        if "TU" in by_track: tracks_order.append("TU")
        if "ZS" in by_track: tracks_order.append("ZS")

        first_row_for_title = True
        for track in tracks_order:
            row = t.add_row().cells

            if first_row_for_title:
                _p(row[0], str(idx), center=True)
                _p(row[1], title)
                first_row_for_title = False
                idx += 1
            else:
                _p(row[0], "")
                _p(row[1], "")

            _p(row[2], "ТУ" if track == "TU" else "ЗС", center=True)

            for j, cat in enumerate(cats):
                d = by_track.get(track, {}).get(cat)
                if d:
                    # в клетке: код + чекбокс (чекбокс отмечен, потому что это выбранное направление)
                    _p(row[3 + j], f"Категория {cat}\nКод {d.code}\n{CHECKED}", center=True)
                else:
                    # категории нет среди выбранных для этой строки — можно пусто
                    _p(row[3 + j], "", center=True)

    return subdoc


@require_POST
def noc_exam_print(request):
    def g(name):
        return (request.POST.get(name) or "").strip()

    # ---- валидация (как у тебя) ----
    applicant_type = g("applicant_type")
    candidate_fio = g("candidate_fio")
    candidate_phone = g("candidate_phone")
    candidate_email = g("candidate_email")

    errors = {}
    if applicant_type not in ("company", "person"):
        errors["applicant_type"] = "Выберите тип заявителя"
    if not candidate_fio:
        errors["candidate_fio"] = "Укажите ФИО"
    if not candidate_phone:
        errors["candidate_phone"] = "Укажите телефон"
    if not candidate_email:
        errors["candidate_email"] = "Укажите email"

    birth_date_raw = g("birth_date")
    birth_date = ""
    if birth_date_raw:
        try:
            birth_date = datetime.strptime(birth_date_raw, "%Y-%m-%d").date().strftime("%d.%m.%Y")
        except ValueError:
            errors["birth_date"] = "Неверный формат даты"

    if errors:
        return JsonResponse({"success": False, "errors": errors}, status=400)

    # ---- направления ----

    direction_ids = request.POST.getlist("directions")
    selected_dirs = list(NocPreparationDirection.objects.filter(id__in=direction_ids)) if direction_ids else []

    tpl_path = Path(settings.BASE_DIR) / "landing" / "docx_templates" / "noc_request_template.docx"
    doc = DocxTemplate(str(tpl_path))

    experts_subdoc = doc.new_subdoc()
    build_experts_table(experts_subdoc, selected_dirs)

    auditors_subdoc = doc.new_subdoc()
    build_auditors_table(auditors_subdoc, selected_dirs)

    edo_enabled = (g("edo_enabled") == "1")

    context = {
        "today": datetime.now().strftime("%d.%m.%Y"),
        "applicant_type_label": "Предприятие-плательщик" if applicant_type == "company" else "Частное лицо",

        "applicant_name": g("applicant_name"),
        "contacts": g("contacts"),
        "legal_address": g("legal_address"),
        "postal_address": g("postal_address"),

        "edo_enabled_label": "Да" if edo_enabled else "Нет",
        "edo_service": g("edo_service") if edo_enabled else "",
        "edo_yes": "☑" if edo_enabled else "☐",
        "edo_no":  "☐" if edo_enabled else "☑",

        # реквизиты
        "rs": g("rs"),
        "bank": g("bank"),
        "ks": g("ks"),
        "inn": g("inn"),
        "kpp": g("kpp"),
        "bik": g("bik"),
        "okpo": g("okpo"),
        "okved": g("okved"),

        # соискатель
        "candidate_fio": candidate_fio,
        "birth_date": birth_date,
        "position": g("position"),
        "residence": g("residence"),
        "passport_data": g("passport_data"),
        "candidate_phone": candidate_phone,
        "candidate_email": candidate_email,

        # контактное лицо
        "contact_fio": g("contact_fio"),
        "contact_phone": g("contact_phone"),
        "contact_email": g("contact_email"),
        "comment": g("comment"),

        # списки
        "experts_table": experts_subdoc,
        "auditors_table": auditors_subdoc,
    }

    doc.render(context)

    buff = BytesIO()
    doc.save(buff)
    buff.seek(0)

    filename = f"zayavka-nok-{datetime.now():%Y-%m-%d}.docx"
    resp = HttpResponse(
        buff.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    resp["Content-Disposition"] = f"attachment; filename*=UTF-8''{filename}"
    return resp

# приём подписанной заявки НОК
@require_POST
def noc_exam_upload(request):
    file = request.FILES.get("file")
    comment = (request.POST.get("comment") or "").strip()

    errors = {}
    if not file:
        errors["file"] = "Прикрепите файл подписанной заявки"

    if errors:
        return JsonResponse({"success": False, "errors": errors}, status=400)

    UnifiedRequest.objects.create(
      request_type="noc_signed",
      name="Подписанная заявка (НОК)",
      message=comment,
      file=file,
    )

    return JsonResponse({"success": True})


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
