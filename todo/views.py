from django.shortcuts import render, redirect
from django.http import HttpResponse

# Bring in models
from .models import TodoList, Category

# Create your views here.


def index(request):
    todos = TodoList.objects.all()  # queries all todos
    categories = Category.objects.all()  # queries all categories
    priorities = TodoList._meta.get_field('priority').choices
    # print(priorities)
    # choices = TodoList.PRIORITY_LIST
    priority_group = [i[1] for i in priorities]


    # print(priority_group)
    if request.method == "POST":
        if "taskAdd" in request.POST:  # check if there is a request to add a todo
            title = request.POST["description"]
            date = str(request.POST['date'])
            category = request.POST['category_select']
            priority = [i[0] for i in priorities if i[1] == request.POST['priority_select']]
            content = title + " -- " + date + " " + category
            # Create new todo object
            Todo = TodoList(title=title, content=content, due_date=date, priority=priority[0],
                            category=Category.objects.get(name=category))
            Todo.save()  # save to DB
            return redirect('/')  # reload the page

        if "taskDelete" in request.POST:  # Check if there is a request to delete a todo
            # Checked todos to be deleted
            checkedlist = request.POST['checkedbox']
            for todo_id in checkedlist:
                todo = TodoList.objects.get(
                    id=int(todo_id))  # getting the todo id
                todo.delete()

    return render(request, "index.html", {"todos": todos, "categories": categories, "priorities": priorities, "priority_group": priority_group})
