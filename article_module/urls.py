from django.urls import path
from . import views

urlpatterns = [
    path('', views.ArticlesListView.as_view(), name='articles-list-view'),
    path('article-detail/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail-view'),
    path('article-score-create/<int:pk>', views.ArticleScoreCreateView.as_view(), name='article-score-create-view'),
    path('create-article/', views.ArticleCreateView.as_view(), name='article-create-view'),
    path('article-update/<int:pk>/', views.ArticleUpdateView.as_view(), name='article-update-view'),
    path('article-score-protest/<int:pk>/', views.ArticleScoreProtestView.as_view(), name='article-score-protest-view'),
    path('edit-prmission/<int:pk>/', views.edit_article_permission, name='article-permission'),
    path('article-score-permission/<int:pk>/', views.article_score_permission, name='article-score-permission'),
    path('article/<int:pk>/download/', views.download_article_file, name='download-article-file'),

]