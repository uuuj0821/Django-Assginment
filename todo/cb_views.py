from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todo.models import ToDo


class ToDoListView(LoginRequiredMixin, ListView):
    queryset = ToDo.objects.all()
    template_name = 'todo/todo_list.html'
    paginate_by = 10
    ordering = ('-created_at', )

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        return queryset

class ToDoDetailView(LoginRequiredMixin, DetailView):
    model = ToDo
    template_name = 'todo/todo_info.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # detailview에서 dict 사용
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
    template_name = 'todo/todo_create.html'
    fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('todo:info', kwargs={'pk':self.object.pk})


class ToDoUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDo
    template_name = 'todo/todo_update.html'
    fields = ('title', 'description', 'start_date', 'end_date', 'is_completed')

    def get_queryset(self):
        queryset = super().get_queryset()

        if not self.request.user.is_superuser:
            return queryset.filter(author=self.request.user)
        return queryset

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