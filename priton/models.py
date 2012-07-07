# -*- coding: utf-8 -*-

from django.db import models
from tinymce import models as tinymce_models

class Person(models.Model):
    short_name = models.CharField(u'Имя', max_length=50)
    full_name = models.CharField(u'Полное имя', max_length=50, blank=True, null=True)
    photo_real = models.URLField(u'Реальное фото')
    comic_picture = models.URLField(u'Комичная картинка')
    photo_descr = models.CharField(u'Описание картинки', max_length=50)
    speech = models.TextField(u'Речь')
    diagnosis = models.TextField(u'Диагноз', blank=True, null=True)
    sort = models.SmallIntegerField(u'Порядок следования', default=0)
    doctor = models.BooleanField(u'Доктор?', default=0)
    
    class Meta:
        verbose_name = u'Человек'
        verbose_name_plural = u'Человеки'
    
    def __unicode__(self):
        return self.short_name
    

class Phrase(models.Model):
    phrase = models.CharField(u'Фраза', max_length=100)
    author = models.ForeignKey(Person)
    big_font = models.BooleanField(default=False)
    bold_font = models.BooleanField(default=False)

    class Meta:
        verbose_name = u'Фраза'
        verbose_name_plural = u'Фразы'
    
    def __unicode__(self):
        return self.phrase


class Essense(models.Model):
    name = models.CharField(u'Имя сущности', max_length=60)
    comics = models.ManyToManyField('Comics', related_name='essenses_list')
    
    class Meta:
        verbose_name = u'Сущность'
        verbose_name_plural = u'Сущности'
    
    def __unicode__(self):
        return self.name


class Comics(models.Model):
    title = models.CharField(u'Название', max_length=60)
    comics_picture_preview = models.URLField(u'Превьюшка картинки комикса')
    comics_picture = models.URLField(u'Картинка комикса')
    #comics_descr = models.TextField(u'Описание комикса')
    comics_descr = tinymce_models.HTMLField()
    participants = models.ManyToManyField(Person, related_name='comics_list')
    sort = models.SmallIntegerField(u'Порядок следования', default=0)
    
    class Meta:
        verbose_name = u'Комикс'
        verbose_name_plural = u'Комиксы'
    
    @models.permalink
    def get_absolute_url(self):
        return ('single_comics', [str(self.id)])
    
    def __unicode__(self):
        return self.title
