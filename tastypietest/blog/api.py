# myapp/api.py
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from blog.models import Entry, Comment


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'is_active', 'is_staff']
        allowed_methods = ['get']
        filtering = {
            'username': ALL,
        }


class EntryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user', full=True)
    
    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        authorization = Authorization()
        filtering = {
            'body': ALL,
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }


class CommentResource(ModelResource):
    entry = fields.ForeignKey(EntryResource, 'entry', full=True)
    user = fields.ForeignKey(UserResource, 'user', full=True)

    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }
