from django.urls import path, include
from rest_framework import routers
from api.views import (CatListIdeaForm,CategoryList,IdeasPerCategListView,ProfileRetrView,
                    ProfileRetrUpdateDestrView,IdeasPerCategListView,
                    TagList, TagIdeasListSlug, TagIdeasListName,  
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
    # api for profile,userinfo (profile + user)
    path('profile-owner/<unid>/', ProfileRetrUpdateDestrView.as_view(), name="profile-owner"),
    path('profile-info/<pk>/', ProfileRetrView.as_view(), name="profile-info"),
    # tags
    path('tags/', TagList.as_view(), name="tags-list"),
    path('tags/<slug>/', TagIdeasListSlug.as_view(), name="tag-per-ideas-slug"),
    # TODO: may be all should be name?
    path('tags-name/<name>/', TagIdeasListName.as_view(), name="tag-per-ideas-name"),
]