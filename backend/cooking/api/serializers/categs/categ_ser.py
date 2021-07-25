from rest_framework import serializers as ser
from ideas.models import Category

# N1
# categories with children: for rendering in left side menu and indentation

class FilterCategListSerializer(ser.ListSerializer):
    """filter categs: front should get a list with only root categs"""
    def to_representation(self,objects):
        data = objects.filter(parent=None)
        return super().to_representation(data)



class CustomChildrenSerializer(ser.Serializer):
    """child should be serialized by CategorySer-er"""
    def to_representation(self, obj):
        # self.parent.__class__.__name__)          # ListSerializer
        # self.parent.parent.__class__.__name__)# CategorySerializer
        serializer = self.parent.parent.__class__(obj)
        #print("ser data: ",serializer.data)
        # {'id': 2, 'name': 'Fiction', 'slug': 'fiction', 'parent': 1, 'children': []}
        return serializer.data


class CategorySerializer(ser.ModelSerializer):
    """ list of categs with tree structure"""
    # each related object if parent has attr children == 'related name' from model FK
    #    and will be ser-ed by CategorySerializer; you need children (no need parents) """
    children = CustomChildrenSerializer(many=True)
    class Meta:
        model = Category
        fields = ('id','name','slug','children')
        # over-write list_ser_cls (to filter data: only parents)
        list_serializer_class = FilterCategListSerializer

# 2
# list of all categories for drop-down: user to choose when idea gets created
class CategoryNameSerializer(ser.ModelSerializer):
    """  list of categs without tree-structure"""
    class Meta:
        model = Category
        fields = ('name', 'id')        