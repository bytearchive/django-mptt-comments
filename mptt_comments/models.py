import datetime
import mptt

from django.db import models
from django.conf import settings
from django.contrib.comments.models import Comment
from django.contrib.comments.managers import CommentManager

class MpttCommentManager(CommentManager):
    
    def get_root_comment(self, ctype, object_pk):
        lookup = {
            'parent':None,
            'content_type':ctype,
            'object_pk':str(object_pk),
            'defaults':{
                'comment': 'Root comment placeholder',
                'user_name': 'Noname',
                'user_email': 'no@user.no',
                'user_url': '',
                'submit_date': datetime.datetime.now(),
                'site_id': settings.SITE_ID
            }
        }
        try:
            return self.model.objects.filter(**lookup)[0]
        except IndexError:
            return self.model.objects.create(**lookup)

class MpttComment(Comment):
    title = models.CharField(max_length=60)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True)
    
    class Meta:
        ordering = ('tree_id', 'lft')
    
    objects = MpttCommentManager()

mptt.register(MpttComment)
