from django import template
from django.utils.safestring import mark_safe
from site_content.models import Accordion

register = template.Library()


@register.inclusion_tag("landing/partials/accordion_db.html", takes_context=True)
def render_accordion_db(context, accordion_id, accordion_code, fallback_title=None):
    """
    Пример:
    {% render_accordion_db "normative-toggle" "normative_nok" %}
    """
    acc = (
        Accordion.objects
        .prefetch_related("items")
        .filter(code=accordion_code)
        .first()
    )

    title = fallback_title or (acc.title if acc else "")
    items = acc.items.all() if acc else []

    return {
        "accordion_id": accordion_id,
        "accordion_content_id": f"{accordion_id}-content",
        "accordion_title": title,
        "accordion_items": items,
        # пробросим request, если понадобится
        "request": context.get("request"),
    }