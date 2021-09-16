# from django.db.models import query
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model



from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,RetrieveModelMixin, UpdateModelMixin
from rest_framework import viewsets 
from rest_framework.generics import ListAPIView #,RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter 
# from rest_framework.exceptions import APIException, PermissionDenied

# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken (GOOD TO HAVE delete profile)
from comments.models import Comment
from ideas.models import Idea
from api.serializers.comments.comment_ser import CommentSerializer #,ListCommentSerializer
from api.permissions import IsOwnerOrIsStaff


User = get_user_model()

class CommentAPIView(CreateModelMixin,UpdateModelMixin,DestroyModelMixin,RetrieveModelMixin,viewsets.GenericViewSet):
    """create comment instance """
    permission_classes = (IsOwnerOrIsStaff,)
    authentication_class = (IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    

    def perform_create(self, serializer):
        # print("self is",self)
        # print("self.data",self.request.data)
        # print("line 35 inside perform create",self.request.data)
        # user = self.request.user
        # print("line 35",user)
        # print("req:",self.request.data)
        # {'body': 'Greet', 'idea': 7, 'parent': None}
        idea = get_object_or_404(Idea,id=self.request.data['idea'])
        parent = self.request.data.get('parent')
        if parent is not None:
            # print("parent not None")
            # print("parent is",parent)
            # print("idea is",idea)
            comment_parent = get_object_or_404(Comment,id = parent,idea=idea)            
            recep_id = comment_parent.user_id 
        else:
            recep_id = None            
        serializer.save(user=self.request.user,idea=idea,reply_to_id=recep_id)

        
        # serializer.save(user=self.request.user,idea=idea)

    def perform_destroy(self, instance):
        #   body of the comment deleted; boolean deleted => True
        # but prev content gets saved in attr deleted content
        instance.deleted_content = instance.body
        instance.body="" 
        instance.deleted = True       
        instance.save()
        
    


class CommentListView(ListAPIView):
    """ get list of comments"""
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)
    filter_backends = [ OrderingFilter]
    ordering_fields = ('created_at')
    # This will be used as the default ordering
    ordering = ('created_at',) 
    pagination_class = None  
    

    def get_queryset(self, queryset=None):
        idea_slug = self.kwargs.get('slug')
        idea = get_object_or_404(Idea, slug=idea_slug)
        queryset = Comment.objects.filter(idea=idea).select_related('idea')
        
        # print("length qs is", queryset.count())
        # ? for each obj Comment.objects.get_descendants(Comment.objects.filter(idea=idea),include_self=True).select_related('user', 'parent', 'idea')
        
        return queryset
