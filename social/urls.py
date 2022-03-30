from unicodedata import name
from django.urls import path
from . import views
urlpatterns = [
    path('', views.loginPage, name="login"),
    path('feed/', views.feedPage, name="feed"),
    path('compose/', views.composePost, name='compose'),
    path('postdetail/', views.postDetail, name='detail'),
    path('delete/<int:id>', views.deletePost, name="delete"),
    path('comment/<int:id>', views.commentPost, name="comment"),
    path('deletecomment/<int:id>', views.deleteComment, name="deletecomment"),
    path('like/<int:id>', views.likePost, name="like"),
    path('dislike/<int:id>/', views.dislikePost, name="dislike"),
]
