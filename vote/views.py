from django.shortcuts import render, redirect
from .models import Topic, Choice
# Create your views here.


def index(reqeust):
    t = Topic.objects.all()
    context = {
        "tset" : t
    }
    return render(reqeust, 'vote/index.html', context)

def vote(request, tpk):
    t = Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        t.voter.add(request.user)
        cpk = request.POST.get("cho")
        c = Choice.objects.get(id=cpk)
        c.choicer.add(request.user)
    return redirect("vote:detail", tpk)

def detail(request, tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    cho = Choice.objets.all()
    choice = cho.choicer
    context = {
        "tset" : t,
        "cset" : c,
        "cho" : choice
    }
    return render(request, "vote/detail.html", context)

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        t = Topic(subjects=s, maker=request.user, content = c)
        t.save()
        cn = request.POST.get("bogi")
        cc = request.POST.get("com")
        for name, com in zip(cn,cc):
            Choice(topic=t, name=name, comment=com).save()
        return redirect("vote:index")
    return render(request, "vote/create.html")

def cancel(request, tpk):
    u = request.user
    t = Topic.objects.get(id=tpk)
    t.voter.remove(request.user)
    u.choice_set_get(topic=t).choicer.remove(u)
    return redirect("vote:detail", tpk)
