from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CourseDirection(models.Model):
    class Mode(models.TextChoices):
        OCHNAYA = "fulltime", "очная"
        OCHNO_ZAOCH = "mixed", "очно-заочная"
        DISTANT = "remote", "дистанционная"
        INDIV = "individual", "индивидуальная"

    title = models.CharField("Название", max_length=255)
    start_date = models.DateField("Дата начала")
    end_date = models.DateField("Дата конца")
    rating = models.PositiveSmallIntegerField(
        "Рейтинг",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1–5"
    )
    price = models.DecimalField("Цена, ₽", max_digits=10, decimal_places=0)
    mode = models.CharField("Формат обучения", max_length=16, choices=Mode.choices)
    featured = models.BooleanField("Показывать в «Популярных»", default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "-start_date", "-created_at"]
        verbose_name = "Направление"
        verbose_name_plural = "Направления"

    def __str__(self):
        return self.title
    

class Review(models.Model):
    CATEGORY_CHOICES = [
        ('NK', 'Аттестация специалистов НК'),
        ('PB', 'Промышленная безопасность'),
        ('OT', 'Охрана труда'),
        ('EB', 'Электробезопасность'),
    ]

    category = models.CharField('Категория', max_length=50, choices=CATEGORY_CHOICES)
    text = models.TextField('Текст отзыва')
    rating = models.PositiveSmallIntegerField('Рейтинг', default=5)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"{self.get_category_display()}"