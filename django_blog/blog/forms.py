from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }

class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Enter tags separated by commas (e.g., django, python, blog)'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            # Pre-fill tags with existing tags as comma-separated list
            self.fields['tags'].initial = ', '.join([tag.name for tag in self.instance.tags.all()])

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        # Handle tags
        if self.cleaned_data['tags']:
            tag_names = [name.strip() for name in self.cleaned_data['tags'].split(',') if name.strip()]
            tags = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                tags.append(tag)
            instance.tags.set(tags)
        else:
            instance.tags.clear()
        return instance
