from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
# from .forms import CsRegisterForm
from django.views.generic import CreateView


from .forms import *
from blog.models import *
from users.models import *

# Create your views here.


def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "회원가입이 완료되었습니다.")
            return redirect(reverse("users:login"))
    return render(
        request, "users/register.html", {"title": "Create Account", "form": form}
    )


@login_required
def profile(request, ):
    myprofile = MyUserProfile.objects.filter(username=request.user.id).order_by("-pk")
    dog = Dog.objects.filter(owner=request.user.id).order_by("-pk")
    review_list = DogReview.objects.all().order_by("-pk")
    post_list = Post.objects.filter(author=request.user.id).order_by("-pk")
    context = {
        "post_list": post_list,
        "myprofile": myprofile,
        "review_list": review_list,
        "dog": dog,
        "avatar": request.user.avatar,
    }
    if request.method == "GET":
        return render(
            request,
            "users/profile.html",
            context,
        )
    elif request.method == "POST":
            new_review = DogReview()
            new_review.author = request.user
            new_review.review = request.POST["review"]
            new_review.save()
            return HttpResponseRedirect(reverse("users:profile"))

@login_required
def profile_update(request):
    user = request.user
    user = MyUser.objects.filter(username=user)
    user_info = MyUserProfile.objects.filter(username=user)
    if request.method == "GET":
        context = {
            "user": user,
            "user_info": user_info,
            "avatar": request.user.avatar,
    }
        return render(
        request,
        "users/profile_update.html",
        context,
    )
    elif request.method == "POST":
        user.name = request.POST["title"]
        user_info.text = request.POST["text"]
        user_info.save()
        return HttpResponseRedirect(f"/blog/post/{post_id}/")


class UserLoginView(LoginView, SuccessMessageMixin):
    template_name = "users/login.html"
    extra_context = {"title": "Log In"}
    redirect_authenticated_user = True
    success_message = "로그인 성공"


class UserLogoutView(LogoutView, SuccessMessageMixin):
    template_name = "users/logout.html"
    success_message = "로그아웃 완료"


def dog_update(request):
    form = DogCreationForm()
    if request.method == "POST":
        form = DogCreationForm(request.POST)
        if form.is_valid():
            my_dog = form.save(commit=False)
            my_dog.owner = request.user
            my_dog.created_date = timezone.now()
            my_dog.save()
            messages.success(request, "정보가 저장되었습니다.")
            return redirect(reverse("users:profile"))
    return render(
        request, "users/dog_update.html", {"title": "댕고 | 강아지 정보", "form": form}
    )