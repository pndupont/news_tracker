from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# No methods in our new manager should ever receive the whole request object as an argument! 
# (just parts, like request.POST)
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors["first_name"] = 'First Name too short'
        if len(postData['last_name']) < 2:
            errors["last_name"] = 'Last Name too short'
        if len(postData['username']) < 2:
            errors['username'] = 'username too short'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email_invalid'] = 'Please enter a valid email address.'
        all_users = User.objects.all()
        for user in all_users:
            if(postData['email'] == user.email):
                errors['email'] = 'Email address already in use'
            if(postData['username'] == user.username):
                errors['username'] = 'Username already in use'
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if postData['password'] != postData['retype_password']:
            errors['retype_password'] = 'Passwords must match'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length= 255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return f"User Object: ID:({ self.id }) first_name:{ self.first_name } last_name:{ self.last_name } email:{ self.email } username: { self.username } password:{ self.password } Created At:{ self.created_at } Updated At:{ self.updated_at }"