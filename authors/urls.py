from django.urls import path
from authors import views


urlpatterns = [
    path('', views.authors, name='authors'),
    path('<int:id>', views.authors, name='authors'),
    path('add_author', views.add_author, name='add_author'),
    path('edit_author/<int:id>', views.edit_author, name='edit_author'),
]