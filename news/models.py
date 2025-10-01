from django.db import models

class News(models.Model):
    CATEGORY_CHOICES = [
        ("seminar", "Семинар"),
        ("career", "Карьера"),
    ]

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(
        upload_to="news/images",
        blank=True,
        null=True,
        verbose_name="Изображение"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        blank=True,
        null=True,
        verbose_name="Категория"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def russian_date(self):
        months = {
            1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
            5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
            9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
        }
        
        from django.utils import timezone
        value = self.created_at
        if timezone.is_aware(value):
            value = timezone.localtime(value)
        
        day = value.day
        month = months[value.month]
        year = value.year
        
        return f"{day} {month} {year}г."