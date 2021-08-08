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
from api.serializers.comments.comment_ser import CommentSerializer,ListCommentSerializer
from .permissions import IsAuthorOrIsStaffOrReadOnly


User = get_user_model()

class CommentAPIView(CreateModelMixin,DestroyModelMixin,RetrieveModelMixin, UpdateModelMixin,viewsets.GenericViewSet):
    """create comment instance """
    permission_classes = (IsAuthorOrIsStaffOrReadOnly,)
    authentication_class = (IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        # print("req:",self.request.data)
        # {'body': 'Greet', 'idea': 7, 'parent': None}
        idea = get_object_or_404(Idea,id=self.request.data['idea'])
        serializer.save(user=self.request.user,idea=idea)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()

    def _allowed_methods(self):
        print([m.upper() for m in self.http_method_names if hasattr(self, m)])
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]    

class CommentListView(ListAPIView):
    """ get list of comments"""
    serializer_class = ListCommentSerializer
    permission_classes = (AllowAny,)
    filter_backends = [ OrderingFilter]
    ordering_fields = ('created_at')
    # This will be used as the default ordering
    ordering = ('created_at',) 
    pagination_class = None  
    

    def get_queryset(self, queryset=None):
        idea_slug = self.kwargs.get('slug')
        idea = get_object_or_404(Idea, slug=idea_slug)
        queryset = Comment.objects.filter(idea=idea)
        print("length qs is", queryset.count())
        # queryset = Comment.objects.get_descendants(Comment.objects.filter(idea=idea),include_self=True).select_related('user', 'parent', 'idea')
        return queryset
