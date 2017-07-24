# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class ValidationsManager(models.Manager):
    def required_fields_validator(self, post_data):
        errors = {}
        for field in post_data:
            if len(post_data[field]) == 0:
                errors['required'] = 'All fields are required'
                return errors
    
    def login_validator(self, post_data):
        errors = {}
        # valid e-mail first
        if not EMAIL_REGEX.match(post_data['email']) :
            errors['invalid_email'] = 'Email address is invalid'
            return errors
        # e-mail registered second
        try:
            email = post_data['email']
            user = User.objects.get(email=email)
        except:
            errors['email_not_registered'] = 'Email not recognized.  Please register an account.'
            return errors
        # check password third
        entered_pw = post_data['password']
        user_hash = user.password_hash
        if not bcrypt.checkpw(entered_pw.encode(), user_hash.encode()):
            errors['incorrect_password'] = 'Password incorrect.  Please try again!'
        return errors
        

    def new_user_validator(self, post_data):
        errors = {}
        if not EMAIL_REGEX.match(post_data['email']) :
            errors['invalid_email'] = 'Email address is invalid'
        try:
            User.objects.get(email = post_data['email'])
            errors['already_user'] = 'Email address already registered.  Try logging in'
        except:
            pass
        if len(post_data['password']) < 8:
            errors['password_length'] = 'Password should be at least 8 characters'
        if post_data['password'] != post_data['confirm']:
            errors['password_match'] = 'Passwords do not match'
        return errors

    def review_validator(self, post_data):
        errors = {}
        if len(post_data['title']) < 1 or (len(post_data['author']) < 1 and len(post_data['existing_author']) < 1) or len(post_data['content']) < 1:
            errors['required'] = 'All fields are required'
        if len(post_data['content']) > 1000:
            errors['review_length'] = 'Please keep reviews to 1000 characters or less'
        return errors
    

class User(models.Model):
    name = models.CharField(max_length=256)
    alias = models.CharField(max_length=32)
    email = models.CharField(max_length=256)
    password_hash = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidationsManager()

class Author(models.Model):
    name = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidationsManager()

class Book(models.Model):
    title = models.TextField()
    author = models.ForeignKey(Author, related_name='books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidationsManager()

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    book = models.ForeignKey(Book, related_name='reviews')
    user = models.ForeignKey(User, related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidationsManager()
