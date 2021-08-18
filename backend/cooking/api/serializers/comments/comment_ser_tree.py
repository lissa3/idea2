from rest_framework import serializers as ser
from comments.models import Comment

class FilterCommentListSerializer(ser.ListSerializer):
    """filter comments: front should get a list with only root comments"""
    def to_representation(self,objects):
        print("line 7objects",type(objects))
        # print("dict__",objects.__dict__)
        data = objects.filter(parent=None)
        return super().to_representation(data)

class RecursiveChildrenSerializer(ser.Serializer):
    """child should be serialized by CommentSer-er"""
    def to_representation(self, obj):  
        # print("line 14 obj:",obj)      
        serializer = self.parent.parent.__class__(obj)  
        # print("line 15",serializer.data)     
        return serializer.data

class ListCommentSerializer(ser.ModelSerializer):
    """ ser-er for a list with tree structure"""
    # each related object if parent has attr children == 'related name' from model FK
    # and will be ser-ed by CommentSerializer; you need children (no need parents) """
    author_comment = ser.CharField(source='user.username',read_only=True)
    children = RecursiveChildrenSerializer(many=True,required=False)
    body = ser.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id','created_at','updated_at','body','idea_id',
                'user_id','reply_to_id','children','author_comment'
                )
        list_serializer_class = FilterCommentListSerializer

    def get_body(self,obj):
        # print("line 35")
        if obj.deleted:
            obj.body = ""           
        return obj.body    

class CommentSerializer(ser.ModelSerializer):
    """ serializer for creating-editing-deleting a comment"""
    author_comment = ser.CharField(source='user.username',read_only=True)
    class Meta:
        model = Comment
        fields = ('id','created_at','body','idea_id',
                'user_id','reply_to_id','parent','author_comment'
        )
        

