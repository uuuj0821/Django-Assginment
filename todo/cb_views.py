from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todo.forms import CommentPostForm
from todo.models import ToDo, Comment


class ToDoListView(LoginRequiredMixin, ListView):
    queryset = ToDo.objects.all()
    template_name = 'todo/todo_list.html'
    paginate_by = 10
    ordering = ('-created_at', )

    def get_queryset(self):
        queryset = super().get_queryset().annotate(comment_count=Count('comments')) # 관계네임
        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        return queryset

class ToDoDetailView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'todo/todo_info.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(ToDo, pk=kwargs.get('pk'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(todo=self.object).prefetch_related('author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # detailview에서 dict 사용
        context['comment_form'] = CommentPostForm()
        context['todo'] = self.object
        context['todo_dict'] = {
            '설명': self.object.description,
            '시작일': self.object.start_date,
            '마감일': self.object.end_date,
            '완료 여부': self.object.is_completed
        }

        # context.update({'pk': self.object.pk, ...}) 템플릿에서 일회용으로 사용
        # context.save() : 만약 db에도 저장하고 싶으면 .save() 해줘야함!!

        return context

class ToDoCreateView(LoginRequiredMixin, CreateView):
    model = ToDo
    template_name = 'todo/todo_form.html'
    fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'pk':self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '작성'
        context['btn_name'] = '생성'
        return context


class ToDoUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDo
    template_name = 'todo/todo_form.html'
    fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '수정'
        context['btn_name'] = '수정'
        return context

    # models.py의 get_absolute_url() 선언
    # def get_success_url(self):
    #     return reverse_lazy('todo:info', kwargs={'pk':self.object.pk})

class ToDoDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDo

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        return reverse_lazy('todo:list')

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentPostForm

    def get(self, *args, **kwargs):
        raise Http404

    def form_valid(self, form):
        todo = self.get_todo()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.todo = todo
        self.object.save()
        return HttpResponseRedirect(reverse_lazy('todo:info', kwargs={'pk': todo.pk}))

    def get_todo(self):
        pk = self.kwargs.get('pk')
        todo = get_object_or_404(ToDo, pk=pk)
        return todo

class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentPostForm

    def get(self, *args, **kwargs):
        raise Http404

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        print('todo_id : ',self.object.todo_id)
        return reverse_lazy('todo:info', kwargs={'pk': self.object.todo_id})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self):
        print('todo_id : ',self.object.todo_id)
        return reverse_lazy('todo:info', kwargs={'pk': self.object.todo_id})
