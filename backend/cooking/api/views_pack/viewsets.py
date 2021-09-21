from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models import Count
# from django.core.exceptions import ValidationError
import logging
# import base64


from rest_framework import viewsets  # , permissions
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter # built-in filters
from rest_framework.mixins import UpdateModelMixin,RetrieveModelMixin
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend # third party
# from api.filters import IdeaFilter


from api.serializers.ideas.idea_ser import IdeaSerializer
from api.serializers.user_idea_rel.user_idea_relation_ser import UserIdeaRelSerializer
from api.permissions import IsAuthorOrIsStaffOrReadOnly #IsOwnerOrIsStaffOrReadOnly
from timestamp.broadcast_utils.idea_utils import get_json_tags, checkTagStringLength
from ideas.models import Idea, UserIdeaRelation

User = get_user_model()
logger = logging.getLogger('django')


# TODO: make separ view list idea?
# to prevent headers author-n check?
# premission_class = ['AllowAny']; now simpleAPI vs getAPI



class IdeaRelations(RetrieveModelMixin,UpdateModelMixin,viewsets.GenericViewSet):
    """"""
    queryset = UserIdeaRelation.objects.all()
    serializer_class = UserIdeaRelSerializer
    lookup_field = 'idea'
    permission_classes = (IsAuthenticated,)
    pagination_class=None

    def get_object(self):
        # print("data from vue.js is", self.request.data)
        # print("user is", self.request.user)
        # print("idea", self.kwargs.get('idea'))
        obj, _ = UserIdeaRelation.objects.get_or_create(idea_id=self.kwargs['idea'], user=self.request.user)
        # print("object created or updated in viewset idea-user-rel", obj)
        return obj
         

class IdeaViewSet(viewsets.ModelViewSet):
    """ custom filter:'title','categ','featured','status','author;
    odrering default: -created at = newest on top
    pagination for tests should be off
    """
    # TODO: clearify why this doesn't work out (see default pag's in settings)
    # pagination_class=LimitOffsetPagination
    # PAGE_SIZE = 6
    serializer_class = IdeaSerializer
    permission_classes = (IsAuthorOrIsStaffOrReadOnly,) #IsOwnerOrIsStaffOrReadOnly)
    lookup_field = 'slug'
    parser_classes = (FormParser, MultiPartParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['featured','view_count']
    search_fields = ['title', 'lead_text', 'main_text']
    # Explicitly specify which fields the API may be ordered against
    ordering_fields = ('title', 'created_at','max_rating')
    # This will be used as the default ordering
    ordering = ('-created_at',)  
    
    # for dev
    # def get_queryset(self):
    #     # let op: 2 times qs:? |=> distinct() in postgres        
    #     queryset = Idea.objects.select_related('author','categ').prefetch_related('tags')
    #     # print("viewset made qs:",queryset)  
    #     return queryset 

    # for postgresql   in prod  
    def get_queryset(self):
        # let op: 2 times qs:? |=> distinct() in postgres        
        queryset = Idea.objects.annotate(
            users_comments=Count('comments',distinct=True)
            ).select_related('author','categ').prefetch_related('tags')
        # print("viewset made qs:",queryset)    
        return queryset 

    def update(self, request, *args, **kwargs):
        """let op: don't save twice to avoid err msg: file not img||corrupt
        thumbnail may come from front:
        1. as empty string = not img attached or removed
        2. as string = url of aws s3
        3. as InMemoryUploadedFile which needs validation by ser-er      
        '_auth', '_authenticate', '_authenticator', '_content_type', '_data', '_default_negotiator', '_files', '_full_data', '_load_data_and_files', '_load_stream', '_not_authenticated', '_parse', '_request', '_stream', '_supports_form_parsing', '_user', 'accepted_media_type', 'accepted_renderer', 'auth',   
        """       
        idea = self.get_object()
        setattr(request.data, '_mutable', True)
        # print("editing an idea",request.data)
        # request.data.get('thumbnail')) #'thumbnail': ['']}
        # from vue data https://boterland.s3.amazonaws.com/ideapot/idea_1/lemon1630705942.9574196.jpg
        thumbnail = request.data.get('thumbnail')
        # if thumbnail == "":
        #     print("thumbnail is empty str")
        # else:
        #     print("thumbnail is not an empty str",thumbnail)           
        # print("type thumb line 107 from front : ",type(thumbnail))
        if type(thumbnail) == str and len(thumbnail)!=0:
            print('line 107: looks like img is url str')             
            request.data.pop('thumbnail')
            # logger.warning('thumbnail file is aws s3 url,cutting if from request; rest goes to ser-er')
        # no img from front: thumbnail': ['']}|=> thumbnail = empty string     
        if type(thumbnail) == str and len(thumbnail)==0:
            # print('line 111: looks like img is empty str')
            request.data['remove_file'] = True
            # logger.warning('front:no thumbnail, empty string in request')            
        if type(thumbnail) != str:
            # img from front: thumbnail: [<InMemoryUploadedFile: one.jpg (application/octet-stream)>]
            request.data['remove_file'] = True
            # logger.warning('thumbnail is a real img')           
        tags = request.data.get('tags')
        if tags is not None:
            # print("server got the following tags", tags)
            if checkTagStringLength(tags):
                logger.warning(f'status 400: user {self.user.id} loads too long tags')
                return Response({"detail": "tag string is too long; shouls be max 50 chars"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                request.data['tags'] = get_json_tags(tags)
                setattr(request.data, '_mutable', False)

        serializer = self.get_serializer(idea, data=request.data)
        if serializer.is_valid():
            pass
        else:
            logger.warning(f'status 400: {self.user.id} ser-er idea not valid {serializer.errors}')
            return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        # print("yes,ser-er valid")
        self.perform_update(serializer)
        return Response(serializer.data)
        # from taggit error{"tags": ["Invalid json list. A tag list submitted in string form must be valid json."]}

    def create(self, request, *args, **kwargs):

        """ create object but before adding auth user to request.data and clean tags input before adding them to data"""
        print("create method calling: who is the user?",request.user)
        print("checking if user is banned",request.user.is_banned)

        if request.user.is_banned:
            logger.warning(f'status 403: banned user {request.user.id} create idea ')
            return Response({"error": "user is banned"}, status=status.HTTP_403_FORBIDDEN)

        setattr(request.data, '_mutable', True)
        tags = request.data.get('tags')
        if tags is not None:
            if checkTagStringLength(tags):
                logger.warning(f'status 400: user {request.user.id} loads too long tags')
                return Response({"detail": "tag string is too long; shouls be max 50 chars"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                request.data['tags'] = get_json_tags(tags)
        setattr(request.data, '_mutable', False)
        return super().create(request, *args, **kwargs)
    
    
