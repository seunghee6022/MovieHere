from django import forms
from .models import Movie, Review, Comment
from .validators import *

class MovieForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(MovieForm, self).__init__(*args, **kwargs)
        f = self.fields

        for item in list(self.errors):
            self.fields[item].widget.attrs.update({'autofocus': True})
            break
        else:
            self.fields['title'].widget.attrs.update({'autofocus': True})

        field_names = ['title', 'original_title', 'release_date', 'popularity', 'vote_count', 'vote_average', 'adult', 'overview', 'original_language', 'poster_path', 'backdrop_path', 'category', 'genres']
        label_names = ['제목', '원래_제목', '출시일', '인기', '추천수', '평균 추천수', '성인', '개요', '모국어','포스터','뒷배경', '카테고리', '장르' ]

        for name, label in zip(field_names, label_names):
            if name == 'adult' or name == 'genres' :
                f[name].widget.attrs.update({
                'class': 'form-control',
                'name': name,
                'id': name,
                'required': False,
            })
            else :
                f[name].widget.attrs.update({
                    'class': 'form-control',
                    'name': name,
                    'id': name,

                    'required': True,
                })

            f[name].label = label

    class Meta:
        model = Movie
        fields = ['title', 'original_title', 'release_date', 'popularity', 'vote_count', 'vote_average', 'adult', 'overview', 'original_language', 'poster_path', 'backdrop_path', 'category', 'genres']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title','content','rank']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
