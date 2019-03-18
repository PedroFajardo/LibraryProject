from django import forms
from app.models import Author, Book, Publisher


class BookQueryForm(forms.Form):
    query = forms.CharField(label='Search:', max_length=100)

class BookInsertForm(forms.Form):
    title = forms.CharField(label='Title:', max_length=100)
    date = forms.DateField(label='Date:')
    auts = ()
    for aut in Author.objects.all():
        auts = auts + ((aut.name, aut.name),)
    authors = forms.MultipleChoiceField(label="Author(s):", widget=forms.SelectMultiple, choices=auts)
    pubs = ()
    for pub in Publisher.objects.all():
        pubs = pubs + ((pub.name, pub.name),)
    publisher = forms.ChoiceField(label="Publisher:", widget=forms.Select, choices=pubs)

class AuthorQueryForm(forms.Form):
    query = forms.CharField(label="Search:", max_length=100)

class AuthorInsertForm(forms.Form):
    name = forms.CharField(label="Name:", max_length=100)
    email = forms.EmailField(label="Email:", max_length=100)

class PublisherQueryForm(forms.Form):
    query = forms.CharField(label="Search:", max_length=100)

class PublisherInsertForm(forms.Form):
    name = forms.CharField(label="Name:", max_length=100)
    city = forms.CharField(label="City:", max_length=100)
    country = forms.CharField(label="Country:", max_length=100)
    website = forms.CharField(label="Website:", max_length=100)
