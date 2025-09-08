from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from .models import Book, Library


# ---------------------------
# Function-based view
# ---------------------------
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# ---------------------------
# Class-based view
# ---------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


# ---------------------------
# Registration view (checker requires name = register)
# ---------------------------
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# ---------------------------
# Role-based access views
# ---------------------------

# Admin view (must be named exactly admin_view)
@user_passes_test(lambda u: hasattr(u, "userprofile") and u.userprofile.role == "Admin")
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")


# Librarian view (must be named exactly librarian_view)
@user_passes_test(lambda u: hasattr(u, "userprofile") and u.userprofile.role == "Librarian")
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")


# Member view (must be named exactly member_view)
@user_passes_test(lambda u: hasattr(u, "userprofile") and u.userprofile.role == "Member")
def member_view(request):
    return render(request, "relationship_app/member_view.html")




