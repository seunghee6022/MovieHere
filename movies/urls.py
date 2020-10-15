from django.urls import path
from . import views
app_name = 'movies'

urlpatterns = [

    path('', views.index, name='index'),
    path('top_ranked/', views.top_ranked, name='top_ranked'),
    path('upcoming/', views.upcoming, name='upcoming'),
    path('popular/', views.popular, name='popular'),
    path('nowplaying/', views.nowplaying, name='nowplaying'),
    path('<int:movie_pk>/like/', views.movie_like, name='movie_like'),
    path('<int:movie_pk>/update/', views.movie_update, name='movie_update'),
    path('<int:movie_pk>/delete/', views.movie_delete, name='movie_delete'),
    path('<int:movie_pk>/detail/', views.detail, name='detail'),

    path('movie_create/', views.movie_create, name='movie_create'),
    path('<int:movie_pk>/', views.review_list, name='review_list'),
    path('<int:movie_pk>/create/', views.review_create, name='review_create'),
    path('<int:movie_pk>/<int:review_pk>/detail/', views.review_detail, name='review_detail'),
    path('<int:movie_pk>/<int:review_pk>/update/', views.review_update, name= 'review_update'),
    path('<int:movie_pk>/<int:review_pk>/delete/', views.review_delete, name= 'review_delete'),
    path('<int:movie_pk>/<int:review_pk>/comments/', views.comment_create, name= 'comment_create'),
    path('<int:movie_pk>/<int:review_pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name= 'comment_delete'),
    path('<int:movie_pk>/<int:review_pk>/like/', views.review_like, name="review_like"),
    path('recommendation/', views.recommendation, name='recommendation'),
    path('taste/', views.taste, name='taste'),
    path('movieherechoice/', views.movieherechoice, name='movieherechoice'),
    path('moviehereresult/', views.moviehereresult, name='moviehereresult'),
    path('search/', views.search, name='search'),


]