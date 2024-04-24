from django.shortcuts import render, redirect
from .models import Note, Homework, Task
# pip install youtube-search-python -> for youtube section
from youtubesearchpython import VideosSearch
# pip install requests -> for book and dictionary aps
import requests
# pip install wikipedia -> for wikipedia section
import wikipediaapi
# Import authentication libraries
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Create flash messages about username
        checkuser = authenticate(username = username, password = password)
        if checkuser is not None:
            login(request, checkuser)
            return redirect('home')
        else:
            messages.error(request,"the user doesn't exist")
            return redirect('/login')        
    return render(request, 'studyportalapp\login.html')
def userlogout(request):
    logout(request)
    return redirect('/login')
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Create flash messages about username
        checkUsername = User.objects.filter(username = username)
        if checkUsername:
            messages.error(request,'the username already exists')
            return redirect('/register')
        # Create flash messages about password
        if len(password) < 4:
            messages.error(request,'the password must be at least four characters')
            return redirect('/register')
        # Create user account
        user = User.objects.create_user(username=username, email = email, password=password)
        user.save()
        return redirect('/login')
    return render(request, 'studyportalapp\\register.html')

@login_required
def home(request):
    return render(request,'studyportalapp\home.html',{'username':request.user})

@login_required
def notes(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        note = Note(user = request.user, 
                    title = title, 
                    description = description)
        note.save()
        return redirect('notes')
    
    all_notes = Note.objects.filter(user = request.user)
    context = {'notes':all_notes}
    return render(request, 'studyportalapp\\notes.html', context)
@login_required
def updateNote(request, pk):
    note = Note.objects.get(id = pk)
    if request.method == 'POST':
        note.title = request.POST.get('new_title')
        note.description = request.POST.get('description')
        note.save()
        return redirect('notes')  # Redirect to the task list page
    return render(request, 'studyportalapp/updateNote.html', {'note': note})
@login_required
def deleteNote(request, pk):
    note = Note.objects.get(id = pk)
    if request.method == 'POST':
        note.delete()
        return redirect('notes')  # Redirect to the task list page after deleting
    return render(request, 'studyportalapp\deleteNote.html', {'note': note})

@login_required
def homework(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        completed = (request.POST.get('completed') == 'on')
        homework = Homework(user = request.user, 
                            subject=subject, title=title, 
                            description = description, date = date, finished = completed)
        homework.save()
        return redirect('homework')
    all_homework = Homework.objects.filter(user = request.user)
    context = {'homework': all_homework}
    return render(request, 'studyportalapp\homework.html', context)
@login_required
def updateHomework(request, pk):
    homework = Homework.objects.get(id = pk)
    if request.method == 'POST':
        homework.title = request.POST.get('new_title')
        homework.subject = request.POST.get('new_subject')
        homework.description = request.POST.get('description')
        homework.finished = (request.POST.get('complete') == 'on')
        homework.save()
        return redirect('homework')  # Redirect to the task list page
    return render(request, 'studyportalapp/updateHomework.html', {'homework': homework})
@login_required
def deleteHomework(request, pk):
    howework = Homework.objects.get(id = pk)
    if request.method == 'POST':
        howework.delete()
        return redirect('homework')  # Redirect to the task list page after deleting
    return render(request, 'studyportalapp\deleteHomework.html', {'homework': howework})

@login_required
def todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        completed = (request.POST.get('completed') == 'on')
        task = Task(user = request.user, 
                    title=title, 
                    finished = completed)
        task.save()
        return redirect('todo')
    all_tasks = Task.objects.filter(user = request.user)
    context = {'tasks':all_tasks}
    return render(request, 'studyportalapp\\todo.html',context)
@login_required
def updateTodo(request, pk):
    task = Task.objects.get(id = pk)
    if request.method == 'POST':
        task.title = request.POST.get('new_title')
        task.finished = (request.POST.get('complete') == 'on')
        task.save()
        return redirect('todo')  # Redirect to the task list page
    return render(request, 'studyportalapp/updateTodo.html', {'task': task})
@login_required
def deleteTodo(request, pk):
    task = Task.objects.get(id = pk)
    if request.method == 'POST':
        task.delete()
        return redirect('todo')  # Redirect to the task list page after deleting
    return render(request, 'studyportalapp\deleteTodo.html', {'task': task})

@login_required
def youtube(request):
    if request.method == 'POST':
        SearchTitle = request.POST.get('search')
        # API Call to Youtube with the search term and display results on page 
        videos = VideosSearch(SearchTitle, limit = 10)
        list_videos = []
        for video in videos.result()['result']:
            result_dict = {
                'input':SearchTitle,
                'title':video['title'],
                'duration':video['duration'],
                'thumbnail':video['thumbnails'][0]['url'],
                'channel_name':video['channel']['name'],
                'link':video['link'],
                'views':video['viewCount']['short'],
                'time':video['publishedTime'],
            }
            desc = ''
            if video['descriptionSnippet'] is not None:
                for line in video['descriptionSnippet']:
                    if isinstance(line, str):
                        desc += line
                    else:
                        desc += str(line)
                desc = desc[8:]
            result_dict['description'] = desc
            list_videos.append(result_dict)

        return render(request, 'studyportalapp/youtube.html', {'videos': list_videos})
    return render(request, 'studyportalapp\youtube.html',{'videos':None})
@login_required
def book(request):
    if request.method == 'POST':
        SearchTitle = request.POST.get('search')
        # API Call to Youtube with the search term and display results on page 
        url = "https://www.googleapis.com/books/v1/volumes?q="+SearchTitle
        r = requests.get(url)
        answer = r.json()
        list_books = []
        for book in range(10):
            result_dict = {
                'input':SearchTitle,
                'title':answer['items'][book]['volumeInfo']['title'],
                'subtitle':answer['items'][book]['volumeInfo'].get('subtitle'),
                'description':answer['items'][book]['volumeInfo'].get('description'),
                'count':answer['items'][book]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][book]['volumeInfo'].get('categories'),
                'rating':answer['items'][book]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][book]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][book]['volumeInfo'].get('previewLink')
            }
            list_books.append(result_dict)
        return render(request, 'studyportalapp/books.html', {'books': list_books})
    return render(request, 'studyportalapp/books.html',{'books':None})
@login_required
def dictionary(request):
    if request.method == 'POST':
        SearchTitle = request.POST.get('search')
        # API Call to dictionary API with the search term and display results on page 
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + SearchTitle
        try:
            response = requests.get(url)
            data = response.json()
            context = {'input': SearchTitle}
            if isinstance(data, list) and data:
                word_data = data[0]
                context.update({
                    'phonetics': word_data.get('phonetics', []),
                    'audio': word_data.get('phonetics', [{}])[0].get('audio', ''),
                    'definition': word_data.get('meanings', [{}])[0].get('definitions', [{}])[0].get('definition', ''),
                    'example': word_data.get('meanings', [{}])[0].get('definitions', [{}])[0].get('example', ''),
                    'synonyms': word_data.get('meanings', [{}])[0].get('definitions', [{}])[0].get('synonyms', []),
                })
        except:
            context = {
                'input':None
            }
        return render(request, 'studyportalapp/dictionary.html', context)
    return render(request, 'studyportalapp/dictionary.html', {'input': None})
@login_required
def wikipedia_search(request):
    if request.method == 'POST':
        SearchTitle = request.POST.get('search')
        # Specify a custom user agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        # Create a Wikipedia API object with the custom user agent
        wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent)
        # Search for the query
        page = wiki_wiki.page(SearchTitle)
        # Set default value for the context
        context = {
            'input':SearchTitle,
            'title':"No results",
            'link':None,
            'details':None
        }
        # Check if the page exists
        if page.exists():
            context = {
                'input':SearchTitle,
                'title':page.title,
                'link':page.fullurl,
                'details':page.summary
            }
        return render(request, 'studyportalapp\wiki.html', context)
    return render(request, 'studyportalapp\wiki.html')

