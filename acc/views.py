from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import check_password
from acc.models import User
from django.contrib import messages
# Create your views here.

def chpass(request):
    cp = request.POST.get("cpass")
    if check_password(cp, request.user.password):
        np = request.POST.get("npass")
        request.user.set_password(np)
        request.user.save()
        return redirect("acc:login")
    return redirect("acc:update") 

def update(request):
    if request.method == "POST":
        u = request.user
        up = request.FILES.get("upic")
        uc = request.POST.get("ucomm")
        um = request.POST.get("umail")
        if up:
            u.pic = up
        u.email = um
        u.comment = uc
        u.save()
        return redirect("acc:profile")
    return render(request, "acc/update.html")


def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        uc = request.POST.get("ucomm")
        pi = request.FILES.get("upic")
        User.objects.create_user(username=un, password=up,
        comment=uc, pic=pi)
        return redirect("acc:login")
    return render(request, "acc/signup.html")


def delete(request):
    pw = request.POST.get("pwck")
    if check_password(pw, request.user.password):
        request.user.pic.delete()
        request.user.delete()
        return redirect("acc:index")
    return redirect("acc:profile")

def profile(request):
    return render(request, "acc/profile.html")

def userlogout(request):
    logout(request)
    return redirect("acc:login")

def userlogin(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        u = authenticate(username=un,password=up)
        if u:
            login(request, u)
            messages.success(request, f"{un} 님 환영합니다.")
            return redirect("acc:index")
        else:
            messages.error(request, "계정정보가 일치하지 않습니다.")
    return render(request, "acc/login.html")

def index(request):
    return render(request, "acc/index.html")