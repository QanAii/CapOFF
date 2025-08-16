from django.db import models


class BannerLocationEnum(models.TextChoices):
    INDEX_HEAD = ('index_head', 'Сверху главной страницы')
    INDEX_MIDDLE = ('index_middle', 'По середине в главной странице')
    CATALOG_HEAD = ('catalog_head', 'Сверху каталога')
