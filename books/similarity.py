from difflib import SequenceMatcher
from .models import Book


similar_books = {}

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def similar_book_titles(book1, book2):
    return similar(book1.title, book2.title)

def similar_book_authors(book1, book2):
    book1_authors = book1.author.all()
    book2_authors = book2.author.all()
    authors_similarity = 0
    for author1 in book1_authors:
        for author2 in book2_authors:
            sim = similar(author1.first_name + " " + author1.last_name, author2.first_name + " " + author2.last_name)
            authors_similarity = max(authors_similarity, sim)
    return authors_similarity

def similar_book_prices(book1, book2, max_price_diff=50):
    price_diff = abs(book1.price - book2.price)
    return max(0, 1 - (price_diff / max_price_diff))

def get_similarity(book1, book2, title_weight=0.4, author_weight=0.4, price_weight=0.2):
    title_sim = similar_book_titles(book1, book2)
    author_sim = similar_book_authors(book1, book2)
    price_sim = similar_book_prices(book1, book2)
    
    total_sim = float(title_sim) * title_weight + float(author_sim) * author_weight + float(price_sim) * price_weight
    return total_sim

def build_similar_books():
    books = Book.objects.all()
    for book in books:
        similar_books[book.id] = []
    for book1 in books:
        for book2 in books:
            if book1.id == book2.id:
                continue
            similarity = get_similarity(book1, book2)
            if similarity >= 0.3:
                similar_books[book1.id].append((book2.id, similarity))
    for key in similar_books:
        similar_books[key] = sorted(similar_books[key], key=lambda x: x[1], reverse=True)


def get_similar_books(favorites):    
    books_with_similarities = []
    favorite_ids = [fav.id for fav in favorites]
    for favorite in favorites:
        books_num = 0
        it = 0
        while it < len(similar_books[favorite.id]) and books_num < 5:
            if similar_books[favorite.id][it][0] not in favorite_ids:
                books_with_similarities.append(similar_books[favorite.id][it])
                books_num += 1
            it += 1

    books_with_similarities = sorted(books_with_similarities, key=lambda x: x[1], reverse=True)
    result = [Book.objects.get(id=sim[0]) for sim in books_with_similarities]
    return result[:5]