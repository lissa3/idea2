from .models import UserIdeaRelation
from django.db.models import Avg,Count


def calc_rating(obj):
    # print("rating is:",UserIdeaRelation.objects.filter(idea=obj).aggregate(rate_value=(Count('rating'))))
    print("start func with idea:",obj)
    rating_val = UserIdeaRelation.objects.filter(idea=obj).aggregate(rate_value=(Avg('rating')))
    print("dict",rating_val)
    obj.rating = rating_val.get('rate_value',None)
    print("calc rating is:",obj.rating)
    obj.save()
