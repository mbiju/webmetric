# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify
from django.core.urlresolvers import reverse

# Create your models here.


def image_loc(instance, filename):
    title = instance.title
    slug = slugify(title)
    basename, file_extension = filename.split(".")
    new_filename = "%s-%s.%s" %(slug, instance.id, file_extension)
    return "categories/%s/%s" %(slug, new_filename)


class Product(models.Model):
    title = models.CharField(max_length=120)
    image = models.FileField(upload_to=image_loc, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20, blank=True, null=True)
    desc = models.TextField(verbose_name='Description')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("products:product_detail", kwargs={"pk": self.pk })

