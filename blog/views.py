from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
from django.views.generic import ListView, DetailView
from django.views import View

from .models import Post
from .forms import CommentForm

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering=["-date"]
    context_object_name="posts"

    

    def get_queryset(self):
        queryset=super().get_queryset()
        data=queryset[:3]
        return data

def get_date(post):
    return post['date']

# Create your views here.

class AllPostsView(ListView):
    template_name="blog/all-posts.html"
    model=Post
    ordering=["-date"]
    context_object_name="all_posts"


class SinglePostView(View):
    # template_name="blog/post-detail.html"
    # model=Post
    # context_object_name="post"


    def get(self, request,slug):
        post=Post.objects.get(slug=slug)
        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":CommentForm(),
            "comments":post.comments.all().order_by("-id"),
        }
        return render(request, "blog/post-detail.html",context)
    

    
    def post(self, request,slug):
        comment_form=CommentForm(request.POST)
        post=Post.objects.get(slug=slug)

        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.post=post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        
        
        context={
            "post":post,
            "post_tags":post.tags.all(),
            "comment_form":comment_form,
            "comments":post.comments.all().order_by("-id"),

        }
        return render(request, "blog/post-detail.html",context)
        

class ReadLaterView(View):

    def get(self, request):
        stored_posts=request.session.get("stored_posts")

        context={}

        if stored_posts is None or len(stored_posts):
            context["posts"]=[]
            context["has_posts"]=False
        else:
            posts=Post.objects.filter(id__in=stored_posts)
            context["posts"]=posts
            context["has_posts"]=True

        return render(request, "blog/stored-posts.html", context)
            

        
    

    def post(self, request):
        stored_posts=request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts=[]

        post_id=int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)

        return HttpResponseRedirect("/")




    # def get_context_data(self, **kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context["post_tag"]=self.object.tags.all()
    #     context["comment_form"]=CommentForm()
    #     return context

def commentpage(request):
    pass
    



from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)