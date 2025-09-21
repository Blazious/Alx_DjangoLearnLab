from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.html import escape
import logging
from .models import Book
from .forms import BookForm
from .forms import ExampleForm  # Explicit import of ExampleForm

logger = logging.getLogger(__name__)

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View for listing all books. Requires can_view permission."""
    books = Book.objects.select_related('category').all()
    
    # Secure search implementation
    if 'q' in request.GET:
        query = request.GET.get('q', '').strip()
        if query:
            # Use Q objects for complex queries and parameterized queries
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(isbn__exact=query)
            )
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'query': escape(request.GET.get('q', ''))  # Escape search query for display
    })

from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

@permission_required('bookshelf.can_create', raise_exception=True)
@require_http_methods(['GET', 'POST'])
def book_create(request):
    """View for creating a new book. Requires can_create permission."""
    try:
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                book = form.save(commit=False)
                book.owner = request.user
                book.save()
                messages.success(request, 'Book created successfully!')
                logger.info(f'Book created: {book.id} by user: {request.user.id}')
                return redirect('book_detail', pk=book.pk)
            else:
                logger.warning(f'Invalid book creation attempt by user: {request.user.id}')
        else:
            form = BookForm()
            
        return render(request, 'bookshelf/book_form.html', {
            'form': form,
            'action': 'Create',
            'csrf_token': request.META.get('CSRF_COOKIE', '')  # For AJAX requests
        })
    except Exception as e:
        logger.error(f'Error in book_create: {str(e)}')
        messages.error(request, 'An error occurred while creating the book.')
        return redirect('book_list')

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """View for editing an existing book. Requires can_edit permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Edit'})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """View for deleting a book. Requires can_delete permission."""
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_list')
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

@require_http_methods(['GET', 'POST'])
def example_form_view(request):
    """Example view demonstrating secure form handling."""
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the sanitized data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Example: Log the submission (in a real app, you might save to DB)
            logger.info(f'Form submitted by {name} ({email})')
            
            messages.success(request, 'Form submitted successfully!')
            return redirect('book_list')  # Redirect to a success page
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {
        'form': form,
        'title': 'Example Form'
    })
