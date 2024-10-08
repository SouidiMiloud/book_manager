from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from books import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.books, name='books'),
    path('books/', include('books.urls'), name='books'),
    path('authors/', include('authors.urls'), name='authors'),
    path('users/', include('users.urls'), name='users'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)