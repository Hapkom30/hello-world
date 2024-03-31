from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',
                  'category',
                  'text',
                  'author']


    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get('text')

        if text == title:
            raise ValidationError({'title': 'Заголовок не может быть индентичен тексту'})


        return cleaned_data

class StateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',
                  'category',
                  'text',
                  'author']


    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get('text')

        if text == title:
            raise ValidationError({'title': 'Заголовок не может быть индентичен тексту'})


        return cleaned_data
