from django import forms
from .models import Post

# forms.ModelForm은 ModelForm이라는 것을 알려주는 구문
class PostForm(forms.ModelForm):

    # class Meta는 이 폼을 만들기 위해서 어떤 model이 쓰여야 하는지 장고에 알려주는 구문
    class Meta:
        model = Post
        fields = ('title', 'text', 'head_image')