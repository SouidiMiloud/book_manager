from django.shortcuts import render, redirect, get_object_or_404
from .models import Author
from .forms import AuthorForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

def is_superuser(user):
    return user.is_authenticated and user.is_superuser

def authors(request, id=None):
    if id:
        if request.method == 'GET':
            return get_author(request, id)
        if request.method == 'DELETE':
            return delete_author(request, id)
        return update_author(request, id)
    if request.method == 'POST':
        return save_author(request)
    authors = Author.objects.all()
    return render(request, 'authors.html', {'authors': authors})

def get_author(request, id):
    author = get_object_or_404(Author, id=id)
    return render(request, 'author.html', {'author': author})

@user_passes_test(is_superuser)
def add_author(request):    
    form = AuthorForm()
    return render(request, 'new_author.html', {'form': form})

@user_passes_test(is_superuser)
def edit_author(request, id):
    author = get_object_or_404(Author, id=id)
    form = AuthorForm(instance=author)
    return render(request, 'edit_author.html', {'form': form, 'id': id})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def update_author(request, id):
    author = get_object_or_404(Author, id=id)
    form = AuthorForm(request.POST, request.FILES, instance=author)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'Author updated successfully!'})
    return JsonResponse({'errors': form.errors}, status=400)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def delete_author(request, id):
    author = get_object_or_404(Author, id=id)
    author.delete()
    return JsonResponse({'message': 'Author deleted successfully!'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@user_passes_test(is_superuser)
def save_author(request):
    form = AuthorForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'Author saved successfully!'})
    return JsonResponse({'errors': form.errors}, status=400)