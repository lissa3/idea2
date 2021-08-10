from django.db import models
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from mptt.models import MPTTModel, TreeForeignKey
from ideas.models import Idea
from timestamp.models import TimeStamp

User = get_user_model()

class CommentManager(models.Manager):
    # even if it's empty <class 'mptt.querysets.TreeQuerySet'>|=> queryset
    pass

class Comment(TimeStamp, MPTTModel):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    # tree structure
    parent = TreeForeignKey("self",
                            on_delete=models.SET_NULL,
                            null=True,
                            blank=True,
                            related_name="children"
                            )
    # record second comments to whom,str
    reply_to = models.ForeignKey(User,
                                 null=True,
                                 blank=True,
                                 on_delete=models.CASCADE,
                                 related_name='reply_ers'
                                 )

    banned = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    objects = CommentManager() # even if it's empty <class 'mptt.querysets.TreeQuerySet'>|=> queryset

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self):
        return self.body[:15]


"""
following data passed as an obj to ser-er list
line 35 ['DoesNotExist', 'Meta', 'MultipleObjectsReturned', 
 'banned',
  'body', 
  'check', 
  'children', 
  'clean', 
  'clean_fields', 'created_at', 'date_error_message', 'delete', 'deleted', 'from_db', 'full_clean', 'get_ancestors', 'get_children', 'get_deferred_fields', 'get_descendant_count', 'get_descendants', 'get_family', 'get_leafnodes', 'get_level', 'get_next_by_created_at', 'get_next_by_updated_at', 'get_next_sibling', 'get_previous_by_created_at', 'get_previous_by_updated_at', 'get_previous_sibling', 'get_root', 'get_siblings', 'id', 'idea', 'idea_id', 'insert_at', 'is_ancestor_of', 'is_child_node', 'is_descendant_of', 'is_leaf_node', 'is_root_node', 'level', 'lft', 'move_to', 'objects', 'parent', 'parent_id', 'pk', 'prepare_database_save', 'refresh_from_db', 'reply_to', 'reply_to_id', 'rght', 'save', 'save_base', 'serializable_value', 'tree_id', 'unique_error_message', 'updated_at', 'user', 'user_id', 'validate_unique']
"""        