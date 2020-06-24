from django.urls import path

from .views import ArticleView, ArticleViewT
from .views import ArticleViewL, SingleArticleView

app_name = "tide"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('tide/', ArticleView.as_view()),
    path('tide/<int:pk>', ArticleView.as_view()),
    path('tide_l/<int:pk>', SingleArticleView.as_view()),
    path('tides/', ArticleViewL.as_view()),
    path('tides/<int:key>-<str:point>', ArticleViewT.as_view())
]