from django.shortcuts import get_object_or_404, render, redirect
from .models import Data
from django.http import HttpResponse
from .forms import PostForm
from .forms import SearchForm
from django.utils import timezone


def index(request):
    return render(request, 'ChainLicense/index.html')

# 아래에 블록체인 api 입력 및 로직 구현합니다.
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', seq=post.seq)
    else:
        form = PostForm()
    return render(request, 'ChainLicense/post_edit.html', {'form': form})

def post_detail(request, seq):
    data = get_object_or_404(Data, seq=seq)
    return render(request, 'ChainLicense/post_detail.html', {'data': data})

def post_compare(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.save(commit=False)
            if search.name:
                if search.author:
                    search.name = '%' + search.name
                    datas = Data.objects.filter(name=search.name, author=search.author)
                else: datas = Data.objects.filter(name=search.name)
            else:
                datas = Data.objects.filter(author=search.author)

            return render(request, 'ChainLicense/post_list.html', {'datas': datas})

    form = PostForm()
    return render(request, 'ChainLicense/post_compare.html', {'form': form})

def post_list(request):
    datas = Data.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'ChainLicense/post_list.html', {'datas': datas})