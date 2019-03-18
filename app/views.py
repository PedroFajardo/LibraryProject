from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from app.forms import *

from app.models import Author, Book, Publisher


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    tparams = {
        'title': 'Home Page',
        'year': datetime.now().year,
    }
    return render(request, 'index.html', tparams)


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    tparams = {
        'title': 'Contact',
        'message': 'Your contact page.',
        'year': datetime.now().year,
    }
    return render(request, 'contact.html', tparams)


def about(request):
    assert isinstance(request, HttpRequest)
    tparams = {
        'title': 'About',
        'message': 'Your application description page.',
        'year': datetime.now().year,
    }
    return render(request, 'about.html', tparams)


def booksearch(request):
    if 'query' in request.POST:
        query = request.POST['query']
        if query:
            books = Book.objects.filter(title__icontains=query)
            return render(request, 'booklist.html', {'boks': books, 'query': query})
        else:
            return render(request, 'booksearch.html', {'error': True})
    else:
        return render(request, 'booksearch.html', {'error': False})


def bookInsert(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect('/login')
    authors = Author.objects.all()
    publishers = Publisher.objects.all()
    if 'title' in request.POST:
        query = request.POST
        if query:
            b = Book.objects.filter(title__icontains=query['title'])
            if not b:
                pub = Publisher.objects.filter(name__icontains=query['pub'])
                book = Book(title=query['title'], date=query['date'], publisher=pub[0])
                book.save()
                book_auth = []
                for aut in query.getlist('auts'):
                    a = Author.objects.filter(name__icontains=aut)
                    book_auth.append(a[0])
                book.authors.set(book_auth)
                book.save()
                return render(request, 'bookInserted.html', {'book': book, 'query': query['title']})
            else:
                return render(request, 'bookInsert.html',
                              {'error': False, 'exists': True, 'authors': authors, 'publishers': publishers})
        else:
            return render(request, 'bookInsert.html',
                          {'error': True, 'exists': False, 'authors': authors, 'publishers': publishers})
    else:
        return render(request, 'bookInsert.html',
                      {'error': False, 'exists': False, 'authors': authors, 'publishers': publishers})


def authorInsert(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect('/login')
    if 'email' in request.POST:
        query = request.POST
        if query:
            aut = Author.objects.filter(email__icontains=query['email'])
            if not aut:
                author = Author(name=query['name'], email=query['email'])
                author.save()
                return render(request, 'authorInserted.html', {'aut': author, 'query': query['name']})
            else:
                return render(request, 'authorInsert.html', {'error': False, 'exists': True})
        else:
            return render(request, 'authorInsert.html', {'error': True, 'exists': False})
    else:
        return render(request, 'authorInsert.html', {'error': False, 'exists': False})


def authorSearch(request):
    if 'query' in request.POST:
        query = request.POST['query']
        if query:
            authors = Author.objects.filter(name__icontains=query)
            return render(request, 'authorList.html', {'auts': authors, 'query': query})
        else:
            return render(request, 'authorSearch.html', {'error': True})
    else:
        return render(request, 'authorSearch.html', {'error': False})


def publisherInsert(request):
    if not request.user.is_authenticated or request.user.username != 'admin':
        return redirect('/login')
    if 'name' in request.POST:
        query = request.POST
        if query:
            pub = Publisher.objects.filter(name__icontains=query['name'])
            if not pub:
                publisher = Publisher(name=query['name'], city=query['city'], country=query['country'],
                                      website=query['website'])
                publisher.save()
                return render(request, 'publisherInserted.html', {'pub': publisher, 'query': query['name']})
            else:
                return render(request, 'publisherInsert.html', {'error': False, 'exists': True})
        else:
            return render(request, 'publisherInsert.html', {'error': True, 'exists': False})
    else:
        return render(request, 'publisherInsert.html', {'error': False, 'exists': False})


def publisherSearch(request):
    if 'query' in request.POST:
        query = request.POST['query']
        if query:
            publishers = Publisher.objects.filter(name__icontains=query)
            return render(request, 'publisherList.html', {'pubs': publishers, 'query': query})
        else:
            return render(request, 'publisherSearch.html', {'error': True})
    else:
        return render(request, 'publisherSearch.html', {'error': False})


def bookquery(request):
    # if POST request, process form data
    if request.method == 'POST':
        # create form instance and pass data to ir
        form = BookQueryForm(request.POST)
        if form.is_valid():  # is it valid?
            query = form.cleaned_data['query']
            books = Book.objects.filter(title__icontains=query)
            return render(request, 'booklist.html', {'boks': books, 'query': query})
    # if GET (or any other method), create blank form
    else:
        form = BookQueryForm()
    return render(request, 'bookquery.html', {'form': form})


def bookInsertQuery(request):
    #if not request.user.is_authenticated or request.user.username != 'admin':
    #    return redirect('/login')
    # if POST request, process form data
    if request.method == 'POST':
        # create form instance and pass data to ir
        form = BookInsertForm(request.POST)
        if form.is_valid():  # is it valid?
            title = form.cleaned_data['title']
            date = form.cleaned_data['date']
            auts = form.cleaned_data['authors']
            pub = form.cleaned_data['publisher']
            b = Book.objects.filter(title__icontains=title)
            if not b:
                pub = Publisher.objects.filter(name__icontains=pub)
                book = Book(title=title, date=date, publisher=pub[0])
                book.save()
                book_auth = []
                for aut in auts:
                    a = Author.objects.filter(name__icontains=aut)
                    book_auth.append(a[0])
                book.authors.set(book_auth)
                book.save()
                return render(request, 'bookInserted.html', {'book': book, 'query': title})
            else:
                return render(request, 'bookInsertv2.html',
                              {'error': False, 'exists': True})
    # if GET (or any other method), create blank form
    else:
        form = BookInsertForm()
    return render(request, 'bookInsertv2.html', {'form': form})


def authorquery(request):
    # if POST request, process form data
    if request.method == 'POST':
        # create form instance and pass data to ir
        form = AuthorQueryForm(request.POST)
        if form.is_valid():  # is it valid?
            query = form.cleaned_data['query']
            authors = Author.objects.filter(name__icontains=query)
            return render(request, 'authorList.html', {'auts': authors, 'query': query})
    # if GET (or any other method), create blank form
    else:
        form = AuthorQueryForm()
    return render(request, 'authorquery.html', {'form': form})


def authorInsertQuery(request):
    #if not request.user.is_authenticated or request.user.username != 'admin':
    #    return redirect('/login')
    # if POST request, process form data
    if request.method == 'POST':
        # create form instance and pass data to ir
        form = AuthorInsertForm(request.POST)
        if form.is_valid():  # is it valid?
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            aut = Author.objects.filter(email__icontains=email)
            if not aut:
                author = Author(name=name, email=email)
                author.save()
                return render(request, 'authorInserted.html', {'aut': author, 'query': name})
            else:
                return render(request, 'authorInsertv2.html', {'error': False, 'exists': True})
    # if GET (or any other method), create blank form
    else:
        form = AuthorInsertForm()
    return render(request, 'authorInsertv2.html', {'form': form})


def publisherquery(request):
    # if POST request, process form data
    if request.method == 'POST':
        # create form instance and pass data to ir
        form = PublisherQueryForm(request.POST)
        if form.is_valid():  # is it valid?
            query = form.cleaned_data['query']
            publishers = Publisher.objects.filter(name__icontains=query)
            return render(request, 'publisherList.html', {'pubs': publishers, 'query': query})
    # if GET (or any other method), create blank form
    else:
        form = PublisherQueryForm()
    return render(request, 'publisherquery.html', {'form': form})


def publisherInsertQuery(request):
    #if not request.user.is_authenticated or request.user.username != 'admin':
    #    return redirect('/login')
    # if POST request, process form data
    if request.method == 'POST':
        # create form instance and pass data to ir
        form = PublisherInsertForm(request.POST)
        if form.is_valid():  # is it valid?
            name = form.cleaned_data['name']
            city = form.cleaned_data['city']
            country = form.cleaned_data['country']
            website= form.cleaned_data['website']
            pub = Publisher.objects.filter(name__icontains=name)
            if not pub:
                publisher = Publisher(name=name, city=city, country=country, website=website)
                publisher.save()
                return render(request, 'publisherInserted.html', {'pub': publisher, 'query': name})
            else:
                return render(request, 'publisherInsertv2.html', {'error': False, 'exists': True})
    # if GET (or any other method), create blank form
    else:
        form = PublisherInsertForm()
    return render(request, 'publisherInsertv2.html', {'form': form})
