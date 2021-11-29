from django.shortcuts import render, HttpResponseRedirect, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from users.models import MyUser
from friendship.models import Friendship
from friendship.forms import AddFriendForm




# Create your views here.
@login_required
def dog_list(request):
    dog_list = MyUser.objects.filter(address=request.user.address).order_by("-pk")
    context = {
        "dog_list": dog_list,
    }
    form = AddFriendForm(user=request.user)
    if request.method == "POST":
        form = AddFriendForm(request.POST, user=request.user)
        if form.is_valid():
            new_friend = MyUser.objects.get(username=form.cleaned_data.get("username"))
            current_user = request.user

            # checks if there is a pending request yet to be accepted.
            if (
                Friendship.objects.filter(user=new_friend, friend=current_user).count()
                > 0
            ):
                messages.warning(
                    request,
                    "You have a pending request or already rejected a request from this user",
                )
                return redirect(reverse("dog:list"))

            # checks if the two users are friends already
            if Friendship.objects.filter(
                Q(user=current_user, friend=new_friend, status=1)
                | Q(user=new_friend, friend=current_user, status=1)
            ):
                messages.info(request, "You are already friends with this user")
                return redirect(reverse("dog:list"))

            if Friendship.objects.filter(
                user=current_user, friend=new_friend, status=0
            ):
                messages.info(request, "You already sent a friend request to this user")
                return redirect(reverse("dog:list"))

            # a success message
            Friendship.objects.create(user=current_user, friend=new_friend)
            messages.success(request, "Friend request sent successfully")
            return redirect(reverse("friendship:friendship"))

    return render(
        request,
        "dog/doglist.html",
        context,
    )

def dog_profile_view(request, user_id):
    profile = MyUser.objects.get(id=user_id)
    context = {
        "profile": profile,
    }
    return render(request, 'dog/dog_profile.html', context)
