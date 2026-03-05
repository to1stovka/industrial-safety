from django.db import models
from django.core.validators import FileExtensionValidator


class Accordion(models.Model):
    """
    Аккордеон как сущность: заголовок + код, по которому вставляем на странице.
    """
    code = models.SlugField(max_length=120, unique=True)
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.title} ({self.code})"


class AccordionItem(models.Model):
    """
    Пункт списка: текст + ссылка (URL или файл).
    """
    accordion = models.ForeignKey(Accordion, on_delete=models.CASCADE, related_name="items")

    text = models.CharField(max_length=600)
    order = models.PositiveIntegerField(default=0)

    # Внешняя ссылка
    url = models.URLField(blank=True, null=True)

    # Или файл
    file = models.FileField(
        upload_to="landing/docs/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf", "doc", "docx"])],
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self) -> str:
        return self.text

    @property
    def link(self) -> str | None:
        if self.url:
            return self.url
        if self.file:
            return self.file.url
        return None