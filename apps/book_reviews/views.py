# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.db.models import Count
import bcrypt
from models import User, Book, Author, Review

def index(request):
    return render(request, 'book_reviews/index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.required_fields_validator(request.POST)
        if not errors:
            errors = User.objects.new_user_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            request.session['message_location']='registration'
            return redirect('/')
        else:
            name = request.POST['name']
            alias = request.POST['alias']
            email = request.POST['email'] 
            password = request.POST['password']
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            new_user = User.objects.create(name=name, alias=alias, email=email, password_hash=password_hash)
            id = new_user.id
            request.session['logged_in_id']=id
            return redirect('/books')
    else:
        return redirect('/')

def authenticate(request):
    if request.method == 'POST':
        errors = User.objects.required_fields_validator(request.POST)
        if not errors:
            errors = User.objects.login_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            request.session['message_location']='login'
            return redirect('/')
        else:
            email = request.POST['email']
            user = User.objects.get(email=email)
            id = user.id
            request.session['logged_in_id']=id
            return redirect('/books')
    else:
        return redirect('/')

def home(request):
    id = request.session['logged_in_id']
    user = User.objects.get(id=id)
    last_three_reviews = Review.objects.order_by('-id')[:3]
    books = Book.objects.order_by('title')
    context = {
        'user': user,
        'reviews': last_three_reviews,
        'books': books,
    }
    return render(request, 'book_reviews/home.html', context)

def add(request):
    authors = Author.objects.order_by('name')
    return render(request, 'book_reviews/add.html',{'authors':authors})

def create(request):
    if request.method == 'POST':
        print request.POST
        errors = Book.objects.review_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/add')
        else:
            title = request.POST['title']
            try:
                author_name = request.POST['existing_author']
            except:
                author_name = request.POST['author']
            content = request.POST['content']
            rating = request.POST['rating']
            user_id = request.session['logged_in_id']
            user = User.objects.get(id=user_id)
            try: 
                author = Author.objects.get(name=author_name)
            except:
                author = Author.objects.create(name=author_name)
            try:
                book = Book.objects.get(title=title)
            except:
                book = Book.objects.create(title=title, author=author)
            Review.objects.create(content=content, rating=rating, book=book, user=user)
            book_id = book.id
            return redirect('/books/{}'.format(book_id))
    else:
        return redirect('/add')

def read_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except:
        return redirect('/books')
    id = request.session['logged_in_id']
    user = User.objects.get(id=id)
    book_reviews = Review.objects.filter(book = book).order_by('-id')
    context = {
        'book': book,
        'book_reviews': book_reviews,
        'user': user
    }
    return render(request, 'book_reviews/book.html', context)

def read_user(request, id):
    try: 
        user = User.objects.annotate(review_count=Count('reviews')).get(id=id)
    except:
        return redirect('/books')
    user_reviews = Book.objects.filter(reviews__user__id=id).distinct()
    print user_reviews
    context = {
        'user': user,
        'user_reviews': user_reviews,
    }
    return render(request, 'book_reviews/user.html', context)

def logout(request):
    del request.session['logged_in_id']
    request.session.modified = True
    return redirect('/')

def destroy_review(request, id):
    try:
        review = Review.objects.get(id=id)
    except: 
        return redirect('/books')
    book = review.book
    review.delete()
    return redirect('/books/{}'.format(book.id))