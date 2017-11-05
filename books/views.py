from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
# Create your views here.
def search_form(request):
    return render(request, 'books/search_form.html')
    
from django.http import HttpResponse
from books.models import Book
# ...
def search(request):
    error = False
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        if not q:
            error = True
        books = Book.objects.filter(title__icontains=q)
        buttonName = ""
        if "Search" in request.GET: 
            buttonName = "Search"
        else:
            buttonName = "Search2"
        return render(request,'books/search_results.html',
            {'books':books,'query':q,'buttonName':buttonName})
    
    return render(request, 'books/search_form.html',
                      {'error': error})  
                      
def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'books/search_results.html',{'books': books, 'query': q})
    return render(request, 'books/search_form.html',{'error': error})
    
def search(request):
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters.')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'books/search_results.html',{'books': books, 'query': q})
    return render(request, 'books/search_form.html',{'errors': errors})  
    
    
 # view.py
from django.views.generic import ListView,DetailView
from books.models import Publisher,Book

class PublisherList(ListView):
    model = Publisher
    context_object_name = 'my_favorite_publishers'
    
class PublisherDetail(DetailView):

    model = Publisher

    def get_context_data(self,**kwargs):
        context = super(PublisherDetail,self).get_context_data(**kwargs)
        context['book_List'] = Book.objects.all()
        return context
        
    
    
    
    

    
    
    
    
    
    