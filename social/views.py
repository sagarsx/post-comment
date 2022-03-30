from email import message
from multiprocessing import context
from multiprocessing.sharedctypes import Value
from pickle import TRUE
from django.shortcuts import redirect, render
from . models import *
from django.contrib.auth import authenticate, login
from django.db.models import Count
from django.contrib.auth.decorators import login_required


# Create your views here.

def feedPage(request):
    return render(request, 'social/feed.html')



def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('detail') 

        else:
            msg = 'Please enter correct username and password. Note that both field may be case sensitive'
            context = {'msg':msg}
            return render(request, 'social/loginpage.html', context)   

    return render(request, 'social/loginpage.html')



@login_required(login_url='login')
def composePost(request):

    if request.method == 'POST':
        post_user = request.user
        post_message = request.POST["message"]
        Post.objects.create(user=post_user, message=post_message)
        return redirect('detail')

    return render(request, 'social/compose.html')



@login_required(login_url='login')
def deletePost(request, id=None):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('detail')



@login_required(login_url='login')
def deleteComment(request, id=None):
    comment = Comment.objects.get(id=id)
    comment.delete()
    return redirect('detail')



@login_required(login_url='login')
def commentPost(request, id):

    if request.method == "POST":
        comment_user = request.user
        post = Post.objects.get(id=id)    
        comment = request.POST["comment"]
        Comment.objects.create(user=comment_user, post=post, comment=comment)
        return redirect('detail')

    return render(request, 'social/comment.html')



@login_required(login_url='login')
def likePost(request, id):
    like_user = request.user
    post = Post.objects.get(id=id)

    if Like.objects.filter(user = like_user,post=post).exists():
        return redirect('detail')
    else:
        Like.objects.create(user = like_user,post=post,like=True)
        return redirect('detail')



@login_required(login_url='login')
def dislikePost(request, id):
    like_user = request.user
    post = Post.objects.get(id=id)

    if Like.objects.filter(user = like_user,post=post).exists():
        return redirect('detail')
    else:
        Like.objects.create(user = like_user,post=post,like=False)
        return redirect('detail')



def postDetail(request):
    username = request.POST.get("username")

    post = Post.objects.values("user__username", "message", "created", "id")
    comment = Comment.objects.values("comment", "user__username", "post_id", "id")
    comment_count = (Comment.objects.values('post_id').annotate(Count('comment')))
    likes = Like.objects.values("post_id", "like")
    like_count = {}
    dislike_count ={}

    for like in likes:
        if like["like"] is False:
            if like['post_id'] in dislike_count:
                dislike_count[like['post_id']] +=1
            else:
                dislike_count[like['post_id']] = 1
        else:
            if like["post_id"] in like_count:
                like_count[like["post_id"]] += 1          
            else:
                like_count[like["post_id"]] = 1
    context = {
    "username":username, "post":post, 
    "comment":comment, "like":like, 'comment_count':comment_count,
    'like_count':like_count, 'dislike_count':dislike_count, 
    }

    return render(request, 'social/feed.html', context)

