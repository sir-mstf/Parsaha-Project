from django.http import HttpResponseRedirect, HttpResponseForbidden, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from . import forms
from django.http import Http404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from account_module.models import Student
from article_module.models import Article, ArticleScore
#from .forms import ArticleScoreForm, ArticleForm


# Create your views here.

class ArticlesListView(ListView):
    model = Article
    context_object_name = 'articles'
    template_name = 'article_module/article_list_view.html'

    def get_queryset(self):
        user = self.request.user

        if hasattr(user, 'student'):
            return Article.objects.filter(author=user.student)

        if hasattr(user, 'proff'):
            return Article.objects.filter(professors=user.proff)
        else:
            return Article.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article_module/article_detail_view.html'
    context_object_name = 'article'

    def get_queryset(self):
        user = self.request.user
        article_id = self.kwargs['pk']

        if hasattr(user, 'student'):
            return Article.objects.filter(author=user.student, id=article_id)
        elif hasattr(user, 'proff'):
            return Article.objects.filter(professors=user.proff, id=article_id)
        return Article.objects.none()

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data()
        context['user'] = self.request.user
        context['articles_score'] = ArticleScore.objects.filter(article=self.kwargs['pk']).all()

        if hasattr(user, 'proff'):
            context['article_score'] = ArticleScore.objects.filter(article=self.kwargs['pk'], professor=user.proff).first()
        return context


class ArticleScoreCreateView(UpdateView):
    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(ArticleScore, pk=self.kwargs['pk'])
        if not self.object.scoring_permission: #and request.user.proff:
            return HttpResponseForbidden('not permitted to scoring this article for now')
        return super().dispatch(request, *args, **kwargs)

    model = ArticleScore
    #fields = ['score', 'score_1', 'score_2', 'score_3', 'score_4', 'comment']
    template_name = 'article_module/article_score_view.html'
    form_class = forms.ArticleScoreForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['article_score_id'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        query = ArticleScore.objects.filter(id=self.kwargs['pk'], professor__user=self.request.user)
        return query

    #def get_object(self, queryset=None):
    #    article_id = self.kwargs['pk']
    #    professor = self.request.user.proff
    #    return get_object_or_404(ArticleScore, article_id=article_id, professor=professor)

    def get_success_url(self):
        article_score = ArticleScore.objects.get(id=self.kwargs['pk'])
        return reverse('article-detail-view', kwargs={'pk': article_score.article.id})


# create form for std and prof...
class ArticleCreateView(CreateView):
    model = Article
    #fields = ['title', 'content', 'file']
    template_name = 'article_module/create_article_view.html'
    form_class = forms.ArticleForm

    def form_valid(self, form):
        student = get_object_or_404(Student, user=self.request.user)
        form.instance.author = student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles-list-view')

    #def form_valid(self, form):
    #    form.instance.article_id = self.kwargs['pk']
    #    form.instance.professor_id = self.request.user.proff.id
    #    return super().form_valid(form)


class ArticleUpdateView(UpdateView):
    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Article, pk=self.kwargs['pk'])
        if not self.object.edit_permission:
            return HttpResponseForbidden('not permitted to edit this article for now')
        return super().dispatch(request, *args, **kwargs)

    model = Article
    #fields = ['title', 'content', 'file']
    template_name = 'article_module/update_article_view.html'
    form_class = forms.ArticleForm

    def get_queryset(self):
        query = Article.objects.filter(id=self.kwargs['pk'], author=self.request.user.student)
        return query

    def get_success_url(self):
        return reverse('article-detail-view', args=[self.kwargs['pk']])


class ArticleScoreProtestView(UpdateView):
    model = ArticleScore
    #fields = ['student_protest']
    template_name = 'article_module/article_score_protest_view.html'
    form_class = forms.ArticleScoreProtestForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['article_score_id'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        query = ArticleScore.objects.filter(article__author=self.request.user.student)
        return query

    def get_success_url(self):
        return reverse('article-detail-view', args=[Article.objects.get(articlescore=self.kwargs['pk']).id])


def download_article_file(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if (hasattr(request.user, 'proff') and
            (article.professors == request.user.proff or article.manager == request.user.proff)):
        return FileResponse(article.file.open('rb'), as_attachment=True, filename=article.file.name)

    elif hasattr(request.user, 'student') and article.author != request.user.student:
        return FileResponse(article.file.open('rb'), as_attachment=True, filename=article.file.name)

    else:
        return HttpResponseForbidden('not permitted to download this article')


def edit_article_permission(request, pk):
    if request.POST:
        article = get_object_or_404(Article, id=pk, manager_id=request.user.proff.id)
        article.edit_permission = not article.edit_permission
        article.save()
        return redirect('article-detail-view', pk)

    if request.GET:
        raise Http404


def article_score_permission(request, pk):
    if request.POST:
        article_score = get_object_or_404(ArticleScore, id=pk, article__manager_id=request.user.proff.id)
        article_id = article_score.article.id
        article_score.scoring_permission = not article_score.scoring_permission
        article_score.save()
        return redirect('article-detail-view', article_id)

    if request.GET:
        raise Http404


