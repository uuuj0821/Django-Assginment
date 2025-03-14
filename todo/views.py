from django.shortcuts import render, get_object_or_404
from todo.models import ToDo

# Create your views here.
def todo_list(request):
    todo_lists  = ToDo.objects.all()
    context = {
        'todo_lists' : todo_lists,
    }

    return render(request, 'todo_list.html', context)

def todo_info(request, todo_id):
    todo = get_object_or_404(ToDo, id=todo_id)
    info = {
        'title' : todo.title,
        '설명' : todo.description,
        '시작일' : todo.start_date,
        '마감일' : todo.end_date,
        '완료 여부' : todo.is_completed
    }

    return render(request, 'todo_info.html', {'info':info})
