from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from .forms import UserForm, UserChangeForm
from .models import User
from movies.models import Genre, Movie, Review
from django.core.paginator import Paginator

# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('movies:index')
    else :
        form = UserForm()

    context = {
        'form':form,
    }
    return render(request, 'accounts/signup.html', context)

def login(request):
    if request.user.is_authenticated:
        print('로그인 되어있습니다.')
        return redirect('movies:index')

    if request.method =="POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')

    else :
        form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

# 카테고리별 영화 가져오기
    popular_movies = Movie.objects.filter(category='popular')
    # 페이지네이션
    popular_paginator = Paginator(popular_movies,9)
    page_number = request.GET.get('page')
    popular_page_obj = popular_paginator.get_page(page_number)
    context = {
        'popular_movies' : popular_movies,
        'popular_page_obj' : popular_page_obj,
    }
    return render(request, 'movies/popular_movie_list.html', context)

@login_required
def profile(request, user_pk):

    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk )
    movies = user.like_movies.all()
    reviews = Review.objects.filter(user = user_pk)
    movie_paginator = Paginator(movies,3)
    review_paginator = Paginator(reviews,3)
    page_number = request.GET.get('page')
    movie_page_obj = movie_paginator.get_page(page_number)
    review_page_obj = review_paginator.get_page(page_number)

    context={
        'person':user,
        'you_liked_movies' : movies,
        'reviews' : reviews,
        'movie_page_obj':movie_page_obj,
        'review_page_obj':review_page_obj,

    }
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, user_pk ):
    you = get_object_or_404(get_user_model(), pk=user_pk )
    me = request.user

    if you != me :
        if you.followers.filter(pk=me.pk).exists():
            you.followers.remove(me)

        else:
            you.followers.add(me)

    return redirect('accounts:profile', you.pk )

@require_POST
@login_required
def delete(request):
    request.user.delete()
    return redirect('movies:index')

def update(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile', request.user.pk)
    else:
        form = UserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)

@login_required
def adminpage(request):
    data = request.COOKIES['data']
    print(data)
    data = list(data.split(","))
    print("result 결과 넘어왔습니다.")
    print(data)
    request_movies = []
    request.append(
        {'movie_pk' : data[0],
    'movie_title' : data[1],
    'movie_original_title' : data[2],
    'movie_requestuser' :data[3]
    }
    )

    paginator = Paginator(request_movies,10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'request_movies':request_movies,
        'page_obj' : page_obj,
       
    }

    return render(request, 'accounts/adminpage.html')

