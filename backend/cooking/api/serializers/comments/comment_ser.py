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
        if obj.deleted:
            return None
        return obj.body    

class CommentSerializer(ser.ModelSerializer):
    """ serializer for creating-editing-deleting a comment"""
    class Meta:
        model = Comment
        fields = ('id','created_at','body','idea_id',
                'user_id','reply_to_id','parent'
        )
        # over-write list_ser_cls (to filter data: only parents)
        list_serializer_class = FilterCommentListSerializer

"""
line 15 {'id': 4, 'parent': 2, 'created_at': '2021-08-07T16:00:54.589564Z', 'updated_at': '2021-08-07T16:04:03.989936Z', 'body': 'Have fun!', 'idea_id': 7, 'user_id': 7, 'reply_to_id': 2, 'children': [], 'author_comment': 'hemul'}
line 15 {'id': 2, 'parent': 1, 'created_at': '2021-08-07T12:33:32.019700Z', 'updated_at': '2021-08-07T16:00:12.233043Z', 'body': 'Do you enjoy yourself?', 'idea_id': 7, 'user_id': 2, 'reply_to_id': 6, 'children': [{'id': 4, 'parent': 2, 'created_at': '2021-08-07T16:00:54.589564Z', 'updated_at': '2021-08-07T16:04:03.989936Z', 'body': 'Have fun!', 'idea_id': 7, 'user_id': 7, 'reply_to_id': 2, 'children': [], 'author_comment': 'hemul'}], 'author_comment': 'mio'}
line 15 {'id': 4, 'parent': 2, 'created_at': '2021-08-07T16:00:54.589564Z', 'updated_at': '2021-08-07T16:04:03.989936Z', 'body': 'Have fun!', 'idea_id': 7, 'user_id': 7, 'reply_to_id': 2, 'children': [], 'author_comment': 'hemul'}

"""        