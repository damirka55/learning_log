from django.shortcuts import render

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    """Домашняя страница приложения Learning Log."""
    return render(request, 'learning_logs/index.html')
    
@login_required
def topics(request):
    """Выводит список тем."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Выводит одну тему и все ее записи."""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Определяет новую тему."""
    if request.method != 'POST':
        #Данные не отправились; создается пустая форма.
        form = TopicForm()
    else:
        #Отправлены данные POST; обработать данные.
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
            
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
    
@login_required
def new_entry(request, topic_id):
    """Добавляет новую запись по конкретной теме."""
    topic = Topic.objects.get(id=topic_id)
    
    if request.method != 'POST':
        #Данные не отправились; создается пустая форма.
        form = EntryForm()
    else:
        #Отправлены данные POST; обработать данные.
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                args=[topic_id]))
            
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Редактирует существующую запись."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    
    if request.method != 'POST':
        #Исходный запрос; форма заполняется данными текущей записи.
        form = EntryForm(instance=entry)
    else:
        #Отправка данных POST; обработать данные.
        form = EntryForm(instance=entry, data=request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',
                args=[topic.id]))
                
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
