from django.urls import path

from . import views

urlpatterns = [
    path("",views.StartingPageView.as_view(), name="starting-page"),
    path("posts/", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(),  #/posts/my-first-post
         name="post-detail-page"),
    #path("comment/",views.commentpage),
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
]
