import re

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    RegexValidator,
    EmailValidator,
    URLValidator, validate_slug, validate_unicode_slug,
    validate_ipv4_address, validate_ipv6_address, validate_ipv46_address,
    validate_comma_separated_integer_list, int_list_validator,
    MaxValueValidator, MinValueValidator,
    MaxLengthValidator, MinLengthValidator,
    FileExtensionValidator, validate_image_file_extension
)
from django.utils.timezone import now
from django.core.exceptions import ValidationError


def validate_date_of_birth(date_of_birth):
    today = now()
    if (today.year - date_of_birth.year) < 18:
        raise ValidationError('Вы слишком молоды')


class Post(models.Model):

    # Создание кастомного валидатора
    date_of_birth = models.DateField(_("date of birth"), null=True, validators=[
        validate_date_of_birth
    ])

    file = models.FileField(_("file"), upload_to='file/', max_length=100, null=True, validators=[
        validate_image_file_extension, # проверка, что файл должен быть изображением (для работы надо установить расширение в pip pillow)
        #FileExtensionValidator(
        #    allowed_extensions=['xlsx', 'jpg'],
        #    message='Не тот формат файла'
        #)
    ])

    interval_length = models.CharField(_("interval length"), max_length=50, null=True, validators=[
        MaxLengthValidator(
            limit_value=9,
            message='Строка длинее 9 символов'
        ),
        MinLengthValidator(
            limit_value=3,
            message='Строка короче 3 символов'
        )
    ])

    # Проверка значение числа на соответствие интервалу
    interval_value = models.IntegerField(_("interval"), null=True, validators=[
        MaxValueValidator(
            limit_value=42,
            message='Не более 42'
        ),
        MinValueValidator(
            limit_value=11,
            message='Не менее 11'
        )
    ])

    int_list_sep = models.CharField(_('list sep'), max_length=50, null=True, validators=[
        int_list_validator( # тоже что и validate_comma_separated_integer_list, только можно выбрать некоторые параметры
            sep=':', # разделитель между числами
            allow_negative=True, # список может содержать отрицательные значения
            message='Используйте двоеточие между числами'
        )
    ])

    int_list_comma = models.CharField(_('list_comma'), max_length=50, null=True, validators=[
        validate_comma_separated_integer_list # пропускает только записи, состоящие из цифр, разделенных запятой: 3,4,1 и тд
    ])

    # ip = models.GenericIPAddressField(_('ip'), protocol='both', unpack_ipv4=False) # работает на базе TextFild и проверяет, чтобы поле соответствовало 4 или 6 версии
    ip = models.CharField(_('ip'), max_length=50, null=True, validators=[
        validate_ipv4_address, # это RegexValidator, который проверяет, соответствует ли запись ip 4 версии
        validate_ipv6_address, # это RegexValidator, который проверяет, соответствует ли запись ip 6 версии
        validate_ipv46_address # это RegexValidator, который проверяет, соответствует ли запись ip 4 и 6 версии
    ])

    # url = models.SlugField(_('url'), allow_unicode=False) # использует validate_slug, если allow_unicode=False, иначе validate_unicode_slug
    # url = models.URLField(_('url')) # использует URLValidator
    url = models.CharField(_('url'), max_length=50, null=True, validators=[
        URLValidator( # URLValidator - это RegexValidator с некоторыми переданными аргументами
            message='Введите корректный URL',
            schemes=['https'] # ['http', 'https', 'ftp', 'ftps']
        )
    ])

    email = models.CharField(_("emaill"), max_length=50, null=True, validators=[
        # validate_slug, # RegexValidator, который проверяет, что слово состоит только из букв, цифр, _ или -
        # validate_unicode_slug, # RegexValidator, который проверяет, что выражение состоит из unicode букв, цифр, _ или -
        EmailValidator(
            message='Введите корректный email',
            whitelist=['localhost', 'my_local'] # список разрешенных доменов (например, nik@localhost - не вызовет)
        )
    ])

    title = models.CharField(_("title"), max_length=50, validators=[
        RegexValidator(
            regex=r'\.$', # точка в конце
            message='Поставьте точку в конце!',
            code='invalid', # required
            inverse_match=False, # если переопределим в True, то будем смотреть, чтобы точки в конце не было
            flags=re.IGNORECASE
        )
    ])

    name = models.CharField(_("name"), max_length=150)
    slug = models.SlugField(_("url"))

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        db_table = 'posts'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"slug": self.slug})
