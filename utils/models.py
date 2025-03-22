from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('생성일시', auto_now_add=True)  # 생성한 시간
    modified_at = models.DateTimeField('수정일시', auto_now=True)  # 수정한 시간

    class Meta:
        abstract = True