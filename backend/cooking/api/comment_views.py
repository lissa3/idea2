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
from .permissions import IsOwnerOrIsStaff


User = get_user_model()

class CommentAPIView(CreateModelMixin,DestroyModelMixin,RetrieveModelMixin, UpdateModelMixin,viewsets.GenericViewSet):
    """create comment instance """
    permission_classes = (IsOwnerOrIsStaff,)
    authentication_class = (IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    

    def perform_create(self, serializer):
        print("self is",self)
        print("self.data",self.request.data)
        print("line 35 inside perform create",self.request.data)
        user = self.request.user
        print("line 35",user)
        print("req:",self.request.data)
        # {'body': 'Greet', 'idea': 7, 'parent': None}
        idea = get_object_or_404(Idea,id=self.request.data['idea'])
        # print("line 37",idea)
        serializer.save(user=self.request.user,idea=idea)

    def perform_destroy(self, instance):
        instance.deleted = True
        instance.save()
    def perform_update(self, serializer):
        print("inside 50 line",self.request.data)
        serializer.save()

"""
 'action', 
 'action_map',
  'allowed_methods',
   'args',
    'as_view', 'authentication_class', 'authentication_classes', 'basename', 'check_object_permissions', 'check_permissions', 'check_throttles', 'content_negotiation_class', 'create', 'default_response_headers', 'delete', 'description', 'destroy', 'detail', 'determine_version', 'dispatch', 'filter_backends', 'filter_queryset', 'finalize_response', 'format_kwarg', 'get', 'get_authenticate_header', 'get_authenticators', 'get_content_negotiator', 'get_exception_handler', 'get_exception_handler_context', 'get_extra_action_url_map', 'get_extra_actions', 'get_format_suffix', 'get_object', 'get_paginated_response', 'get_parser_context', 'get_parsers', 'get_permissions', 'get_queryset', 'get_renderer_context', 'get_renderers', 'get_serializer', 'get_serializer_class', 'get_serializer_context', 'get_success_headers', 'get_throttles', 'get_view_description', 'get_view_name', 'handle_exception', 'head', 'headers', 'http_method_names', 'http_method_not_allowed', 'initial', 'initialize_request', 'kwargs', 'lookup_field', 'lookup_url_kwarg', 'metadata_class', 'name', 'options', 'paginate_queryset', 'pagination_class', 'paginator', 'parser_classes', 'partial_update', 'patch', 'perform_authentication', 'perform_content_negotiation', 'perform_create', 'perform_destroy', 'perform_update', 'permission_classes', 'permission_denied', 'put', 'queryset', 'raise_uncaught_exception', 'renderer_classes', 'request', 'retrieve', 'reverse_action', 'schema', 'serializer_class', 'settings', 'setup', 'suffix', 'throttle_classes', 'throttled', 'update', 'versioning_class']

"""        
        

    # def _allowed_methods(self):
    #     print([m.upper() for m in self.http_method_names if hasattr(self, m)])
    #     return [m.upper() for m in self.http_method_names if hasattr(self, m)]    

class CommentListView(ListAPIView):
    """ get list of comments"""
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)
    filter_backends = [ OrderingFilter]
    ordering_fields = ('created_at')
    # This will be used as the default ordering
    ordering = ('-created_at',) 
    pagination_class = None  
    

    def get_queryset(self, queryset=None):
        idea_slug = self.kwargs.get('slug')
        idea = get_object_or_404(Idea, slug=idea_slug)
        queryset = Comment.objects.filter(idea=idea)
        
        # print("length qs is", queryset.count())
        # ? for each obj Comment.objects.get_descendants(Comment.objects.filter(idea=idea),include_self=True).select_related('user', 'parent', 'idea')
        
        return queryset
