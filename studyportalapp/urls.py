from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.userlogin, name = 'login'),
    path('logout/', views.userlogout, name = 'ulogout'),
    path('register/', views.register, name = 'register'),

    path('', views.home, name = 'home'),
    path('books/', views.book, name = 'books'),
    path('youtube/', views.youtube, name = 'youtube'),

    path('notes/', views.notes, name = 'notes'),
    path('updateNote/<str:pk>/',views.updateNote, name = 'update_Note'),
    path('deleteNote/<str:pk>', views.deleteNote, name = 'delete_Note'),
    
    path('homework/', views.homework, name = 'homework'),
    path('updateHomework/<str:pk>/',views.updateHomework, name = 'update_Homework'),
    path('deleteHomework/<str:pk>', views.deleteHomework, name = 'delete_Homework'),
    
    path('todo/', views.todo, name = 'todo'),
    path('updatetodo/<str:pk>/',views.updateTodo, name = 'update_Todo'),
    path('deletetodo/<str:pk>', views.deleteTodo, name = 'delete_Todo'),

    path('dictionary/', views.dictionary, name = 'dictionary'),
    path('wiki/', views.wikipedia_search, name = 'wiki'),
]