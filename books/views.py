from django.shortcuts import render, get_object_or_404
from .models import Book
from .forms import BookForm
from books.models import Book, Favorite
from authors.models import Author
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .similarity import get_similar_books
from .similarity import build_similar_books
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from django.views.decorators.csrf import csrf_exempt
import time


build_similar_books()

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

def books(request, id=None):
    if id:
        if request.method == 'GET':
            return get_book(request, id)
        if request.method == 'DELETE':
            return delete_book(request, id)
        return update_book(request, id)
    if request.method == 'POST':
        return save_book(request)
    
    return get_books(request)

def get_books(request):
    recommendations = []
    search_query = request.GET.get('search', '')
    if search_query:
        books = get_searched_books(search_query)
    else:
        recommendations = get_recommendations(request.user)
        books = Book.objects.exclude(id__in=[book.id for book in recommendations])
    return render(request, 'books.html', {'books': books, 'recommendations': recommendations})

def get_searched_books(search_query):
    books = Book.objects.filter(
        title__icontains=search_query
    ).distinct()

    author_ids = Author.objects.filter(
        first_name__icontains=search_query
    ).values_list('id', flat=True) | Author.objects.filter(
        last_name__icontains=search_query
    ).values_list('id', flat=True)

    books = books | Book.objects.filter(
        author__id__in=author_ids
    ).distinct()
    return books

def get_recommendations(user):
    try:
        favorites = Favorite.objects.filter(user=user).select_related('book').values_list('book', flat=True)
        favorite_books = Book.objects.filter(id__in=favorites)
        recommendations = get_similar_books(favorite_books)
    except:
        recommendations = []
    return recommendations

def get_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.user.is_authenticated and not is_superuser(request.user):
        in_favorites = Favorite.objects.filter(user=request.user, book=book).exists()
        return render(request, 'book.html', {'book': book, 'in_favorites': in_favorites})
    return render(request, 'book.html', {'book': book})

@user_passes_test(is_superuser)
def add_book(request):
    form = BookForm()
    authors = Author.objects.all()
    return render(request, 'new_book.html', {'form': form, 'authors': authors})

@user_passes_test(is_superuser)
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    form = BookForm(instance=book)
    authors = Author.objects.all()
    old_authors = list(book.author.values('id', 'first_name', 'last_name')) 
    return render(request, 'edit_book.html', {
        'form': form,
        'id': id,
        'authors': authors,
        'old_authors': json.dumps(old_authors) 
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def update_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.title = request.POST.get('title')
    book.isbn = request.POST.get('isbn')
    book.publication_date = request.POST.get('publication_date')
    book.pages = request.POST.get('pages')
    book.price = request.POST.get('price')
    if request.FILES.get('image'):
        book.image = request.FILES.get('image')  
    author_ids = request.POST.get('author_ids').split(',')
    if author_ids:
        book.author.set(author_ids) 
    book.save()
    return JsonResponse({'message': 'Book updated successfully!'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return JsonResponse({'message': 'Book deleted successfully!'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def save_book(request):
    title = request.POST.get('title')
    isbn = request.POST.get('isbn')
    author_ids = request.POST.get('author_ids').split(',')  
    publication_date = request.POST.get('publication_date')
    pages = request.POST.get('pages')
    price = request.POST.get('price')
    image = request.FILES.get('image')  

    book = Book.objects.create(
        title=title,
        isbn=isbn,
        publication_date=publication_date,
        pages=pages,
        price=price,
        image=image
    )    
    if author_ids:
        book.author.set(author_ids) 
    return JsonResponse({'message': 'Book save successfully!'})

@login_required
def get_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('book').values_list('book', flat=True)
    favorite_books = Book.objects.filter(id__in=favorites)
    return render(request, 'favorites.html', {'favorite_books': favorite_books})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        favorite = Favorite.objects.get(user=request.user, book_id=book_id)
        favorite.delete()
        return JsonResponse({'message': 'Book removed from favorites successfully!'})
    except Favorite.DoesNotExist:
        Favorite.objects.create(user=request.user, book=book)
        return JsonResponse({'message': 'Book added to favorites successfully!'})