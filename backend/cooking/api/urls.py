from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import (
                    CatListIdeaForm,CategoryList,
                    ProfileRetrUpdateDestrView,ProfileRetrView,
                    IdeasPerCategListView,IdeasPerCategListView,IdeasFollowing,
                    TagList, TagIdeasListSlug, TagIdeasListName, 
                    UserDeleteAPIView, ShowFollowingRetrView,
                    RetrieveFollowers,UnFollowUser,FollowAuthorView                            
                    #FollowAuthorView
                    )
from api.viewsets import IdeaViewSet, IdeaRelations

router = routers.DefaultRouter()

router.register(r'relations', IdeaRelations) #,basename='useridearelation')
router.register(r'ideas', IdeaViewSet, basename="idea")

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories-create-idea/', CatListIdeaForm.as_view(), name='category-create-idea'),
    path('cats/<slug>/', IdeasPerCategListView.as_view(), name="cat-per-idea"),
    path('ideas-collection/', include(router.urls)),
    path('feed-ideas/<unid>/',IdeasFollowing.as_view(),name='user-following-ideas'),
    # private api for profile,userinfo (profile + user)
    path('profile-owner/<unid>/', ProfileRetrUpdateDestrView.as_view(), name="profile-owner"),
    # public api profile
    path('profile-info/<pk>/', ProfileRetrView.as_view(), name="profile-info"),
    # tags
    path('tags/', TagList.as_view(), name="tags-list"),
    path('tags/<slug>/', TagIdeasListSlug.as_view(), name="tag-per-ideas-slug"),
    # TODO: may be all should be name?
    path('tags-name/<name>/', TagIdeasListName.as_view(), name="tag-per-ideas-name"),
    # user account delete
    path('delete-account/',UserDeleteAPIView.as_view(),name="delete-account"),
    # following smb
    path('following/<unid>/',ShowFollowingRetrView.as_view(),name='show-following'),
    path('followers/<id>/',RetrieveFollowers.as_view(),name='show-followers'), # add follow
    path('unfollow/',UnFollowUser.as_view(),name='unfollow-user'),
    path('add-following/',FollowAuthorView.as_view(),name='add-to-following')
]

