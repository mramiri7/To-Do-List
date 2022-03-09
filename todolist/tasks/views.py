from django.http.response import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages

from .models import Task
from .forms import RegisterForm



@csrf_exempt
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request, 'register.html', context)


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tasks')
    return render(request, 'login.html', {})

@csrf_exempt
@login_required(login_url='login/')
def logout_view(request):
    messages.info(request, "You have successfully logged out.")
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'index.html', {})

class TaskView(LoginRequiredMixin, ListView):
    model = Task
    fields = ('user', 'title', 'description', 'completed')
    template_name = 'tasks.html'
    login_url = '/login/'

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user=user)


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'taskdetail.html'


class CreateTask(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'completed',]
    success_url = reverse_lazy('tasks')
    template_name = 'createtask.html'


    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'deletetask.html'


class EditTask(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasks')
    template_name = 'edittask.html'
