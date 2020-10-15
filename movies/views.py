from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Comment, Review, Genre
from accounts.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .forms import MovieForm, CommentForm,ReviewForm
from django.contrib.auth import get_user_model
from django.contrib import messages
import requests
from django.db.models import Q, Avg
from movies.moviehereList import *
from django.conf import settings
from django.db.models import Func

def index(request):
    print(request)
    return render(request, 'movies/index.html')


def detail(request, movie_pk):
    movies = Movie.objects.all()
    movie = get_object_or_404(Movie, pk=movie_pk)
    API_KEY = settings.YOUTUBE_SECRET_KEY_API
    print(API_KEY)
    context = {
        'movie' : movie,
        'movies':movies,
        'API_KEY':API_KEY
    }
    return render(request, 'movies/detail.html',context)

def nowplaying(request):
    # 현재 상영작 영화 가져오기

    nowplaying_movies = Movie.objects.filter(category='nowplaying').order_by('-release_date')

    # 페이지네이션
    nowplaying_paginator = Paginator(nowplaying_movies,9)

    page_number = request.GET.get('page')

    nowplaying_page_obj = nowplaying_paginator.get_page(page_number)

    context = {

        'nowplaying_movies' : nowplaying_movies,

        'nowplaying_page_obj' : nowplaying_page_obj,
    }
    return render(request, 'movies/nowplaying_movie_list.html', context)


def popular(request):
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

def upcoming(request):
    # 카테고리별 영화 가져오기
    upcoming_movies = Movie.objects.filter(category='upcoming')

    # 페이지네이션
    upcoming_paginator = Paginator(upcoming_movies,9)
    page_number = request.GET.get('page')
    upcoming_page_obj = upcoming_paginator.get_page(page_number)
    context = {
        'upcoming_movies' : upcoming_movies,
        'upcoming_page_obj' : upcoming_page_obj,
    }
    return render(request, 'movies/upcoming_movie_list.html', context)

def top_ranked(request):
    # 탑 랭킹 영화 가져오기
    top_ranked_movies = Movie.objects.filter(category='top-ranked').order_by('-vote_average')
    # 페이지네이션
    top_ranked_paginator = Paginator(top_ranked_movies,9)
    page_number = request.GET.get('page')
    top_ranked_page_obj = top_ranked_paginator.get_page(page_number)
    context = {
        'top_ranked_movies' : top_ranked_movies,
        'top_ranked_page_obj' : top_ranked_page_obj,
    }
    return render(request, 'movies/top_ranked_movie_list.html', context)


@login_required
def movie_like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if user.is_authenticated :
        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            liked = False # 좋아요 눌렀는지 안눌렀는지 확인로직
        else:
            movie.like_users.add(user)
            liked = True

    else :
        return redirect('accounts:login')
    context = {
        'liked': liked,
        'count' : movie.like_users.count(),
    }
    return JsonResponse(context)


def review_list(request,movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    reviews = Review.objects.filter(movie = movie_pk)

    # 페이지네이션
    paginator = Paginator(reviews,10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    class Round(Func):
      function = 'ROUND'
      arity = 2

    moviehererank = Review.objects.filter(user = request.user).aggregate(Avg('rank'))['rank__avg']
    # moviehererank = Review.objects.filter(movie=movie_pk).aggregate(Round(Avg('rank'),1))['rank__avg']

    print(moviehererank)
    context = {
        'reviews': reviews,
        'movie': movie,
        'moviehererank':moviehererank,
        'page_obj' : page_obj,
    }
    return render(request, 'movies/review_list.html', context)

@login_required
def review_create(request, movie_pk ):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()

            return redirect('movies:review_list', movie.pk)
    else:
        review_form = ReviewForm()
    context = {
        'review_form' : review_form,
        'movie':movie,

    }
    return render(request,'movies/form.html',context)

@login_required
def review_detail(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)
    comment_form = CommentForm()
    context = {
        'movie':movie,
        'review':review,
        'comment_form' : comment_form,
    }
    return render(request, 'movies/review_detail.html', context)

@login_required
def review_update(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if review.user != request.user:
            return redirect('movies:review_detail', movie.pk, review.pk)
        else :
            if request.method == "POST":
                review_form = ReviewForm(request.POST, instance=review)
                if review_form.is_valid():
                    updated = review_form.save()
                    return redirect('movies:review_detail', movie.pk, updated.pk)
            else :
                review_form = ReviewForm(instance=review)
            context = {
                'movie':movie,
                'review_form' : review_form
            }
            return render(request,'movies/form.html', context)
    else:
        return redirect('accounts:login')


@login_required
@require_POST
def review_delete(request, movie_pk, review_pk):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, pk=review_pk)
        if review.user != request.user:
            return redirect('movies:review_detail', review.pk)
        else:
            if request.method == "POST":
                review = get_object_or_404(Review, pk=review_pk)
                review.delete()
                return redirect('movies:review_list', movie_pk)
            else :
                return redirect('movies:review_detail', movie_pk, review.pk)

    else:
        return redirect('accounts:login')


@login_required
def comment_create(request, movie_pk, review_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()

        return redirect('movies:review_detail', movie.pk, review.pk)

@require_POST
def comment_delete(request, movie_pk, review_pk, comment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.user.is_authenticated:
        if request.method == "POST":
            comment = get_object_or_404(Comment, pk=comment_pk)
            if comment.user == request.user:
                comment.delete()
        return redirect('movies:review_detail', movie.pk, review_pk)
    else :
        return redirect('accounts:login')

def review_like(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user.is_authenticated :
        if review.like_users.filter(id=request.user.pk).exists():
            review.like_users.remove(request.user)
        else:
            review.like_users.add(request.user)

    else :
        return redirect('accounts:login')

    return redirect('movies:review_detail', movie_pk, review_pk)

@login_required
#수정 기능
def movie_update(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if not request.user.is_superuser:
        return redirect('movies:index')

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)

        if form.is_valid():
            movie = form.save()
            return redirect('movies:index')
    else:
        form = MovieForm(instance=movie)
        messages.warning(request, "올바르게 작성해주세요")

    context = {
        'form': form
    }
    return render(request, 'movies/movie_form.html', context)

@require_POST
def movie_delete(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie.delete()
    return redirect('movies:index')

@login_required
def movie_create(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = MovieForm()
    context = {
        'form' : form,

    }
    return render(request, 'movies/movie_form.html', context)


def recommendation(request):
    if request.user.is_authenticated:
        context = {
            'message' : '',
            }

        return render(request,'movies/recommendation.html/',context)
        
    else:
        return redirect('accounts:login')


def movieherechoice(request):
    messages.warning(request, "한 질문에 1개씩만 선택해주세요.")
    return render(request, 'movies/movieherechoice.html')

def moviehereresult(request):
    data = request.COOKIES['data']
    print(data)
    data = list(data.split(","))
    print("result 결과 넘어왔습니다.")
    print(data)

    chooseWhom = data[0]
    chooseFeeling = data[1]


    Whom = ''
    Feeling = ''
    whom_mean = {'whom_family':'가족과','whom_sibling':'남매들과','whom_coworker':'직장 상사 혹은 동료와', 'whom_ssum':'썸남 썸녀 혹은 사랑하는 사람과', 'whom_friends':'칭구들과','whom_solo':'빛이나는 홀로'}
    feeling_mean = {'feeling_broken':'사랑했을때','feeling_love':'사랑할때','feeling_angry':'화가날때','feeling_imagine':'상상 속에 빠지고 싶을 때','feeling_mung':'멍때릴때','feeling_healing':'힐링할때','feeling_groomy':'우울할때','feeling_action':'액션이 땡길떄','feeling_scary':'오싹오싹 할 때  '}

    # 알고리즘
    whom_list = []
    feeling_list = []
    for key,val_list in whom.items():
        if chooseWhom == key:
            whom_list = val_list
            Whom = whom_mean[key]
            print(Whom)

    for key,val_list in feeling.items():
        if chooseFeeling == key:
            feeling_list = val_list
            Feeling = feeling_mean[key]
            print(Feeling)

    common = set(whom_list).intersection(feeling_list)

    # common = list(set(whom_list).intersection(feeling_list))
    print(len(common))

    w_idx = 0
    f_idx = 0
    while len(common) < 9 :
        if f_idx < len(feeling_list) :
            common.add(feeling_list[f_idx])
            f_idx+=1
        else :
            common.add(whom_list[w_idx])
            w_idx+=1

    common = list(common)[:9]

    recommend_movies = []
    # 영화 id로 정보를 가져오기 위해
    for searchingid in common :

        search_url = f'https://api.themoviedb.org/3/movie/{searchingid}?api_key={settings.TMDB_SECRET_KEY_API}&language=ko-KR'

        movie = requests.get(search_url).json()
        if movie : print(type(movie),movie['title'])
        recommend_movies.append(movie)

    context = {
        'Whom':Whom,
        'Feeling': Feeling,
        'recommend_movies': recommend_movies,


        }
    return render(request,'movies/moviehereresult.html',context)


def taste(request):
    print("취향 저격 추천 시작")
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    user_review = Review.objects.filter(user=user)
    if not user_review or len(user_review)< 3 :
        message= "적어도 영화 리뷰 3개는 써주시기 바랍니다."
        context = {
            'message' : message,
        }

        return render(request,'movies/recommendation.html/',context)

    '''
    게시글의 평점 만으로는 추천이 부정확할 것이라 판단하여,
    좋아요한 영화와 함께 데이터베이스 분석하여 결과를 내놓음.
    -> 게시글을 남긴 영화 개봉일과 평점 전체 평균으로 영화 데이터를 취향에 맞게 한번 필터링 한 후,
        좋아요한 영화들과 게시글 남긴 영화들의 장르들 최빈 3순위를 뽑아 영화를 추천.


    -게시글 평점을 통해 추출한 정보
    # 1. 고려사항 : 개봉일 (최신, 다양, 옛날)
    2. 장르 : 장르(많이 중복되는 장르가 있는가) + 좋아요한 영화들의 장르 합쳐서 장르 순위매김
    3. 평점 전체 평균 : 후한가-> 관용적, 포용적, 좀더 다양하고 인기있는 장르 많이 추천 ,
    박한가 -> 깐깐할 수 있다. 평점 좋은 위주로 너무 다양한 콘텐츠는 피하기.
     '''


    # 사용자가 작성한 게시글의 모든 평점의 평균
    reviews_avg = Review.objects.filter(user = request.user).aggregate(Avg('rank'))['rank__avg']
    print(reviews_avg)
    # # 사용자가 작성한 게시글의 모든 영화들 중 가장 최근 개봉일
    # latest_release_date = Review.objects.filter(user = request.user).movie.all().order_by('-release_date')[0]
    # print(latest_release_date)

    # 대체적으로 평점이 짠 사람에게는 - 탑랭킹과 인기영화를 높은 평점순으로 정렬된 안정적인 영화
    if reviews_avg < 7.0 :

        filtered_movies = Movie.objects.filter(Q(category='top-ranked') | Q(category='popular')).order_by('-vote_average')
    # 대체적으로 평점이 후한 사람에게는 - 모든 높은 평점순으로 정렬된 다양성 있는 영화
    else :
        filtered_movies = Movie.objects.order_by('-vote_average')


    # 사용자가 작성한 게시글의 모든 영화들
    reviews = Review.objects.filter(user = request.user).all()


    # 사용자가 좋아요 누른 영화들
    movies = user.like_movies.all()

    # 카운팅을 위해 장르를 가져와서 딕셔너리로 만듭니다.
    genres = Genre.objects.all()
    genres_dict = {}
    for genre in genres:
        genres_dict[genre.name] = 0
  	#사용자가 좋아요한 영화에서 장르 카운트
    for movie in movies:
        for genre in movie.genres.all():
            genres_dict[genre.name]+=1

    # 게시물에 작성한 영화의 장르도 함께 카운트
    for review in reviews:
        for genre in review.movie.genres.all():
            genres_dict[genre.name]+=1

    # 장르 내림차순 정렬
    sorted_genres_dict = sorted(genres_dict.items(), key=lambda kv: kv[1], reverse=True)
    genres_dict= dict(sorted_genres_dict)

    #장르명 쉽게 빼오기 위한 key리스트
    keys = []
    for key in genres_dict.keys():
        keys.append(key)

	#높은 평점 영화부터 시작해서 사용자가 가장 많이 좋아한 장르 3위를 모두 만족하면 영화 추천대상에 넣습니다.
    recommand = []
    recommand2 = []
    for filtered_movie in filtered_movies:

        check = [0,0,0]
        for genre in filtered_movie.genres.all():
            if genre.name == keys[0]:
                check[0] = 1
            elif genre.name == keys[1]:
                check[1] = 1
            elif genre.name == keys[2]:
                check[2] = 1
        if 0 not in check:
            recommand.append(filtered_movie)
        if sum(check) == 2 :
            recommand2.append(filtered_movie)
    print(recommand)


    if len(recommand) < 10 :
        recommand.extend(recommand2)

    context = {
        '1st_genre': keys[0],
        '2nd_genre': keys[1],
        '3rd_genre': keys[2],
        'reviews':reviews,
        'recommendations': recommand[:9],
        'you_liked_movies':movies,
    }

    return render(request, 'movies/taste.html', context)

def search(request):


    total_movies = Movie.objects.all()


    searchingword = request.GET.get('searchingword')
    if searchingword == '' :
        context = {
        'searchingword' : False,

        }
        return render(request, 'movies/searchresult.html',context)

    else :
        print(searchingword,'를 검색합니다.')

        search_url = f'https://api.themoviedb.org/3/search/movie?api_key={settings.TMDB_SECRET_KEY_API}&language=ko-KR&query={searchingword}&page=1'

        movies = requests.get(search_url).json().get('results')
        print(movies)
        db_movies = []
        for movie in movies :
            movie_id = movie['id']
            print(movie_id)
            db_movie = Movie.objects.filter(pk = movie_id)
            if db_movie: db_movies.append(movie_id)
        print(db_movies)


        context = {
                'searchingword' : searchingword,
                'movies' : movies,
                'db_movies' : db_movies,


            }
        return render(request, 'movies/searchresult.html',context)

