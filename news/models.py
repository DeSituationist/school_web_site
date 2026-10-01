from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
class VKPost(models.Model):
    vk_id = models.BigIntegerField(unique=True)
    text = models.TextField(blank=True)
    created = models.DateTimeField()
    photos = models.JSONField(default=list, blank=True)
    slug = models.SlugField(max_length=250, unique_for_date='created', allow_unicode=True)

    tags = TaggableManager(blank=True)

    def __str__(self):
        return f'Пост с id:{self.vk_id}, создан: {self.created.strftime('%d.%m.%Y')}'

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def get_absolute_url(self):
        return reverse(
            'news:VKpost_detail',
            args = [self.created.year, self.created.month, self.created.day, self.slug]
        )