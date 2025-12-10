from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

from .models import Todo
from .forms import TodoForm, RegisterForm


def welcome(request):
    """Trang chào mừng với 2 nút Đăng ký / Đăng nhập"""
    return render(request, 'core/welcome.html')


def register(request):
    """View đăng ký tài khoản"""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            login(request, user)
            return redirect('todo')  # Redirect tới /todo/ thay vì admin
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required(login_url='login')
def index(request):
    """Trang todo - CRUD cơ bản, dữ liệu lưu trong db.sqlite3."""

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            title = request.POST.get('title', '').strip()
            if title:
                Todo.objects.create(user=request.user, title=title)

        elif action == 'toggle':
            todo_id = request.POST.get('todo_id')
            try:
                todo = Todo.objects.get(id=todo_id, user=request.user)
                todo.is_done = not todo.is_done
                todo.save()
            except Todo.DoesNotExist:
                pass

        elif action == 'edit':
            todo_id = request.POST.get('todo_id')
            title = request.POST.get('title', '').strip()
            if title:
                try:
                    todo = Todo.objects.get(id=todo_id, user=request.user)
                    todo.title = title
                    todo.save()
                except Todo.DoesNotExist:
                    pass

        elif action == 'delete':
            todo_id = request.POST.get('todo_id')
            Todo.objects.filter(id=todo_id, user=request.user).delete()

        # Luôn redirect để tránh gửi lại form khi refresh
        return redirect('todo')

    # Sắp xếp
    sort_by = request.GET.get('sort', 'newest')
    todos = Todo.objects.filter(user=request.user)
    
    if sort_by == 'a-z':
        todos = todos.order_by('title')
    elif sort_by == 'z-a':
        todos = todos.order_by('-title')
    elif sort_by == 'oldest':
        todos = todos.order_by('created_at')
    else:  # newest (default)
        todos = todos.order_by('-created_at')
    
    form = TodoForm()
    return render(request, 'core/index.html', {
        'todos': todos,
        'sort_by': sort_by,
        'form': form
    })