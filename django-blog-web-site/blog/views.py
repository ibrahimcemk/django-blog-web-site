from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Post Listesi
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

# Post Detay
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# Yeni Post Oluşturma
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)  # request.FILES burada gerekli
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# Post Düzenleme
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# Post Silme
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Yalnızca postu yazan ya da admin silme işlemi yapabilir
    if post.author != request.user and not request.user.is_staff:
        raise Http404("Bu postu silmeye yetkiniz yok.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')  # Silme işleminden sonra ana sayfaya dön

    return render(request, 'blog/post_confirm_delete.html', {'post': post})
