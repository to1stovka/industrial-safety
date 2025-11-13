from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ckeditor_uploader.fields import RichTextUploadingField

# Основные направления обучения (главная страница)
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
    

# Отзывы на главной странице (карточки)
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


class Chunk(models.Model):
    """Модель для управления фрагментами контента на сайте"""
    key = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Ключ'
    )
    content = RichTextUploadingField(
        verbose_name='Содержание',
        blank=True
    )
    file = models.FileField(upload_to="chunk_files/", blank=True, null=True, verbose_name="Документ")

    class Meta:
        verbose_name = 'Фрагмент контента'
        verbose_name_plural = 'Фрагменты контента'
        ordering = ['key']

    def __str__(self):
        return self.key

# # ЗАпрос обратного звонка
# class CallbackRequest(models.Model):
#     name = models.CharField("Имя", max_length=100)
#     phone = models.CharField("Телефон", max_length=30)
#     created_at = models.DateTimeField("Дата отправки", auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} ({self.phone})"
#     class Meta:
#         verbose_name = 'Запрос на звонок'
#         verbose_name_plural = 'Запросы на звонок'


# Эксперты на странице НОК (Фото + ФИО)
class Expert(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    photo = models.ImageField("Фото", upload_to="experts/", blank=True, null=True)
    
    def __str__(self):
        return self.full_name
    class Meta: 
        verbose_name = 'Эксперт'
        verbose_name_plural = 'Эксперты'


# # Форма "Оставить заявку" на странице НОК
# class NOCRequest(models.Model):
#     name = models.CharField("Имя", max_length=255)
#     email = models.EmailField("Электронная почта")
#     message = models.TextField("Сообщение", blank=True)
#     file = models.FileField("Прикреплённое заявление", upload_to="noc_requests/", blank=True, null=True)
#     created_at = models.DateTimeField("Дата отправки", auto_now_add=True)

#     class Meta:
#         verbose_name = "Заявка на НОК"
#         verbose_name_plural = "Заявки на НОК"

#     def __str__(self):
#         return f"{self.name} ({self.email})"
    

# Перечень программ, соответствующих направлениям деятельности экспертов
class MinstroyProgram(models.Model):
    order = models.PositiveIntegerField(default=0, help_text="Порядок сортировки")
    title = models.CharField(max_length=300, verbose_name="Название программы")
    description = models.TextField(blank=True, verbose_name="Описание")
    is_active = models.BooleanField(default=True, verbose_name="Показывать на сайте")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Программа Минстроя"
        verbose_name_plural = "Программы Минстроя"
        ordering = ("order", "id")

    def __str__(self):
        return self.title


# Подготовка специалистов по следующим профессиональным квалификациям:
class Qualification(models.Model):
    code = models.CharField(max_length=50, verbose_name="Код квалификации")
    title = models.TextField(verbose_name="Наименование квалификации")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Квалификация"
        verbose_name_plural = "Квалификации"

    def __str__(self):
        return f"{self.code} – {self.title[:60]}"
    

# универсальная форма
class UnifiedRequest(models.Model):

    REQUEST_TYPES = [
        ("callback", "Запрос на звонок"),
        ("noc", "Заявка"),
    ]

    request_type = models.CharField(
        "Тип заявки",
        max_length=20,
        choices=REQUEST_TYPES,
        default="noc",
    )

    name = models.CharField("Имя", max_length=255)
    phone = models.CharField("Телефон", max_length=30, blank=True, null=True)
    email = models.EmailField("Электронная почта", blank=True, null=True)
    message = models.TextField("Сообщение", blank=True, null=True)
    file = models.FileField("Прикреплённый файл",
                            upload_to="requests/", blank=True, null=True)
    created_at = models.DateTimeField("Дата отправки", auto_now_add=True)

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return f"{self.name} ({self.get_request_type_display()})"

