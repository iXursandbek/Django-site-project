from django.urls import path
from . views import *

urlpatterns = [
   path('', HomeView, name='posts'),
   path("post/<slug:slug>/", BlogDetailView, name="detail"),
   path("page/<slug:slug>/", PageView, name="page"),
   path('searchbar/', Searchbar, name='searchbar'),
   path('review/<int:pk>/', CommentView.as_view(), name='comment_view'),
]