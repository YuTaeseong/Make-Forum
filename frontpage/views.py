from django.shortcuts import render
from .forms import Post, CreatUserForms
from .models import MakeBoard, Profile
from django.contrib.auth.decorators import login_required
# Create your views here.
# 리다이렉트 할때 필요한것
from django.shortcuts import redirect
# get or 404
from django.shortcuts import get_object_or_404
# 수정일 넣을 때 필요한 것
from django.utils import timezone
# ajax 할 때 필요한 것들
from django.http import JsonResponse
from django.contrib.auth.models import User

def frontpage(request) :
    MakeBoards = MakeBoard.objects.order_by('-id')
    return render(request, 'frontpage/frontpage.html', {'MakeBoards':MakeBoards})

def post_detail(request, pk):
    Board = MakeBoard.objects.get(pk = pk)
    like = 'off'
    follow = 'off'
    if request.user.is_authenticated() :
        userpk = request.user.pk
        likeornot = Board.like.filter(pk = userpk)
        if likeornot.exists() :
            like = 'on'
        else:
            like = 'off'

        authorpk = MakeBoard.objects.get(pk=pk).author.pk
        followornot = Profile.objects.get(user__pk=authorpk).follower.filter(pk=userpk)
        if followornot.exists() :
            follow = 'on'
        else:
            follow = 'off'

    number = MakeBoard.objects.get(pk=pk).like.count()
    return render(request, 'post/detail.html', {'Board':Board, 'like' : like, 'number' : number, 'follow':follow})

@login_required
def post_edit(request, pk):
    Board = get_object_or_404(MakeBoard, pk=pk)
    Board.published_date = timezone.now()
    if request.method == "POST" :
        form = Post(request.POST, request.FILES, instance=Board)
        if form.is_valid() :
            form.save()
            return redirect('post_detail', pk = pk)
    else:
        editBoard = Post(instance=Board)
    return render(request, 'post/edit.html', {'editBoard' : editBoard})

@login_required
def post_new(request):
    Board = MakeBoard(author = request.user, published_date = timezone.now(), photo = 'photos/favicon1.png')
    if request.method == 'POST' :
        form = Post(request.POST, request.FILES, instance=Board)
        if form.is_valid() :
            form.save()
            return redirect('post_detail', pk=Board.pk)

    editBoard = Post(instance=Board)
    return render(request, 'post/edit.html', {'editBoard' : editBoard})

@login_required
def post_delete(request):
    deletelist = 0
    if request.method == 'POST' :
        deletelist = request.POST.getlist('Delete')

        for delete in deletelist :
            MakeBoard.objects.filter(pk = delete).delete()

    userBoard = MakeBoard.objects.filter(author_id = request.user.id)
    return render(request, 'post/delete.html', {'userBoard': userBoard })

@login_required
def like(request):
    userpk = request.GET.get('userpk')
    postpk = request.GET.get('postpk')
    likeornot = MakeBoard.objects.filter(like__pk = userpk).filter(pk = postpk)
    user = User.objects.get(pk=userpk)
    if likeornot.exists() :
        MakeBoard.objects.get(pk=postpk).like.remove(user)
        number = MakeBoard.objects.get(pk=postpk).like.count()
        data = {
            'add' : 'dislike',
            'remove' : 'like',
            'number' : number
        }
    else:
        MakeBoard.objects.get(pk = postpk).like.add(user)
        number = MakeBoard.objects.get(pk=postpk).like.count()
        data = {
            'add' : 'like',
            'remove' : 'dislike',
            'number': number
        }
    return JsonResponse(data)

@login_required
def follow(request):
    userpk = request.GET.get('userpk')
    authorpk = request.GET.get('authorpk')
    user = User.objects.get(pk=userpk)

    if Profile.objects.get(user__pk=authorpk).follower.filter(pk=userpk).exists() :
        Profile.objects.get(user__pk=authorpk).follower.remove(user)
        data = {
            'add': 'btn-default',
            'remove': 'btn-primary'
        }
    else:
        Profile.objects.get(user__pk=authorpk).follower.add(user)
        data = {
            'add': 'btn-primary',
            'remove': 'btn-default'
        }

    return JsonResponse(data)

@login_required
def likeandfollow(request) :
    userpk = request.user.pk
    followings = User.objects.get(pk=userpk).follower.all()
    likes = User.objects.get(pk=userpk).like.all()
    followers = Profile.objects.get(user__pk = userpk).follower.all()
    return render(request, 'profile/likeandfollow.html', {'followings' : followings, 'followers' : followers, 'likes' : likes})

@login_required
def overview(request) :
    return render(request, 'profile/overview.html', {})

@login_required
def profile_edit(request) :
    userBoard = MakeBoard.objects.filter(author__pk = request.user.pk)
    return render(request, 'profile/edit.html', {'userBoard' : userBoard})