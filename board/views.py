from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Post

# Create your views here.
def index(request):
    postList = Post.objects.order_by('-date')
    context = {'postList': postList}
    return render(request, 'board/list.html', context)

def detail(request, postId):
    post = Post.objects.get(id=postId)
    context = {'post': post}
    return render(request, 'board/detail.html', context)

def answer_create(request, postId):
    # 답글 추가
    post = get_object_or_404(Post, pk=postId)
    post.answer_set.create(content=request.POST.get('content'), date=timezone.now())
    return redirect('board:detail', postId=postId)