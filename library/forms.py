from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from django.forms import ModelForm, fields
from .models import Chat, Post, Category
from django import forms


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('message', )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'desc', 'published_date', 'category',)


class SearchForm(forms.Form):
    q = forms.CharField()
    c = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].label = ''
        self.fields['c'].required = False
        self.fields['c'].label= 'Category'
        self.fields['q'].label = ''
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control'},
        )
        self.fields['q'].widget.attrs.update(
            {'placeholder': 'Search for posts'}
        )


class AddPostForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('name')
    )
    title = forms.CharField()
    desc = forms.CharField()
    file = forms.FileField()
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].label = 'Select a category'
        self.fields['title'].label = ''
        self.fields['desc'].label = ''
        self.fields['file'].label = 'Choose File'
        self.fields['file'].required = False

        self.fields['category'].widget.attrs.update(
            {'class': 'form-select'},
        )
        self.fields['title'].widget.attrs.update(
            {'class': 'form-control'},
        )
        self.fields['desc'].widget.attrs.update(
            {'class': 'form-control'},
        )
       

        self.fields['title'].widget.attrs.update(
            {'placeholder': 'Post Title'}
        )
        self.fields['desc'].widget.attrs.update(
            {'placeholder': 'Post Description'}
        )
    
       
        
    



