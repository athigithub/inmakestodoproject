from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Task
from . forms import TodoForms
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView


#class based generic views
class Tasklistview(ListView):
    model=Task
    template_name = 'home.html'
    context_object_name = 'task1'

class Taskdetailview(DetailView):
    model=Task
    template_name = 'detail.html'
    context_object_name = 'task' #variable we create this is used in detail.html

class Taskupdateview(UpdateView):
    model=Task
    template_name = 'update.html'
    context_object_name = 'task' #variable we create
    fields=('name','priority','date')
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class Taskdeleteview(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')

# Create your views here.#function based
def add(request):
    task1=Task.objects.all()
    if request.method=='POST':
        name=request.POST.get('task','')
        priority=request.POST.get('priority','')
        date=request.POST.get('date','')
        task=Task(name=name,priority=priority,date=date)
        task.save()
    return render(request,'home.html',{'task1':task1})

def delete(request,taskid):
    obj=Task.objects.get(id=taskid)
    if request.method=='POST':
        obj.delete()
        return redirect('/')
    return render(request,'delete.html')

def update(request,taskid):
    task=Task.objects.get(id=taskid)
    formobj=TodoForms(request.POST or None, instance=task)
    if formobj.is_valid():
        formobj.save()
        return  redirect('/')
    return render(request,'edit.html',{'form':formobj ,'task':task})
