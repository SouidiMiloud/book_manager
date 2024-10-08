from django.urls import path
from books import views


urlpatterns = [
    path('', views.books, name='books'),
    path('<int:id>', views.books, name='books'),
    path('add_book', views.add_book, name='add_book'),
    path('edit_book/<int:id>', views.edit_book, name='edit_book'),
    path('favorites', views.get_favorites, name="favorites"),
    path('update_favorite/<int:book_id>', views.update_favorite, name='update_favorite'),

    # for testing
    path('get_recommendations', views.get_recommendations)
]