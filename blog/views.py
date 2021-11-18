from django.shortcuts import render, HttpResponseRedirect, reverse
from django.utils import timezone
from blog.models import Post

# Create your views here.
def blog_home(request):
    post_list = Post.objects.all().order_by("-pk")
    context = {
        "post_list": post_list,
    }

    return render(request, 'blog/post_list.html', context)

def blog_post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    context = {
        "post": post,
    }
    return render(request, 'blog/post.html', context)

def blog_post_write(request):
    if request.method == "POST":
        new_post = Post()
        new_post.title = request.POST["title"]
        new_post.text = request.POST["text"]
        if request.FILES["image"]:
            new_post.head_image = request.FILES["image"]
        new_post.likes = 0
        new_post.save()
        return HttpResponseRedirect(reverse("blog:post"))

def blog_post_delete(request, post_id):
    target_post = Post.objects.get(pk=post_id)
    target_post.delete()
    return HttpResponseRedirect("/profile/")

def blog_post_edit(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == "GET":
        context = {
            "post": post
        }
        return render(request, "blog/edit.html", context)
    elif request.method == "POST":
        post.title = request.POST["title"]
        if request.FILES["image"]:
            post.head_image = request.FILES["image"]
        post.text = request.POST["text"]
        post.save()
        return HttpResponseRedirect(f"/blog/post/{post_id}/")