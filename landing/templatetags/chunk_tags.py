from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
from landing.models import Chunk

register = template.Library()


@register.simple_tag(takes_context=True)
def chunk(context, key, default=''):
    """
    Использование: {% chunk 'key_name' %}
    или с дефолтным значением: {% chunk 'key_name' 'default content' %}
    """
    request = context.get('request')
    is_superuser = request and request.user.is_authenticated and request.user.is_superuser

    try:
        chunk_obj = Chunk.objects.get(key=key)
        content = chunk_obj.content if chunk_obj.content else default
        chunk_id = chunk_obj.id
        chunk_exists = True
    except Chunk.DoesNotExist:
        content = default
        chunk_id = None
        chunk_exists = False

    if is_superuser:
        if chunk_exists:
            edit_url = reverse('admin:landing_chunk_change', args=[chunk_id])
        else:
            edit_url = f"{reverse('admin:landing_chunk_add')}?key={key}"

        wrapped_content = f'''
        <div class="chunk-editable" style="position: relative; outline: 2px dashed #007bff; outline-offset: 4px; margin: 4px;">
            {content}
            <a href="{edit_url}" target="_blank" class="chunk-edit-btn" style="position: absolute; top: -2px; right: -2px; background: #007bff; color: white; padding: 4px 8px; font-size: 11px; text-decoration: none; border-radius: 3px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); z-index: 1000; font-family: sans-serif;">
                ✏️ {key}
            </a>
        </div>
        '''
        return mark_safe(wrapped_content)

    return mark_safe(content)
