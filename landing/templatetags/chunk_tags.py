from django import template
from django.templatetags.static import static
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.urls import reverse
from landing.models import Chunk
import re

register = template.Library()


def _is_superuser(context):
    request = context.get("request")
    return bool(request and request.user.is_authenticated and request.user.is_superuser)


def _get_chunk(key):
    try:
        return Chunk.objects.get(key=str(key))
    except Chunk.DoesNotExist:
        return None


def _strip_single_outer_p(content):
    match = re.fullmatch(r"\s*<p>(.*?)</p>\s*", content or "", flags=re.DOTALL)
    if match:
        return match.group(1)
    return content or ""


def _chunk_edit_url(chunk_obj, key):
    if chunk_obj:
        return reverse("admin:landing_chunk_change", args=[chunk_obj.id])
    return f"{reverse('admin:landing_chunk_add')}?key={key}"


def _wrap_for_superuser(html, edit_url, key, extra_class=""):
    classes = f"chunk-editable {extra_class}".strip()
    return f'''
        <div class="{classes}"
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


def _render_chunk(context, key, default="", preserve_block_markup=False):
    chunk_obj = _get_chunk(key)

    if chunk_obj:
        content = chunk_obj.content or default
        file_url = chunk_obj.file.url if chunk_obj.file else ""
    else:
        content = default
        file_url = ""

    if not preserve_block_markup:
        content = _strip_single_outer_p(content)

    if "<a" in content:
        html = content
    elif file_url:
        html = f'<a href="{file_url}" target="_blank">{content}</a>'
    else:
        html = content

    if _is_superuser(context):
        html = _wrap_for_superuser(html, _chunk_edit_url(chunk_obj, key), key)

    return mark_safe(html)


@register.simple_tag(takes_context=True)
def chunk(context, key, default=""):
    return _render_chunk(context, key, default, preserve_block_markup=False)


class ChunkBlockNode(template.Node):
    def __init__(self, key_expr, nodelist):
        self.key_expr = key_expr
        self.nodelist = nodelist

    def render(self, context):
        key = self.key_expr.resolve(context)
        default = self.nodelist.render(context)
        return _render_chunk(context, key, default, preserve_block_markup=True)


@register.tag(name="chunkblock")
def do_chunkblock(parser, token):
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("chunkblock takes exactly one argument: the chunk key")

    key_expr = parser.compile_filter(bits[1])
    nodelist = parser.parse(("endchunkblock",))
    parser.delete_first_token()
    return ChunkBlockNode(key_expr, nodelist)

def _has_media_html(content):
    """Return True when rich text contains an uploaded/inserted image or another media tag."""
    return bool(
        re.search(
            r"<(img|iframe|video|picture|svg|object|embed)\b",
            content or "",
            flags=re.IGNORECASE,
        )
    )

@register.simple_tag(takes_context=True)
def chunk_image(context, key, default_static_path="", alt="", css_class=""):
    """
    Image chunk.

    Можно заполнить чанк двумя способами:
    1) загрузить файл в поле Chunk.file;
    2) вставить картинку прямо в поле «Содержание» через CKEditor.
    """
    chunk_obj = _get_chunk(key)
    content = (chunk_obj.content or "").strip() if chunk_obj else ""

    class_attr = f' class="{escape(css_class)}"' if css_class else ""

    if _has_media_html(content):
        html = f'<div{class_attr}>{content}</div>' if css_class else content
    else:
        if chunk_obj and chunk_obj.file:
            src = chunk_obj.file.url
        elif default_static_path:
            src = static(default_static_path)
        else:
            src = ""

        if src:
            html = f'<div{class_attr}><img src="{escape(src)}" alt="{escape(alt)}" /></div>'
        elif _is_superuser(context):
            html = f'<div{class_attr}>Изображение не загружено</div>'
        else:
            return ""

    if _is_superuser(context):
        html = _wrap_for_superuser(
            html,
            _chunk_edit_url(chunk_obj, key),
            key,
            extra_class="chunk-editable--image",
        )

    return mark_safe(html)
