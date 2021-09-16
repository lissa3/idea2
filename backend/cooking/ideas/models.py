from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.storage import default_storage as storage
from django.core.validators import FileExtensionValidator

from mptt.models import MPTTModel, TreeForeignKey
from autoslug import AutoSlugField
from taggit.managers import TaggableManager

from timestamp.models import TimeStamp
from timestamp.broadcast_utils.idea_utils import upload_img
from timestamp.broadcast_utils.base_utils import get_random_str
from timestamp.broadcast_utils.validators import validate_size

# from django.core.exceptions import ValidationError
# from django.core.files.images import get_image_dimensions


ALLOWED_EXTENTIONS = ('JPG', 'JPEG', 'PNG')

User = get_user_model()

import logging
logger = logging.getLogger('django')

class CategoryManager(models.Manager):
    pass
    # def get_category_count(self):
    #     ''' make qs ready for iter-n through objects - objects.count
    #         to display total posts for each category
    #     '''
    #     return Category.objects.annotate(count=Count('ideas'))


class Category(MPTTModel):
    name = models.CharField(max_length=120, unique=True)
    # name = models.CharField(max_length=120, unique=True,db_index=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            null=True,
                            blank=True,
                            db_index=True,
                            related_name='children'
                            )
    objects = CategoryManager()

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('ideas:ideas-per-cat', args=[str(self.slug)])

    # def get_full_name(self):
    #     names = self.get_ancestors(include_self=True).values('name')
    #     full_name = ' - '.join(map(lambda x: x['name'], names))
    #     return full_name

    # def get_group_count(self):
    #     cats = self.get_descendants(include_self=True)
    #     return Group.objects.filter(categories__in=cats).count()


class IdeaManager(models.Manager):
    pass

    # def search(self,words):
    #     '''can be used for no results of first-line-search based on title,overview '''
    #     lookup = ( models.Q(content__icontains=words)|
    #                 models.Q(tags__name__icontains=words)
    #                 )
    #     #print(Idea.objects.filter(lookup).distinct())
    #     return Idea.objects.filter(lookup).distinct()


PROGR = 0
REVIEW = 1
PUB = 3


class Idea(TimeStamp):
    STATUS_CHOICES = (
        (PROGR, 'in progres'),
        (REVIEW, 'in review'),
        (PUB, 'published')
    )

    # class Idea(TimeStamp,models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    # TreeForeignKey
    categ = TreeForeignKey(Category,
                           related_name='ideas',
                           on_delete=models.PROTECT,
                           )
    title = models.CharField(max_length=240)
    slug = models.SlugField(max_length=255, blank=True, unique=True)
    lead_text = models.CharField(max_length=254,default="")
    main_text = models.TextField()
    view_count = models.IntegerField(blank=True, default=0)
    thumbnail = models.ImageField(blank=True, null=True, upload_to=upload_img,
                                  validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENTIONS), validate_size])

    featured = models.BooleanField(blank=True, default=False)
    # TODO: do I need it?
    fans = models.ManyToManyField(User, related_name='idea_fans', through='UserIdeaRelation')
    is_public = models.BooleanField(default=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    tags = TaggableManager(blank=True, verbose_name="Tags", help_text="Tags should be separated by comma")
    # two cached fields (db calc only if like,rating gets updated)
    avg_rate = models.DecimalField(decimal_places=2,max_digits=5,default=None,null=True)
    an_likes = models.IntegerField(default=None,null=True)
    max_rating = models.DecimalField(decimal_places=2,max_digits=5,default=None,null=True)
    remove_file = models.BooleanField(default=False)

    objects = IdeaManager()

    def __str__(self):
        return self.title 

    def get_absolute_url(self):
        return reverse('ideas:detail', kwargs={'slug': self.slug})

    def save(self,*args,**kwargs):
        """
        try to catch bug with idea formed without slug
        """
        start_creating = not self.pk
        if start_creating:
            try:                
                super().save(*args,**kwargs)                
                if not self.slug:
                    self.slug = get_random_str(10)
                    self.save()  
            except Exception as e:
                logger.warning(f'Failed creating idea with exception {e}')                
            else:
                logger.info(f'Idea object created id: {self.id}')          
            finally:
                pass
        else:
            super().save(*args,**kwargs)    
    
         

    


class UserIdeaRelation(models.Model):
    """ rating here stores value, idea attr rating calc avg and chach it in .save() Idea"""
    RATING = (
        (1, 'OK'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Excellent')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    like = models.BooleanField(blank=True, default=False)
    dislike = models.BooleanField(blank=True, default=False)
    in_bookmark = models.BooleanField(blank=True, default=False)
    rating = models.PositiveSmallIntegerField(choices=RATING, null=True, blank=True)
    # follow = models.BooleanField(blank=True,default=False)

    def __str__(self):
        return f'User: {self.user} active in user-idea-relations {self.like}, {self.rating}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_rating = self.rating
        self.old_like = self.like
        
    

    def save(self,*args,**kwargs):
        """ import here to avoide circular import (idea-user-relation calls idea-user-relation)"""
        from .logic import calc_rating,calc_count_likes,calc_max_rating
        # if like or rating changed |=> re-calc total likes on idea
        start_creating = not self.pk
        super().save(*args,**kwargs) # here idea gets (if triggered by change rating event) 
        new_rating = self.rating
        new_like = self.like
        
        if self.old_rating!=new_rating or start_creating:
            # print("obj is already exist,so working on condition old!=new")
            calc_rating(self.idea)
            calc_max_rating(self.idea)            
              
        if self.old_like != new_like or start_creating:
            # print("user-idea-rel is just created< see calc")           
            calc_count_likes(self.idea)
            

        




    

