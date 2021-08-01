from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.models import When, Case, Count, Avg,Max
# from django.core.exceptions import ValidationError


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

from ideas.models import Idea, UserIdeaRelation

from api.serializers.ideas.idea_ser import IdeaSerializer
from api.serializers.user_idea_rel.user_idea_relation_ser import UserIdeaRelSerializer
from timestamp.broadcast_utils.idea_utils import get_json_tags, checkTagStringLength
from .permissions import IsAuthorOrIsStaffOrReadOnly

User = get_user_model()


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
        print("object created or updated", obj)
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
    permission_classes = (IsAuthorOrIsStaffOrReadOnly,)
    lookup_field = 'slug'
    parser_classes = (FormParser, MultiPartParser)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['featured','view_count']
    search_fields = ['title', 'lead_text', 'main_text']
    # Explicitly specify which fields the API may be ordered against
    ordering_fields = ('title', 'created_at','max_rating')
    # This will be used as the default ordering
    ordering = ('-created_at',)   
    

    def get_queryset(self):
        # let op: 2 times qs:? |=> distinct() in postgres
        queryset = Idea.objects.annotate(
            an_likes=Count(Case(When(useridearelation__like=True, then=1))),
            avg_rate=Avg('useridearelation__rating'),
            max_rating=Max('useridearelation__rating')
            )
        # print("qs",queryset)    
        return queryset    
    def update(self, request, *args, **kwargs):
        """let op: don't save twice to avoid err msg: file not img||corrupt"""

        idea = self.get_object()
        setattr(request.data, '_mutable', True)
        tags = request.data.get('tags')
        if tags is not None:
            # print("server got the following tags", tags)
            if checkTagStringLength(tags):
                return Response({"detail": "tag string is too long; shouls be max 50 chars"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                request.data['tags'] = get_json_tags(tags)
                setattr(request.data, '_mutable', False)

        serializer = self.get_serializer(idea, data=request.data)
        if serializer.is_valid():
            pass
        else:
            return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        # print("yes,ser-er valid")
        self.perform_update(serializer)
        return Response(serializer.data)
        # from taggit error{"tags": ["Invalid json list. A tag list submitted in string form must be valid json."]}

    def create(self, request, *args, **kwargs):
        """ create object but before adding auth user to request.data and clean tags input before adding them to data"""
        # print("check where i am.................")
        setattr(request.data, '_mutable', True)
        tags = request.data.get('tags')
        if tags is not None:
            if checkTagStringLength(tags):
                return Response({"detail": "tag string is too long; shouls be max 50 chars"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                request.data['tags'] = get_json_tags(tags)
        setattr(request.data, '_mutable', False)
        return super().create(request, *args, **kwargs)