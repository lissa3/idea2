# from django.db.models import query
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken (GOOD TO HAVE delete profile)

from api.serializers.account.user_serializer import UserSerializer


User = get_user_model()


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
    # print("inside view")

    def get_queryset(self, queryset=None):
        # print("view for cats works with qs:", Category.objects.all())
        # print("categs view line 60")
        queryset = Category.objects.all()
        # print(type(Category.objects.all()))        
        return queryset
#       # return queryset.get_cached_trees()

class IdeasPerCategListView(generics.ListAPIView):
    """ retrieve all ideas linked to the category;
    for tests pagination_class = None
    """
    serializer_class = IdeaSerializer
    # pagination_class = None
    
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        print("got a categ with slug:",slug)
        categ = get_object_or_404(Category, slug=slug)
        qs2 = Idea.objects.filter(categ = categ)
        print("qs2",qs2)
        if categ.get_children():
            print("categ has children")
            print(categ.children.exists())
            categ_descend = categ.get_descendants(include_self=True)
            qs = Idea.objects.filter(categ__in =categ_descend)
        else:
            print("categ has no children")
            qs = Idea.objects.filter(categ=categ) 
            print("qs line 86 len",qs) 
        print("returning qs with len to tests",qs.count())      
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


class ShowFollowingRetrView(APIView):
    """return a list whom a given person is following (for both public AND private view)"""
    permission_classes = (AllowAny,)
    
    def get(self,request,unid,format=None):
        try:
            profile = get_object_or_404(Profile,unid=unid)
            users_to_follow = profile.following.all().order_by('username')
            users = UserSerializer(users_to_follow,many=True)
            return Response({'data':users.data},status=status.HTTP_200_OK)
        except:
            return Response({'error':'List not found'},status=status.HTTP_404_NOT_FOUND)

class RetrieveFollowers(APIView):
    """return a list of followers of a given person (for both public AND private view)"""
    permission_classes = (AllowAny,)
    
    def get(self,request,id,format=None):
        try:
            user = get_object_or_404(User,id=id)
            followers = user.followed_by.all()
            print(followers)
            profiles = ProfilePublicSerializer(followers,many=True)
            return Response({'data':profiles.data},status=status.HTTP_200_OK)
        except:
            return Response({'error':'List followers not found'},status=status.HTTP_404_NOT_FOUND)

class ProfileRetrView(generics.RetrieveAPIView):
    """return profile info for public view"""
    serializer_class = ProfilePublicSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        print("public profile info: qs")
        return  Profile.objects.annotate(count_following=Count('following')).select_related('user').prefetch_related('following')
    
    
class ProfileRetrUpdateDestrView(generics.RetrieveUpdateDestroyAPIView):
    """profile info for private use:
       request should be via form because of option upload profile image 
       readOnly attr: name,
       writable/changable attr's: bio,website, image
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
                Profile,
                unid=self.kwargs.get('unid'),
            )
            # print("profile object is ", obj)
            self.check_object_permissions(self.request, obj)
        except APIException:
            # TODO log attempt to get to this point
            print("fighting with perms")
            raise PermissionDenied
            

        return obj

    def update(self, request, *args, **kwargs):
        """let op: don't save twice to avoid err msg: file not img||corrupt"""
        partial = kwargs.pop('partial', False)
        profile = self.get_object()
        # print("server got the following data:", request.data)
        serializer = self.get_serializer(profile, data=request.data, partial=partial)
        print("is ser-er valid?")
        if serializer.is_valid():
            print("ser-er is valid")
            # print("img attr in ser-er", serializer.data['image'])
            # print('following this user', serializer.data['image'])
        else:
            # print("data", serializer.data)
            print("ser errors:", serializer.errors)
            # {'linkedin': [ErrorDetail(string='Enter a valid URL.', code='invalid')]}
            return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        print("yes,ser-er valid")
        self.perform_update(serializer)
        return Response(serializer.data)

class UnFollowUser(APIView):
    """auth-ed user can remove item from the list of following"""
    authentication_class = (IsAuthenticated,)
    permission_classes = (IsOwnerOrIsStaff,)

    def post(self,request):        
        try:
            user = request.user        
            person_to_unfollow_id = request.data.get('userId')        
            profile = get_object_or_404(Profile,id=user.id)
            user_obj_to_unfollow = get_object_or_404(User,id=person_to_unfollow_id)
            profile.following.remove(user_obj_to_unfollow)
            return Response({'success':'Successfully removed user to follow'},status=status.HTTP_200_OK)
        except:
            return Response({'error':'User is not found'},status=status.HTTP_404_NOT_FOUND)

class FollowAuthorView(APIView):
    """auth-ed user can add to 'following' :
    """
    authentication_class = (IsAuthenticated,)
    # permission_classes = (IsOwnerOrIsStaff,)

    def post(self,request):   
        print('line 241', request.data.get('authorId'))     
        try:
            user = request.user        
            person_to_follow_id = request.data.get('authorId')        
            profile = get_object_or_404(Profile,id=user.id)
            user_obj_to_follow = get_object_or_404(User,id=person_to_follow_id)
            print(profile,user_obj_to_follow)
            profile.following.add(user_obj_to_follow)
            return Response({'success':'Successfully added user to follow'},status=status.HTTP_200_OK)
        except:
            print('inside except in view')
            return Response({'error':'User is not found'},status=status.HTTP_404_NOT_FOUND)   

    


class UserDeleteAPIView(APIView):
    # print("inside user delete view")
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


class IdeasFollowing(ListAPIView):
    """list of ideas (user is following): newest on top"""
    serializer_class = IdeaSerializer
    # authentication_class = (IsAuthenticated,)
    ordering_fields = ('title', 'created_at','max_rating')
    # default ordering
    ordering = ('-created_at',)     
    
    def get_queryset(self):
        unid = self.kwargs.get('unid')        
        person = get_object_or_404(Profile,unid=unid)
        person_following_list = person.following.values_list('id',flat=True)
        qs = Idea.objects.filter(author_id__in=person_following_list)  
       
        return qs
        
   






