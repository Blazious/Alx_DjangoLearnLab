from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm  # We'll create this form later

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """View for listing all books. Requires can_view permission."""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """View for creating a new book. Requires can_create permission."""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            messages.success(request, 'Book created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form, 'action': 'Create'})

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
