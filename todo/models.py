from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from utils.models import TimeStampedModel

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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('todo:info', kwargs={'pk':self.pk})

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