from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views


app_name = 'articles'
urlpatterns = [
    path('add', login_required(views.AddArticleView.as_view()), name='add'),
    path('change/<str:slug>', login_required(views.ChangeArticleView.as_view()), name='change'),
    path('read/<str:slug>', login_required(views.ReadArticleView.as_view()), name='read'),
]