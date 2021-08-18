from rest_framework import serializers as ser
from comments.models import Comment




class CommentSerializer(ser.ModelSerializer):
    """ serializer for creating-editing-deleting a comment"""    
    author_comment = ser.CharField(source='user.username',read_only=True)
    # children = ser.SerializerMethodField()
    # children = ser.SerializerMethodField(source='get_descendants')
    
    
    class Meta:
        model = Comment
        fields = ('id','created_at','body','idea_id',
                'user_id','reply_to_id','parent','author_comment',
                #'children'
        )
    
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
 