from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post, Tag 
from .models import Comment
from taggit.forms import TagWidget

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UserEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "profile_image")

class PostForm(forms.ModelForm):
    tags = forms.CharField(required=False, help_text="Comma-separated tags")

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write your post here...', 'class': 'form-control', 'rows': 8}),'tags': TagWidget()
        }
    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            tags_list = self.cleaned_data["tags"].split(",")
            instance.tags.clear()
            for tag_name in tags_list:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, _ = Tag.objects.get_or_create(name=tag_name)
                    instance.tags.add(tag)
        return instance

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Add a comment...',
                'class': 'form-control'
            })
        }

    def clean_content(self):
        content = (self.cleaned_data.get('content') or '').strip()
        if not content:
            raise forms.ValidationError("Comment cannot be empty.")
        return content        