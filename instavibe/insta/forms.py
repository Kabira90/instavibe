

from django import forms
from .models import Profile
from .models import Post
from .models import Highlight, Story

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']



# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['image', 'caption']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'video', 'caption']






class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['image', 'caption']







class HighlightForm(forms.ModelForm):
    class Meta:
        model = Highlight
        fields = ['title', 'cover_image', 'stories']
        widgets = {
            'stories': forms.CheckboxSelectMultiple()
        }
