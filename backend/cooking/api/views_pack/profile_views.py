# from django.db.models import query
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
import logging

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken (GOOD TO HAVE delete profile)
# from rest_framework.generics import DestroyAPIView

from api.serializers.account.user_serializer import UserSerializer
from api.serializers.account.profile_serializer import ProfileSerializer 
from api.permissions import IsOwnerOrIsStaffOrReadOnly,IsOwnerOrIsStaff 
from timestamp.broadcast_utils.user_utils import get_ip
# from api.serializers.account.user_serializer import UserSerializer

User = get_user_model()
logger = logging.getLogger('user_issues')

from profiles.models import Profile
User  = get_user_model()

class ShowFollowingRetrView(APIView):
    """return a list of people who are followed by a given person(for both public AND private view)"""
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
            # print(followers)
            profiles = ProfileSerializer(followers,many=True)
            return Response({'data':profiles.data},status=status.HTTP_200_OK)
        except:
            return Response({'error':'List followers not found'},status=status.HTTP_404_NOT_FOUND)

class ProfileRetrView(generics.RetrieveAPIView):
    """return profile info for public view"""
    serializer_class = ProfileSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        print("public profile info: qs")
        return  Profile.objects.select_related('user').prefetch_related('following')
        # return  Profile.objects.annotate(count_following=Count('following')).select_related('user').prefetch_related('following')
    
    
class ProfileRetrUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """profile info for private use:
       request should be via form because of option upload profile image 
       readOnly attr: name,
       writable/changable attr's: bio,website, image
    """
    serializer_class = ProfileSerializer #ProfileSerializer
    permission_classes = (IsOwnerOrIsStaffOrReadOnly,)
    queryset = Profile.objects.all()
    parser_classes = (FormParser, MultiPartParser)
    
    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super().__init__(*args, **kwargs)

    def get_object(self):
        """ TODO in logs:status 405 if attempt to del account via this route"""
        try:
            """ can check user is banned here """
            print("view line 85: in kwargs unid:", self.kwargs.get('unid'))
            obj = get_object_or_404(
                Profile,
                unid=self.kwargs.get('unid'),
            )
            print("view line 90 object is",obj)
            remote_address = get_ip(self.request)
            self.check_object_permissions(self.request, obj)
            logger.info(f'accessed by id: {remote_address} OK')
            
        # except APIException:
        except Exception as e:
            unid = self.kwargs.get('unid')
            print("view line 98 unid",unid)
            # remote_address = get_ip(self.request)
            # logger.warning(
            #     f'user  id {self.request.user.id} from IP: {remote_address} tried to  retrieve another profile unid: {unid} \ : {e}')
            raise PermissionDenied
        finally:
            pass  
        return obj
    def delete(self, request, *args, **kwargs):     
        """ change user.is_active =False to delete object(both profile and user
        idea obj and comment => DO_NOTHING""" 
        try:
            print("inside delete view with kwargs",kwargs)
            # User.objects.filter(id=request.user.id).delete() 
            unid = kwargs.get('unid') 
            print("view line 113",unid)
            profile = get_object_or_404 (Profile,unid=unid)  
            print("line 115 found profile with unid",profile)
            user = profile.user 
            print("user for this profile is",user)
            user_deleted_id = user.id
            print("user ot delete id",user_deleted_id)
            user.delete()   
            print("Done???????????????")    
            remote_address = get_ip(self.request)
            print("remote addr",remote_address)
            logger.warning(f'User id {user_deleted_id} deleted his profile from IP:{remote_address}')            
            return Response({'success':'Successfully deleted user acoount'},status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error':'user does not exist'},status = status.HTTP_404_NOT_FOUND)   
        except Exception as e:
            print("exception block")
            logger.error(f'500 ERROR: Failed to delete user id: {user_deleted_id} {e}')
            return Response({'error':'Failed to delete user account'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)            
                  

    def update(self, request, *args, **kwargs):
        """let op: don't save twice to avoid err msg: file not img||corrupt"""
        setattr(request.data, '_mutable', True)
        img = request.data.get('image')
        # print("img is",img)        
        # print("type img line 244 from front : ",type(img))
        if type(img) == str and len(img)!=0:
            # print('line 107: looks like img is url str')             
            request.data.pop('image')
        # no img from front: thumbnail': ['']}|=> thumbnail = empty string     
        if type(img) == str and len(img)==0:
            print('line 250: looks like img is empty str')
            request.data['remove_file'] = True
            
        if type(img) != str:
            # img from front: thumbnail: [<InMemoryUploadedFile: one.jpg (application/octet-stream)>]
            request.data['remove_file'] = True
            # print('line 256: looks like img is real img upload')  
            
        partial = kwargs.pop('partial', False)
        profile = self.get_object()
        # print("line 260 server got data:", request.data)
        serializer = self.get_serializer(profile, data=request.data, partial=partial)
        # print("is ser-er valid?")
        if serializer.is_valid():
            print("ser-er is valid")
            # print("img attr in ser-er", serializer.data['image'])
            # print('following this user', serializer.data['image'])
        else:
            # print("data", serializer.data)
            # print("ser errors:", serializer.errors)
            # {'linkedin': [ErrorDetail(string='Enter a valid URL.', code='invalid')]}
            return Response(serializer.errors, status=400)
        serializer.is_valid(raise_exception=True)
        # print("yes,ser-er valid")
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

    

# class UserDeleteAccountAPIView(DestroyAPIView):
#     print("AAAAAAAAAAAAAAAAAAAAAAA inside user delete view")
#     permission_classes = (IsOwnerOrIsStaff,)

#     def _allowed_methods(self):
#         print ([m.upper() for m in self.http_method_names if hasattr(self, m)])
#         return [m.upper() for m in self.http_method_names if hasattr(self, m)]

    # def delete(self, request,format=None):    
    #     print("line 187",self.kwargs)    
    #     print("line 188",request.data)    
    #     unid = self.kwargs.get('unid')
    #     # unid = request.data.get('unid',"no unid in data") 
    #     print("where is my UNIDDDDDDDDDDDDDDDDD",unid)
        
    #     try:
    #         # User.objects.filter(id=request.user.id).delete()   
    #         user = User.objects.filter(id=request.user.id).last()  
    #         user.is_active = False 
    #         user.save()
    #         remote_address = get_ip(self.request)
    #         logger.warning(f'User id {user.id} deleted his profile from IP:{remote_address}')            
    #         return Response({'success':'Successfully deleted user acoount'},status=status.HTTP_204_NO_CONTENT)
    #     except Exception as e:
    #         print("where am I??????????")
    #         logger.error(f'Let op: permission denied for user with id {self.request.user.id} to delete profile unid: {unid} from IP: {remote_address}: {e}')
    #         logger.error(f'500 ERROR: Failed to delete user {user}')
    #         return Response({'error':'Failed to delete user account'},status = status.HTTP_500_INTERNAL_SERVER_ERROR)  

"""
req dict { 'parser_context': {'view': <api.views_pack.profile_views.ProfileRetrUpdateDestroyView object at 0x7f1b8e3b6880>, 'args': (), 'kwargs': {'unid': 'vqrqa'}, 'request': <rest_framework.request.Request: DELETE '/api/v1/profile-owner/vqrqa/'>, 'encoding': 'utf-8'}, '_data': <class 'rest_framework.request.Empty'>, '_files': <class 'rest_framework.request.Empty'>, '_full_data': <class 'rest_framework.request.Empty'>, '_content_type': <class 'rest_framework.request.Empty'>, '_stream': <class 'rest_framework.request.Empty'>, 'accepted_renderer': <rest_framework.renderers.JSONRenderer object at 0x7f1b8cbed790>, 'accepted_media_type': 'application/json', 'version': None, 'versioning_scheme': None, '_authenticator': <rest_framework.request.ForcedAuthentication object at 0x7f1b8cbed970>, '_user': <User: nick>, '_auth': None}

req dict ['DATA', 'FILES', 'POST', 'QUERY_PARAMS', '__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_auth', '_authenticate', '_authenticator', '_content_type', '_data', '_default_negotiator', '_files', '_full_data', '_load_data_and_files', '_load_stream', '_not_authenticated', '_parse', '_request', '_stream', '_supports_form_parsing', '_user', 'accepted_media_type', 'accepted_renderer', 'auth', 'authenticators', 'content_type', 'data', 'force_plaintext_errors', 'negotiator', 'parser_context', 'parsers', 'query_params', 'stream', 'successful_authenticator', 'user', 'version', 'versioning_scheme']

"""






