from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from landing.models import Chunk
import re

register = template.Library()

@register.simple_tag(takes_context=True)
def chunk(context, key, default=''):

    request = context.get('request')
    is_superuser = (
        request and request.user.is_authenticated and request.user.is_superuser
    )

    try:
        chunk_obj = Chunk.objects.get(key=key)
    except Chunk.DoesNotExist:
        chunk_obj = None

    if chunk_obj:
        content = chunk_obj.content or default

        match = re.fullmatch(r"\s*<p>(.*?)</p>\s*", content, flags=re.DOTALL)
        if match:
            content = match.group(1)

        file_url = chunk_obj.file.url if chunk_obj.file else ""
    else:
        content = default
        file_url = ""

    if "<a" in content:
        html = content
    else:
        if not file_url:
            html = content
        else:
            html = f'<a href="{file_url}" target="_blank">{content}</a>'

    if is_superuser:
        edit_url = (
            reverse('admin:landing_chunk_change', args=[chunk_obj.id])
            if chunk_obj else
            f"{reverse('admin:landing_chunk_add')}?key={key}"
        )

        html = f'''
        <div class="chunk-editable"
            style="position: relative; outline: 2px dashed #007bff;
                   outline-offset: 4px; margin: 4px; padding: 2px;">
            {html}
            <a href="{edit_url}" target="_blank"
                class="chunk-edit-btn"
                style="position:absolute; top:-2px; right:-2px;
                       background:#007bff; color:white; padding:4px 8px;
                       font-size:11px; text-decoration:none; border-radius:3px;
                       box-shadow:0 2px 4px rgba(0,0,0,0.2); z-index:1000;">
                ✏️ {key}
            </a>
        </div>
        '''

    return mark_safe(html)
