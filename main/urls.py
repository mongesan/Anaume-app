from django.urls import path
from main import views
from django.contrib.auth import views as auth_views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('mynote', views.MyNoteListView.as_view(), name='mynote'),
    path('note/<int:note_id>', views.note, name='note'),
    path('note/fav/<int:note_id>', views.fav_note, name="fav_note"),
    path('note/delete/<int:note_id>', views.delete_note, name="delete_note"),
    path('text/delete/<int:text_id>', views.delete_text, name="delete_text"),
    path('pdf/<int:note_id>', views.PDFView, name='PDFView'),
    # path('note/ajax_note_add', views.ajax_note_add, name='ajax_note_add')
]
