from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny

from api.serializers.categs.categ_ser import CategorySerializer,CategoryNameSerializer
from ideas.models import Category

User  = get_user_model()


class CatListIdeaForm(generics.ListAPIView):
    """ get all categories for idea creation form without tree structure"""
    serializer_class = CategoryNameSerializer
    permission_classes = (AllowAny,)
    pagination_class=None

    def get_queryset(self, queryset=None):
        queryset = Category.objects.all()
        return queryset
        # return queryset.get_cached_trees()


class CategoryList(generics.ListAPIView):

    """ get all categories with tree structure"""
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    pagination_class = None
    # print("inside view")

    def get_queryset(self, queryset=None):
        # print("view for cats works with qs:", Category.objects.all())
        # print("categs view line 60")
        queryset = Category.objects.all()
        # print(type(Category.objects.all()))        
        return queryset
#       # return queryset.get_cached_trees()
