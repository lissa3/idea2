from datetime import date
from django.contrib import admin
from .models import Category
from mptt.admin import MPTTModelAdmin
from mptt.admin import TreeRelatedFieldListFilter


from .models import Idea, Category, UserIdeaRelation

# mptt_level_indent = 20 on settings.py
# want to make it Draggabel (see bottom)
# class CustomMPTTModelAdmin(MPTTModelAdmin):
#     mptt_level_indent = 30


class YearIdeaFilter(admin.SimpleListFilter):
    # name of the filter to display
    title = "Year created"
    # name for what we a filtering
    parameter_name = "year"

    def lookups(self, request, modeladmin):
        """create a clickable link on the right side"""
        # one goes to the url,another appears in the sidebar
        # url = parameter_name + [0] from the lookups
        return (
            (2019, 2019),
            (2018, 2018)
        )

    def queryset(self, request, queryset):
        if self.value() == '2019':
            return queryset.filter(created_at__gte=date(2019, 1, 1),
                                   created_at__lte=date(2019, 12, 31)
                                   )
        if self.value() == '2018':
            return queryset.filter(created_at__gte=date(2018, 1, 1),
                                   created_at__lte=date(2018, 12, 31)
                                   )

# add action to dropdowm admin (added to default = delete)


def make_published(modeladmin, request, queryset):
    """make possbile to mark idea as published in admin bar checkbox"""
    queryset.update(status=2)


make_published.short_description = 'Mark idea as published'


# group fields in fieldsets
class IdeaAdmin(admin.ModelAdmin):
    search_fields = ('title', 'lead_text', 'main_text', 'categ', 'featured')
    list_filter = ('created_at', 'is_public', 'featured', 'tags',
                   ('categ', TreeRelatedFieldListFilter), YearIdeaFilter)
    list_display = ['id', 'title', 'thumbnail', 'author', 'status', 'is_public', 'created_at', 'featured']
    list_editable = ['status', 'featured']
    list_display_links = ['id', 'title']
    fieldsets = (
        # I don't need it
        ('Main info', {'fields': ('author', 'title', 'categ',
                                  'lead_text', 'main_text', 'status')}),
        # should be present for clearity
        ('Not required Fields',
         {
             'fields': ('featured', 'view_count', 'is_public', 'thumbnail', 'tags'),
             'classes': ('collapse',)
         },
         )
    )
    # just for training
    # radio_fields = {'categ': admin.HORIZONTAL}
    radio_fields = {'categ': admin.VERTICAL}
    # categ = built-in drop-down with indentaion
    actions = [make_published]


class UserIdeaRelationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'idea', 'like', 'rating')


class CategoryAdmin(MPTTModelAdmin):
    mptt_indent_field = "name"
    mptt_level_indent = 20
    list_display = ('name',) 
   


admin.site.register(Category, CategoryAdmin)
admin.site.register(Idea, IdeaAdmin)
admin.site.register(UserIdeaRelation, UserIdeaRelationAdmin)