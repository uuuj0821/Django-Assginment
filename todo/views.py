from IPython.core.release import author
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from todo.forms import ToDoPostForm
from todo.models import ToDo
from django.db.models import Q
from django.views.decorators.http import require_http_methods

@login_required()
def todo_list(request):
    todo_lists  = ToDo.objects.all()

    q = request.GET.get('q')
    if q:
        # 제목, 본문에서 검색
        todo_lists = todo_lists.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    # 페이지네이션
    paginator = Paginator(todo_lists, 10)  # 한페이지당 몇개씩
    page = request.GET.get('page')  # 현재페이지 값
    page_object = paginator.get_page(page)
    # 페이지네이션_end

    context = {
        'page_object':page_object,
    }

    return render(request, 'todo/todo_list.html', context)

@login_required()
def todo_info(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)
    info = {
        'pk' : todo.pk,
        'author' : todo.author,
        'title' : todo.title,
        '설명' : todo.description,
        '시작일' : todo.start_date,
        '마감일' : todo.end_date,
        '완료 여부' : todo.is_completed
    }

    return render(request, 'todo/todo_info.html', {'info':info})

# 할일 생성하기
@login_required()
def todo_create(request):
    form = ToDoPostForm(request.POST or None)

    if form.is_valid():
        todo = form.save(commit=False)
        todo.author = request.user
        todo.save()

        return redirect(reverse('todo_info', kwargs={'todo_id':todo.pk}))

    context = {'form':form}

    return render(request, 'todo/todo_create.html', context)


# 할일 수정하기
@login_required()
def todo_update(request, todo_id):
    print('todo_id :', todo_id)
    todo = get_object_or_404(ToDo, id=todo_id, author=request.user)
    form = ToDoPostForm(request.POST or None, instance=todo)

    if form.is_valid():
        todo = form.save()
        print('todo : ', todo)
        return redirect(reverse('todo_info', kwargs={'todo_id':todo.pk}))

    context = {
            'form':form
        }

    return render(request, 'todo/todo_update.html', context)

# 할일 삭제하기
@login_required()
@require_http_methods(['POST'])
def todo_delete(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id, author=request.user)
    todo.delete()
    return redirect(reverse('todo_list'))