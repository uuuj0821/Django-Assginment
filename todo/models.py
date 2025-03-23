from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from utils.models import TimeStampedModel
from django.conf import settings

from io import BytesIO
from PIL import Image
from pathlib import Path

User = get_user_model()

# Create your models here.
class ToDo(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE) # 참조와 다 같이 삭제 옵션
    title = models.CharField('할 일', max_length=50) # todo 제목
    description = models.TextField('설명') # todo 설명
    start_date = models.DateField('시작일') # todo 시작일
    end_date = models.DateField('마감일') # todo 마감일
    is_completed = models.BooleanField('완료여부', default=False) # 완료여부
    # created_at = models.DateTimeField('생성일시', auto_now_add=True) # 생성한 시간
    # modified_at = models.DateTimeField('수정일시', auto_now=True) # 수정한 시간

    image = models.ImageField('이미지', null=True, blank=True, upload_to='todo/%Y/%m/%d')
    thumbnail = models.ImageField('썸네일', null=True, blank=True, upload_to='todo/%Y/%m/%d/thumbnail', default='default/no_image.png')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('todo:info', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        image = Image.open(self.image)
        image.thumbnail((300, 300))
        image_path = Path(self.image.path)
        thumbnail_name = image_path.stem # 이미지 파일명만 가져옴 (경로, 확장자 제외)
        thumbnail_extension = image_path.suffix.lower() # 이미지 확장자만 가져옴(.png, .jpg,...) (경로, 이미지파일명 제외)
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}'

        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)
        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()

        return super().save(*args, **kwargs)

    def get_thumbnail_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        elif self.image:
            return self.image.url
        else:
            return settings.MEDIA_URL + '/default/no_image.png'

    class Meta:
        verbose_name = '할 일'
        verbose_name_plural = '할 일 목록'
        # ordering = ["end_date"]

class Comment(TimeStampedModel):
    todo = models.ForeignKey(ToDo, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    message = models.TextField(max_length=200)

    def __str__(self):
        return f'{self.todo.title} 댓글'

    class Meta:
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'
        ordering = ('-created_at', '-id')