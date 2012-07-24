from articles.models import Article,PostList

def add_hit(articleid):
    a=Article.objects.get(aid=article)
    a.hits=a.hits+1
    a.save()