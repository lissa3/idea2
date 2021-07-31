# from django.db.models import query
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status


from taggit.models import Tag

from api.serializers.categs.categ_ser import CategorySerializer,CategoryNameSerializer
from api.serializers.tags.tags_ser import TagSerializer
from api.serializers.ideas.idea_ser import IdeaSerializer
from api.serializers.account.profile_serializer import ProfileSerializer,ProfilePublicSerializer
# from api.serializers.account.user_serializer import UserSerializer

from ideas.models import Category, Idea
from profiles.models import Profile
from .permissions import IsOwnerOrIsStaff

User  = get_user_model()

# Categories

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
    print("inside view")

    def get_queryset(self, queryset=None):
        # print("view for cats works with qs:", Category.objects.all())
        return Category.objects.all()
        # return queryset
#       # return queryset.get_cached_trees()

class IdeasPerCategListView(generics.ListAPIView):
    """ retrieve all ideas linked to the category;
    for tests pagination_class = None
    """
    serializer_class = IdeaSerializer
    # pagination_class = None
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        categ = get_object_or_404(Category, slug=slug)
        # qs = Idea.objects.filter(categ = categ)
        # print("qs",qs)
        if categ.children:
            categ_descend = categ.get_descendants(include_self=True)
            qs = Idea.objects.filter(categ__in =categ_descend)
        else:
            qs = Idea.objects.filter(categ=categ)    
        return qs    

# Tags (thir party taggit)

class TagList(generics.ListAPIView):
    """ get list of tags"""
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class=None

    def get_queryset(self, queryset=None):
        return Tag.objects.all()


class TagIdeasListSlug(generics.ListAPIView):
    """ get list of ideas based on a tag's slug"""
    serializer_class = IdeaSerializer
    permission_classes = (AllowAny,)
    # pagination_class = CustomPaginationIdeas

    def get_queryset(self):
        # print("inside  tag view on idea slug")
        slug = self.kwargs.get('slug')
        if slug is not None:
            # result = Idea.objects.filter(tags__slug__in=(slug,))
            # print("result is", result)
            return Idea.objects.filter(tags__slug__in=(slug,))
        else:
            return Response(status=400)
            
class TagIdeasListName(generics.ListAPIView):
    """ get list of tags via names"""
    serializer_class = IdeaSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        name = self.kwargs.get('name')
        if name is not None:
            print("server got a tag:", name)
            print("founs following ideas for this tag", Idea.objects.filter(tags__name__in=(name,)))

            return Idea.objects.filter(tags__name__in=(name,))
        else:
            return Response(status=400)            

# Profile

class ProfileRetrView(generics.RetrieveAPIView):
    """return profile info for public view"""
    serializer_class = ProfilePublicSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        return  Profile.objects.annotate(
                count_following=Count('following'),
                
                )           

class ProfileRetrUpdateDestrView(generics.RetrieveUpdateDestroyAPIView):
    """profile info for private use:
       readOnly: name,
       can be changed: bio,website, image
    """
    serializer_class = ProfileSerializer #ProfileSerializer
    permission_classes = (IsOwnerOrIsStaff,)
    queryset = Profile.objects.all()
    parser_classes = (FormParser, MultiPartParser)

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super().__init__(*args, **kwargs)

    def get_object(self):
        try:
            """ checking of the user is banned = here """
            # print("req data", self.request.data)
            # print("in kwargs unid:", self.kwargs.get('unid'))
            obj = get_object_or_404(
                self.queryset,
                unid=self.kwargs.get('unid'),
            )
            # print("profile object is ", obj)
            self.check_object_permissions(self.request, obj)
        except APIException:
            # TODO log attempt to get to this point
            print("fighting with perms")
            raise PermissionDenied
            # return

        return obj

    def update(self, request, *args, **kwargs):
        """let op: don't save twice to avoid err msg: file not img||corrupt"""
        partial = kwargs.pop('partial', False)
        profile = self.get_object()
        print("server got the following data:", request.data)
        serializer = self.get_serializer(profile, data=request.data, partial=partial)
        print("is ser-er valid?")
        if serializer.is_valid():
            print("ser-er is valid")
            # print("img attr in ser-er", serializer.data['image'])
            # print('img data', serializer.data['image'])
        else:
            # print("data", serializer.data)
            print("ser errors:", serializer.errors)
            # {'linkedin': [ErrorDetail(string='Enter a valid URL.', code='invalid')]}
            return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        print("yes,ser-er valid")
        self.perform_update(serializer)
        return Response(serializer.data)



from rest_framework_simplejwt.tokens import RefreshToken

class UserDeleteAPIView(APIView):
    print("inside user delete view")
    permission_classes = (IsAuthenticated,)
    def delete(self, request,format=None):
        try:
            # User.objects.filter(id=request.user.id).delete()   
            user = User.objects.filter(id=request.user.id).last()  
            user.is_active = False 
            user.save()
            return Response({'success':'Successfully deleted user acoount'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error':'Failed to delete user account'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)   

"""
{'_state': <django.db.models.base.ModelState object at 0x7fae19f4acd0>, 'id': 5, 'created_at': datetime.datetime(2021, 6, 21, 9, 14, 36, 816249, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 6, 21, 11, 57, 14, 263355, tzinfo=<UTC>), 'user_id': 1, 'unid': 'abcT3', 'image': '', 'bio': '', 'website': 'http://www.snork.com', 'badge_bg': '(119,174,139)', 'countFolow': 0}

{'_state': <django.db.models.base.ModelState object at 0x7fae19f59100>, 'id': 1, 'created_at': datetime.datetime(2021, 6, 21, 8, 50, 23, 764715, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 6, 21, 8, 50, 23, 764751, tzinfo=<UTC>), 'user_id': 2, 'unid': 'XBVDg', 'image': '', 'bio': '', 'website': '', 'badge_bg': '(42,101,35)', 'countFolow': 0}

{'_state': <django.db.models.base.ModelState object at 0x7fae19f591f0>, 'id': 2, 'created_at': datetime.datetime(2021, 6, 21, 8, 53, 27, 979333, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 6, 21, 8, 53, 27, 979447, tzinfo=<UTC>), 'user_id': 3, 'unid': 'rlpIT', 'image': '', 'bio': '', 'website': '', 'badge_bg': '(75,84,241)', 'countFolow': 0}

{'_state': <django.db.models.base.ModelState object at 0x7fae19f592e0>, 'id': 4, 'created_at': datetime.datetime(2021, 6, 21, 9, 1, 7, 173459, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 6, 21, 9, 1, 7, 173494, tzinfo=<UTC>), 'user_id': 5, 'unid': 'kscv4', 'image': '', 'bio': '', 'website': '', 'badge_bg': '(42,140,238)', 'countFolow': 0}


{'_state': <django.db.models.base.ModelState object at 0x7fae19f593d0>, 'id': 6, 'created_at': datetime.datetime(2021, 6, 21, 22, 29, 31, 659766, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 7, 28, 12, 25, 57, 260303, tzinfo=<UTC>), 'user_id': 6, 'unid': 'kmuX5', 'image': '', 'bio': 'love fun, parties and so on', 'website': 'http://mumla-fun.nk', 'badge_bg': '(95,35,150)', 'countFolow': 4}


{'_state': <django.db.models.base.ModelState object at 0x7fae19f594c0>, 'id': 7, 'created_at': datetime.datetime(2021, 7, 6, 21, 27, 51, 232186, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 7, 6, 21, 27, 51, 232225, tzinfo=<UTC>), 'user_id': 7, 'unid': 't7ZK4', 'image': '', 'bio': '', 'website': '', 'badge_bg': '(11,183,35)', 'countFolow': 0}
{'_state': <django.db.models.base.ModelState object at 0x7fae19f595b0>, 'id': 8, 'created_at': datetime.datetime(2021, 7, 27, 10, 37, 36, 659202, tzinfo=<UTC>), 'updated_at': datetime.datetime(2021, 7, 27, 10, 37, 36, 659291, tzinfo=<UTC>), 'user_id': 8, 'unid': 'WU7c1', 'image': '', 'bio': '', 'website': '', 'badge_bg': '(210,52,155)', 'countFolow': 0}
"""