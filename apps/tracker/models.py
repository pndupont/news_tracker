from django.db import models
import re

URL_REGEX = re.compile(r'^https://')

class NewsManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if not URL_REGEX.match(postData['url']):
            errors['url'] = 'please enter a valid url'
        if len(postData['list_name']) == 0:
            errors['list_name'] = 'News List cannot be blank'
        if len(postData['list_name']) < 3:
            errors['list_name'] = 'News List must be at least 3 characters'
        return errors

class News(models.Model):
    users = models.ManyToManyField('login.User', related_name='news')
    list_name = models.CharField(max_length=255)
    site = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = NewsManager()
    def __repr__(self):
        return f"News Object: ID:({ self.id }) list_name:{ self.list_name } site:{ self.site } Created At:{ self.created_at } Updated At:{ self.updated_at }"


