from .models import UserIdeaRelation
from django.db.models import Avg,Count,Case,When,Max


def calc_rating(obj):   
    rating_val = UserIdeaRelation.objects.filter(idea=obj).aggregate(rate_value=(Avg('rating')))    
    obj.avg_rate = rating_val.get('rate_value',None)    
    obj.save()

def calc_count_likes(obj):
    agr_likes=UserIdeaRelation.objects.filter(idea=obj).aggregate(like_total=(Count(Case(When(like=True, then=1))))) 
    obj.an_likes = agr_likes.get('like_total',None)    
    obj.save()

# def calc_max_rating(obj):
#     agr_likes=UserIdeaRelation.objects.filter(idea=obj).aggregate(max_rating=Max('rating'))   
#     # arrg_likes = UserIdeaRelation.objects.filter(idea=obj).aggregate(count_likes=(Count('like')))
#     print("dict",agr_likes)
#     obj.likes = agr_likes.get('like_total',None)
#     print("calc rating is:",obj.likes)
#     obj.save()
