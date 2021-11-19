from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import PermissionDenied
# from .forms import CsRegisterForm
from django.views.generic import CreateView


from .forms import UserCreationForm
from blog.models import Post

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
def profile(request):

    post_list = Post.objects.all().order_by("-pk")
    context = {
        "post_list": post_list,
        "title": "Profile",
        "avatar": request.user.avatar
    }
    return render(
        request,
        "users/profile.html",
        context,
    )

@login_required
def profile_update(request):
    context = {
        "title": "Profile",
        "avatar": request.user.avatar
    }
    return render(
        request,
        "users/profile_update.html",
        context,
    )

class UserLoginView(LoginView, SuccessMessageMixin):
    template_name = "users/login.html"
    extra_context = {"title": "Log In"}
    redirect_authenticated_user = True
    success_message = "로그인 성공"


class UserLogoutView(LogoutView, SuccessMessageMixin):
    template_name = "users/logout.html"
    success_message = "로그아웃 완료"
