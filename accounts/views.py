from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm, ProfileUpdateForm


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect ("profile")
    else:
        form = SignupForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html", {"user": request.user})

@login_required
def profile_update_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile_edit.html", {"form": form})
