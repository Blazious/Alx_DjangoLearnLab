from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date', 'publisher', 
                 'category', 'condition', 'description', 'cover_image']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and security attributes to form fields
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',  # Prevent browser autocomplete
                'data-lpignore': 'true'  # Prevent LastPass from filling
            })
            
    def clean_isbn(self):
        """Validate ISBN format"""
        isbn = self.cleaned_data['isbn']
        if not isbn.isdigit():
            raise forms.ValidationError("ISBN must contain only numbers")
        if len(isbn) not in [10, 13]:
            raise forms.ValidationError("ISBN must be 10 or 13 digits")
        return isbn
        
    def clean_title(self):
        """Sanitize title input"""
        title = self.cleaned_data['title']
        # Remove potentially dangerous characters
        title = ''.join(char for char in title if char.isprintable())
        return title
        
    def clean_description(self):
        """Sanitize description input"""
        from django.utils.html import strip_tags
        description = self.cleaned_data['description']
        # Remove HTML tags from description
        return strip_tags(description)