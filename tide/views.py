from django.shortcuts import render

# Create your views here.
from rest_framework.generics import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView


from .models import Article, Author
from .serializers import ArticleSerializer, ArticleSerializerL

class ArticleView(APIView):
    def get(self, request, key, spot):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response({"articles": serializer.data})

    def post(self, request):
        article = request.data.get('article')

        # Create an article from the above data
        serializer = ArticleSerializer(data=article)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({"success": "Article '{}' created successfully".format(article_saved.title)})

    def put(self, request, pk):
        saved_article = get_object_or_404(Article.objects.all(), pk=pk)
        data = request.data.get('article')
        serializer = ArticleSerializer(instance=saved_article, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({
            "success": "Article '{}' updated successfully".format(article_saved.title)
        })

    def delete(self, request, pk):
        # Get object with this pk
        article = get_object_or_404(Article.objects.all(), pk=pk)
        article.delete()
        return Response({
            "message": "Article with id `{}` has been deleted.".format(pk)
        }, status=204)

from rest_framework.generics import RetrieveUpdateAPIView

class SingleArticleView(RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializerL

class ArticleViewL(ListCreateAPIView):
    import json
    import os
    module_dir = os.path.dirname(__file__)
    file_patch = os.path.join(module_dir,'Data/')
    with open(file_patch + 'TideList.json', 'r', encoding='utf-8') as fh:  # открываем файл на чтение
        queryset = json.load(fh)  # загружаем из файла данные в словарь data

    #queryset = Article.objects.all()
    #serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(Author, id=self.request.data.get('author_id'))
        return serializer.save(author=author)


class ArticleViewT(APIView):
    def get(self, request, key, point):
        import json
        import os
        module_dir = os.path.dirname(__file__)
        file_patch = os.path.join(module_dir,'Data/')
        with open(file_patch + 'TideList.json', 'r', encoding='utf-8') as fh:  # открываем файл на чтение
            queryset = json.load(fh)  # загружаем из файла данные в словарь
        if key == 5698456:
            output_dict = [x for x in queryset if x['tide_spot'] == point]
            #resdata = json.dumps(output_dict)
            return Response(output_dict)
        return Response({
            "Error": "Key incorrect"})



