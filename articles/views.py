from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.decorators import login_required
from . import forms

def articles_list(request):
    articles = models.Article.objects.all().order_by('-date')
    context = {
        'articles' : articles
    }
    return render(request, "articles/articles_list.html", context)


def article_detail(request, slug):
    # return HttpResponse(slug)
    article = models.Article.objects.get(slug=slug)
    context = {
        "article" : article
    }
    return render(request, "articles/articles_detail.html", context)



@login_required(login_url = '/accounts/login')
def create_article(request):
    if request.method == 'POST':
        form = forms.CreateArticle(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.author = request.user
            instance.save()
            return redirect('articles:articles_list')
    else:
        form = forms.CreateArticle()
        context = {
            'form': form
            }
    return render(request, 'articles/create_article.html', context)
