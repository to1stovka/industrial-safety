from django import template

register = template.Library()

@register.filter
def times(n: int):
    try:
        n = int(n)
    except Exception:
        n = 0
    return range(1, n + 1)

@register.filter
def ru_mode(value: str):
    mapping = {
        "fulltime": "очная",
        "mixed": "очно-заочная",
        "remote": "дистанционная",
        "individual": "индивидуальная",
    }
    return mapping.get(value, value)

@register.filter
def money(value):
    try:
        s = f"{int(value):,}"
        return s.replace(",", " ")
    except Exception:
        return value

@register.filter
def subtract(a, b):
    """Вычитание в шаблоне: {{ 5|subtract:rating }}"""
    try:
        return int(a) - int(b)
    except Exception:
        return 0

@register.filter
def empty_stars(rating, max_stars=5):
    """Сколько пустых звёзд показать."""
    try:
        r = int(rating)
    except Exception:
        r = 0
    n = max(0, int(max_stars) - r)
    return range(n)
