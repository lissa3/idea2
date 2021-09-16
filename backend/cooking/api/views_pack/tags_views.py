from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from taggit.models import Tag
from api.serializers.tags.tags_ser import TagSerializer
from api.serializers.ideas.idea_ser import IdeaSerializer
from ideas.models import Idea

User  = get_user_model()

class TagList(generics.ListAPIView):
    """ get list of tags"""
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class=None

    def get_queryset(self, queryset=None):
        return Tag.objects.all()


# class TagIdeasListSlug(generics.ListAPIView):
#     """ get list of ideas based on a tag's slug"""
#     serializer_class = IdeaSerializer
#     permission_classes = (AllowAny,)
    
#     def get_queryset(self):
#         # print("inside  tag view on idea slug")
#         slug = self.kwargs.get('slug')
#         if slug is not None:
#             # result = Idea.objects.filter(tags__slug__in=(slug,))
#             # print("result is", result)
#             return Idea.objects.filter(tags__slug__in=(slug,))
#         else:
#             return Response(status=400)
            
class TagIdeasListName(generics.ListAPIView):
    """ get list of tags via names"""
    serializer_class = IdeaSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        name = self.kwargs.get('name')
        if name is not None:
            # print("server got a tag:", name)
            # print("found following ideas for this tag", Idea.objects.filter(tags__name__in=(name,)))
            return Idea.objects.filter(tags__name__in=(name,))
        else:
            return Response(status=400)            

