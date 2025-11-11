from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def render_accordion(context, accordion_id, accordion_title, include_path):
    ctx_dict = getattr(context, "flatten", lambda: dict(context))()

    inner_html = render_to_string(include_path, ctx_dict)

    accordion_html = f"""
    <section class="container py-3">
      <div class="accordion-wrapper">
        <button class="accordion-toggle" id="{accordion_id}">
          {accordion_title}
          <img
            src="/static/landing/img/Vector.svg"
            alt="toggle"
            class="accordion-icon"
          />
        </button>

        <div class="accordion-content" id="{accordion_id}-content">
          {inner_html}
        </div>
      </div>
    </section>
    """
    # __import__('ipdb').set_trace()
    return mark_safe(accordion_html)
