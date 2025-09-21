from django import forms
from django.core.validators import validate_email
from .models import Book

class ExampleForm(forms.Form):
    """Example form to demonstrate secure form handling"""
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'autocomplete': 'off'
        })
    )
    email = forms.EmailField(
        required=True,
        validators=[validate_email],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your message'
        })
    )

    def clean_name(self):
        """Sanitize name input"""
        name = self.cleaned_data['name']
        if len(name.strip()) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long")
        return name.strip()

    def clean_message(self):
        """Sanitize message input"""
        from django.utils.html import strip_tags
        message = self.cleaned_data['message']
        return strip_tags(message)

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