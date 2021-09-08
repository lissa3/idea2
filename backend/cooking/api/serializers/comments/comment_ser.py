from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers as ser
from comments.models import Comment


User = get_user_model()


class CommentSerializer(ser.ModelSerializer):
    """ serializer for creating-editing-deleting a comment"""    
    author_comment = ser.CharField(source='user.username',read_only=True)
    name_recepient = ser.SerializerMethodField()
    # body = ser.SerializerMethodField()
    # children = ser.SerializerMethodField(source='get_descendants')    
    class Meta:
        model = Comment
        fields = ('id','created_at','body','idea_id',
                'user_id','reply_to_id','parent','author_comment','deleted','name_recepient'
                
        )
    def get_name_recepient(self,obj):
        """return username of the user who got a reply"""
        try:
            if obj.parent is not None:
                return get_object_or_404(User,id=obj.reply_to_id).username              
        except:
            return  None
        finally:
            pass      
     
        
    
    # def get_children(self, obj):
    #     # children = self.context['children'].get(obj.id, [])
    #     serializer = CommentSerializer(obj.get_descendants(), many=True, context=self.context)
    #     return serializer.data
        

# class CategoryTreeSerializer(ModelSerializer):
#     children = SerializerMethodField(source='get_children')
#     class Meta:
#         fields = ('children',)  # add here rest of the fields from model 
 
#     def get_children(self, obj):
#         children = self.context['children'].get(obj.id, [])
#         serializer = CategoryTreeSerializer(children, many=True, context=self.context)
#         return serializer.data
 